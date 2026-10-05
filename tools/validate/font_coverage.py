"""Check that every character used by translations exists in a font.

Reads the font's cmap table directly (TrueType/OpenType, formats 4 and 12),
so no third-party packages are needed.

Usage:
  python font_coverage.py <font.ttf|otf> <file-or-dir> [...]

Text sources are scanned as UTF-8. For .po files only msgstr lines are used;
for .tsv files only the last column (the translation). Other files are
scanned whole. ASCII control characters are ignored.

Exit status: 0 if every character is covered, 1 otherwise.
"""
import os, struct, sys
from collections import Counter

# Characters the engine never draws as glyphs
IGNORED = set("\t\r\n")
# U8 control characters inside game text (Master Plan §9.1)
U8_CONTROLS = set("~*%^")


def read_cmap(path):
    data = open(path, "rb").read()
    num_tables = struct.unpack_from(">H", data, 4)[0]
    cmap_off = None
    for i in range(num_tables):
        tag, _, off, _ = struct.unpack_from(">4sIII", data, 12 + 16 * i)
        if tag == b"cmap":
            cmap_off = off
    if cmap_off is None:
        raise ValueError("no cmap table")

    n = struct.unpack_from(">H", data, cmap_off + 2)[0]
    subtables = []
    for i in range(n):
        pid, eid, off = struct.unpack_from(">HHI", data, cmap_off + 4 + 8 * i)
        subtables.append((pid, eid, cmap_off + off))

    chars = set()
    for pid, eid, off in subtables:
        if not (pid == 3 and eid in (1, 10)) and pid != 0:
            continue
        fmt = struct.unpack_from(">H", data, off)[0]
        if fmt == 4:
            segx2 = struct.unpack_from(">H", data, off + 6)[0]
            ends = struct.unpack_from(">%dH" % (segx2 // 2), data, off + 14)
            starts = struct.unpack_from(">%dH" % (segx2 // 2), data, off + 16 + segx2)
            deltas = struct.unpack_from(">%dh" % (segx2 // 2), data, off + 16 + 2 * segx2)
            ro_off = off + 16 + 3 * segx2
            ranges = struct.unpack_from(">%dH" % (segx2 // 2), data, ro_off)
            for s, (start, end, delta, ro) in enumerate(zip(starts, ends, deltas, ranges)):
                for c in range(start, end + 1):
                    if c == 0xFFFF:
                        continue
                    if ro == 0:
                        gid = (c + delta) & 0xFFFF
                    else:
                        addr = ro_off + 2 * s + ro + 2 * (c - start)
                        gid = struct.unpack_from(">H", data, addr)[0]
                        if gid:
                            gid = (gid + delta) & 0xFFFF
                    if gid:
                        chars.add(c)
        elif fmt == 12:
            ngroups = struct.unpack_from(">I", data, off + 12)[0]
            for g in range(ngroups):
                start, end, gid = struct.unpack_from(">III", data, off + 16 + 12 * g)
                for c in range(start, end + 1):
                    if gid + (c - start):
                        chars.add(c)
    return chars


def text_of(path):
    text = open(path, encoding="utf-8").read()
    ext = os.path.splitext(path)[1].lower()
    if ext == ".po":
        out = []
        in_str = False
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("msgstr"):
                in_str = True
                line = line[line.find('"'):]
            elif not line.startswith('"'):
                in_str = False
                continue
            if in_str and line.startswith('"'):
                out.append(line[1:-1].encode("latin-1", "backslashreplace").decode("unicode_escape")
                           if "\\" in line else line[1:-1])
        return "\n".join(out)
    if ext == ".tsv":
        return "\n".join(l.split("\t")[-1] for l in text.splitlines()
                         if l and not l.startswith("#"))
    return text


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in sorted(files):
                    if f.endswith((".po", ".tsv", ".txt")):
                        yield os.path.join(root, f)
        else:
            yield p


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    font = sys.argv[1]
    covered = read_cmap(font)

    used = Counter()
    where = {}
    for f in iter_files(sys.argv[2:]):
        for ch in text_of(f):
            if ch in IGNORED or ch in U8_CONTROLS or ord(ch) < 0x20:
                continue
            used[ch] += 1
            where.setdefault(ch, f)

    missing = sorted((c for c in used if ord(c) not in covered), key=lambda c: -used[c])
    print(f"font: {os.path.basename(font)}  glyphs: {len(covered)}")
    print(f"distinct characters used: {len(used)}  missing: {len(missing)}")
    for c in missing:
        print(f"  U+{ord(c):04X} {c}  x{used[c]}  first in {where[c]}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
