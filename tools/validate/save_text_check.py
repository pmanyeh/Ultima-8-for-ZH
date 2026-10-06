"""Check a ScummVM Ultima VIII savegame for localized (CJK) text.

Savegames must only contain the original English game text (Master Plan
§16): this decompresses the save, reports every run of CJK characters and
lists the bark/text widget objects with their text.

Usage:
  python save_text_check.py <savefile> [--show "text to look for"]...
Exit code 1 if CJK text was found.
"""
import argparse
import re
import sys
import zlib

CJK_RANGES = [(0x2E80, 0x9FFF), (0xF900, 0xFAFF), (0xFE30, 0xFE4F), (0xFF00, 0xFFEF),
              (0x20000, 0x2FFFF)]


def is_cjk(cp):
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def decompress(raw):
    """The savegame body is a gzip stream; ScummVM may put a header before it."""
    pos = raw.find(b"\x1f\x8b\x08")
    while pos >= 0:
        try:
            d = zlib.decompressobj(16 + zlib.MAX_WBITS)
            return d.decompress(raw[pos:]), pos
        except zlib.error:
            pos = raw.find(b"\x1f\x8b\x08", pos + 1)
    return raw, -1


def cjk_runs(data):
    """Find runs of valid UTF-8 that contain CJK characters."""
    runs = []
    for m in re.finditer(rb"(?:[\xC2-\xF4][\x80-\xBF]{1,3}|[\x20-\x7E])+", data):
        chunk = m.group(0)
        try:
            text = chunk.decode("utf-8")
        except UnicodeDecodeError:
            continue
        # one CJK character can occur by chance in binary data; text has more
        if re.search(r"[^\x00-\x7F]{2}", text) and \
                sum(is_cjk(ord(c)) for c in text) >= 2:
            runs.append((m.start(), text))
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("save")
    ap.add_argument("--show", action="append", default=[], help="English text to look for")
    a = ap.parse_args()

    raw = open(a.save, "rb").read()
    data, gz = decompress(raw)
    print(f"{a.save}: {len(raw)} bytes, " +
          (f"gzip at {gz}, {len(data)} bytes decompressed" if gz >= 0 else "not compressed"))

    for name in (b"BarkGump", b"TextWidget", b"AskGump"):
        print(f"  {name.decode()}: {data.count(name)} occurrence(s)")
    for text in a.show:
        n = data.count(text.encode("latin-1"))
        print(f"  \"{text}\": {n} occurrence(s)")

    runs = cjk_runs(data)
    if runs:
        print(f"FAIL: {len(runs)} run(s) of CJK text in the save")
        for off, text in runs[:20]:
            print(f"  @{off:08X}: {ascii(text[:80])}")
        sys.exit(1)
    print("OK: no CJK text in the save")


if __name__ == "__main__":
    main()
