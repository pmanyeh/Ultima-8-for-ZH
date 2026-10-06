"""Phase 8: count the player-visible text in the U8 game data, per surface.

Read-only. Reports:
  - usecode intrinsic call sites that show text (bark, ask, Book/Scroll/
    Grave/Plaque::read), with the event they are in, whether the text is a
    literal and its size
  - credits / quotes text (STATIC/ECREDITS.DAT, QUOTES.DAT)
  - movie subtitles (STATIC/EINTRO.SKF, ENDGAME.SKF)

Usage:
  python text_survey.py [--samples N] [--json out.json]
"""
import argparse
import collections
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import u8dis  # noqa: E402

GAME = os.path.join(os.path.dirname(u8dis.USECODE), "..")
STATIC = os.path.join(GAME, "STATIC")

TEXT_INTRINSICS = {0x49: "bark", 0x4A: "ask", 0x6E: "book", 0x6F: "scroll", 0x70: "grave", 0x71: "plaque"}
EVENT_NAMES = {0x00: "look", 0x01: "use", 0x02: "anim", 0x04: "cachein", 0x05: "hit", 0x06: "gotHit",
               0x07: "hatch", 0x08: "schedule", 0x09: "release", 0x0A: "equip", 0x0B: "unequip",
               0x0C: "combine", 0x0F: "calledFromAnim", 0x10: "enterFastArea", 0x11: "leaveFastArea",
               0x12: "cast", 0x13: "justMoved", 0x14: "AvatarStoleSomething", 0x15: "guardianBark"}


def usecode_survey(samples):
    data, ents = u8dis.load_flex(u8dis.USECODE)
    names = u8dis.class_names(data, ents)
    sites = collections.defaultdict(list)   # kind -> [(cls, pc, event, text or None)]
    for cls in range(len(ents) - 2):
        cd = u8dis.obj(data, ents, cls + 2)
        if len(cd) < 0x8C:
            continue
        starts = []
        for e in range(32):
            off = struct.unpack_from("<I", cd, 12 + 4 * e)[0]
            if off:
                starts.append((off, e))
        starts.sort()

        def event_at(pc):
            ev = None
            for off, e in starts:
                if off <= pc:
                    ev = e
            return ev

        last_lit, concat = None, False
        for pc, op, args, s in u8dis.disasm(cd[0x0C:]):
            if op == 0x0D:
                last_lit, concat = s.decode("latin-1"), False
            elif op == 0x16:
                concat = True
            elif op == 0x0F:
                fn = struct.unpack_from("<H", args, 1)[0]
                if fn in TEXT_INTRINSICS:
                    kind = TEXT_INTRINSICS[fn]
                    text = last_lit if (last_lit is not None and not concat) else None
                    sites[kind].append((cls, pc, event_at(pc), text))
                    if kind != "ask":
                        last_lit = None
    return names, sites


def flex_objects(path):
    data, ents = u8dis.load_flex(path)
    return [u8dis.obj(data, ents, i) for i in range(len(ents)) if ents[i][1]]


def skf_subtitles(path):
    """Subtitle objects: 6 byte header, then NUL terminated text."""
    subs = []
    for o in flex_objects(path):
        if len(o) > 7:
            text = o[6:].split(b"\0")[0]
            if len(text) > 1 and all(32 <= c < 127 or c in (10, 13) for c in text):
                subs.append(text.decode("latin-1"))
    return subs


def credit_text(path):
    raw = open(path, "rb").read()
    out = bytearray()
    for i, c in enumerate(raw):
        if i < 2:
            x = 0
        elif i == 2:
            x = 0xE1
        else:
            x = 0x20 * (i + 1) + (i >> 1)
            x += (i % 0x40) * ((i & 0xC0) >> 6) * 0x40
        d = (c ^ x) & 0xFF
        out.append(10 if d == 0 else d)
    return out.decode("latin-1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--json")
    a = ap.parse_args()

    names, sites = usecode_survey(a.samples)
    report = {}
    print("== usecode text intrinsics")
    for kind in ("bark", "ask", "book", "scroll", "grave", "plaque"):
        lst = sites[kind]
        lits = [t for _, _, _, t in lst if t is not None]
        distinct = set(lits)
        chars = sum(len(t) for t in distinct)
        by_event = collections.Counter(EVENT_NAMES.get(e, f"ev{e:02X}" if e is not None else "func")
                                       for _, _, e, _ in lst)
        classes = len({c for c, _, _, _ in lst})
        print(f"{kind:7} sites={len(lst):5} classes={classes:4} literal={len(lits):5} "
              f"distinct={len(distinct):5} chars(distinct)={chars:7}")
        print("        events: " + ", ".join(f"{k} {v}" for k, v in by_event.most_common(8)))
        for c, pc, e, t in lst[:0] if kind in ("bark", "ask") else lst[:a.samples]:
            sample = (t or "<dynamic>")[:90].replace("\n", " ")
            print(f"        {names.get(c, '?')} {c:04X}:{pc:04X}  {sample}")
        report[kind] = {"sites": len(lst), "classes": classes, "literal": len(lits),
                        "distinct": len(distinct), "chars": chars, "events": dict(by_event)}

    # look barks (event 00): item / NPC names shown when the Avatar looks at something
    look = [t for _, _, e, t in sites["bark"] if e == 0x00 and t is not None]
    print(f"look barks (event 00): {len(sites['bark']) and sum(1 for s in sites['bark'] if s[2] == 0)} sites, "
          f"distinct texts {len(set(look))}, e.g. " +
          ", ".join(repr(t) for t in sorted(set(look))[:12]))
    report["look"] = {"distinct": len(set(look))}

    print("\n== static files")
    for fn in ("ECREDITS.DAT", "QUOTES.DAT"):
        p = os.path.join(STATIC, fn)
        if os.path.exists(p):
            t = credit_text(p)
            lines = [l for l in t.split("\n") if l.strip()]
            print(f"{fn:13} lines={len(lines):4} chars={len(t):6}  e.g. {lines[3:6]}")
            report[fn] = {"lines": len(lines), "chars": len(t)}
    for fn in ("EINTRO.SKF", "ENDGAME.SKF"):
        p = os.path.join(STATIC, fn)
        if os.path.exists(p):
            subs = skf_subtitles(p)
            print(f"{fn:13} subtitles={len(subs):3} chars={sum(map(len, subs)):5}  e.g. {subs[:2]}")
            report[fn] = {"subtitles": len(subs), "chars": sum(map(len, subs))}

    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=1)


if __name__ == "__main__":
    main()
