"""Compare Ultima VIII savegames section by section (Phase 12 save matrix).

A ScummVM U8 savegame is a gzip stream holding a small container
("8UMV", version, count, then name[12] + size + data per section: GAME, INFO,
KERNEL, OBJECTS, WORLD, MAPS, CURRENTMAP, UCSTRINGS, UCGLOBALS, UCLISTS, APP),
followed by ScummVM's metadata (thumbnail, description).

For each pair of saves this reports which sections are identical, how many
bytes differ, the differing UCGLOBALS bytes (usecode flags) and the strings
that only one of them has. Every save is also checked for CJK text (it must
only contain the original English text, Master Plan §16).

Two saves of the same game taken at different moments always differ in the
time-dependent sections (KERNEL, OBJECTS, MAPS: processes, NPC positions).
Compare the localized run against a second English run (--baseline) to see
which differences come from timing and which from the language mode.

Usage:
  python save_compare.py <save A> <save B> [--baseline <save C>]
    reports A vs B (and A vs C); exit code 1 if a save holds CJK text or
    the usecode state (UCGLOBALS) of A and B differs more than A and C
  python save_compare.py --list <save>
"""
import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
from save_text_check import decompress, cjk_runs  # noqa: E402

LOGIC_SECTIONS = ("GAME", "WORLD", "UCGLOBALS", "UCSTRINGS", "UCLISTS")


def read_save(path):
    raw = open(path, "rb").read()
    data, _ = decompress(raw)
    ident, version, count = struct.unpack_from("<IIH", data, 0)
    if ident != 0x564D5538:              # "8UMV"
        raise ValueError(f"{path}: not an Ultima VIII savegame")
    sections, pos = {}, 10
    for _ in range(count):
        name = data[pos:pos + 12].split(b"\0")[0].decode("ascii")
        size = struct.unpack_from("<I", data, pos + 12)[0]
        sections[name] = data[pos + 16:pos + 16 + size]
        pos += 16 + size
    return {"version": version, "sections": sections, "data": data, "end": pos}


def strings(blob):
    return set(m.group(0).decode("latin-1") for m in re.finditer(rb"[\x20-\x7E]{4,}", blob))


def diff_bytes(a, b):
    n = sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))
    return n


def compare(a, b, name_a, name_b):
    print(f"\n{name_a}  vs  {name_b}")
    result = {}
    for sec in a["sections"]:
        x, y = a["sections"][sec], b["sections"].get(sec, b"")
        n = diff_bytes(x, y)
        result[sec] = n
        state = "identical" if n == 0 else f"{n} byte(s) differ" + \
            (f" (size {len(x)} / {len(y)})" if len(x) != len(y) else "")
        print(f"  {sec:11} {len(x):7}  {state}")
    ga, gb = a["sections"].get("UCGLOBALS", b""), b["sections"].get("UCGLOBALS", b"")
    offs = [i for i, (x, y) in enumerate(zip(ga, gb)) if x != y]
    if offs:
        print("  UCGLOBALS differing bytes: " +
              ", ".join(f"{o}: {ga[o]:02X}/{gb[o]:02X}" for o in offs[:20]))
    sa, sb = strings(a["sections"].get("UCSTRINGS", b"")), strings(b["sections"].get("UCSTRINGS", b""))
    for label, only in (("only in A", sa - sb), ("only in B", sb - sa)):
        for s in sorted(only)[:10]:
            print(f"  UCSTRINGS {label}: {s[:80]!r}")
    return result


def check_cjk(save, path):
    """Only the game sections count: ScummVM's metadata after them holds the
    save description, which ScummVM writes in its own GUI language (e.g. an
    autosave is named "自动保存" when the launcher is in Chinese)."""
    game = save["data"][:save["end"]]
    runs = cjk_runs(game)
    meta = cjk_runs(save["data"][save["end"]:])
    note = f" (ScummVM metadata: {', '.join(t for _, t in meta)})" if meta else ""
    print(f"{path}: {'FAIL, ' + str(len(runs)) + ' CJK text run(s) in game data' if runs else 'no CJK text in game data'}{note}")
    return not runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("saves", nargs="*")
    ap.add_argument("--baseline")
    ap.add_argument("--list")
    a = ap.parse_args()

    if a.list:
        s = read_save(a.list)
        print(f"{a.list}: version {s['version']}")
        for name, blob in s["sections"].items():
            print(f"  {name:11} {len(blob):7}")
        return

    if len(a.saves) != 2:
        ap.error("give two saves")
    paths = a.saves + ([a.baseline] if a.baseline else [])
    saves = [read_save(p) for p in paths]
    ok = all([check_cjk(s, p) for s, p in zip(saves, paths)])

    ab = compare(saves[0], saves[1], "A " + paths[0], "B " + paths[1])
    if a.baseline:
        ac = compare(saves[0], saves[2], "A " + paths[0], "C " + paths[2])
        print("\nlogic sections, differing bytes (A vs B / A vs C baseline):")
        for sec in LOGIC_SECTIONS:
            print(f"  {sec:11} {ab.get(sec, 0):6} / {ac.get(sec, 0):6}")
        if ab.get("UCGLOBALS", 0) > ac.get("UCGLOBALS", 0):
            print("FAIL: usecode state differs more than between the two English runs")
            ok = False
    print("\nOK" if ok else "\nFAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
