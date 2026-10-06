"""Compile the U8 translation PO files into the single catalog the engine reads.

The output is a gettext MO file (msgfmt compatible, little endian, no hash
table). Each key is "<msgctxt>\\x04<msgid>", as gettext does for entries with
a context; the engine looks entries up by context + exact English text.

Checks (errors stop the build, nothing is written):
  - PO syntax
  - msgctxt present and in a known form: "bark CCCC:IIII" or "ask CCCC" (hex)
  - no plural entries
  - the same context + English text only once across all files
  - the header Language matches --lang (when the header has one)
Skipped with a note (the game shows English for these):
  - untranslated (empty msgstr) and fuzzy entries, obsolete (#~) entries

Usage:
  python po_compile.py <lang> <po file or directory>... -o <out.mo>
  python po_compile.py zh_TW localization/zh_TW -o private_test/extra/u8_zh_TW.mo
"""
import argparse
import os
import re
import struct
import sys

CONTEXT_RE = re.compile(r"^(?:bark ([0-9A-Fa-f]{1,4}):([0-9A-Fa-f]{1,4})|ask ([0-9A-Fa-f]{1,4}))$")
ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b", "f": "\f", "v": "\v",
           "\\": "\\", '"': '"', "'": "'", "?": "?"}


class POError(Exception):
    pass


class Entry:
    def __init__(self, path, line):
        self.path, self.line = path, line
        self.msgctxt = None
        self.msgid = None
        self.msgid_plural = None
        self.msgstr = None
        self.msgstr_plural = {}
        self.flags = set()
        self.comments = []
        self.obsolete = False

    def where(self):
        return f"{self.path}:{self.line}"


def unquote(s, where):
    s = s.strip()
    if len(s) < 2 or s[0] != '"' or s[-1] != '"':
        raise POError(f"{where}: expected a quoted string: {s}")
    out, i, body = [], 0, s[1:-1]
    while i < len(body):
        c = body[i]
        if c == "\\":
            i += 1
            if i >= len(body):
                raise POError(f"{where}: string ends with a backslash")
            e = body[i]
            if e in ESCAPES:
                out.append(ESCAPES[e])
            elif e in "01234567":
                j = i
                while j < len(body) and j < i + 3 and body[j] in "01234567":
                    j += 1
                out.append(chr(int(body[i:j], 8)))
                i = j - 1
            elif e == "x":
                j = i + 1
                while j < len(body) and body[j] in "0123456789abcdefABCDEF":
                    j += 1
                if j == i + 1:
                    raise POError(f"{where}: bad \\x escape")
                out.append(chr(int(body[i + 1:j], 16)))
                i = j - 1
            else:
                raise POError(f"{where}: unknown escape \\{e}")
        elif c == '"':
            raise POError(f"{where}: unescaped quote inside string")
        else:
            out.append(c)
        i += 1
    return "".join(out)


def parse_po(path):
    """Parse a PO file into a list of Entry (header included)."""
    with open(path, encoding="utf-8-sig") as f:
        lines = f.read().split("\n")

    entries = []
    cur = None
    field = None      # (name, index) the next continuation string belongs to

    def finish():
        nonlocal cur
        if cur is not None and cur.msgid is not None:
            entries.append(cur)
        elif cur is not None and (cur.msgctxt is not None or cur.msgstr is not None):
            raise POError(f"{cur.where()}: entry without msgid")
        cur = None

    def set_field(name, index, value):
        if name == "msgstr_plural":
            cur.msgstr_plural[index] = cur.msgstr_plural.get(index, "") + value
        else:
            setattr(cur, name, (getattr(cur, name) or "") + value)

    for n, raw in enumerate(lines, 1):
        line = raw.rstrip("\r")
        where = f"{path}:{n}"
        stripped = line.strip()
        if not stripped:
            finish()
            field = None
            continue

        obsolete = stripped.startswith("#~")
        if obsolete:
            stripped = stripped[2:].strip()
            if not stripped:
                continue
        elif stripped.startswith("#"):
            # a comment after the strings starts a new entry
            if cur is not None and cur.msgid is not None and field is not None:
                finish()
            if cur is None:
                cur = Entry(path, n)
            if stripped.startswith("#,"):
                cur.flags.update(f.strip() for f in stripped[2:].split(",") if f.strip())
            else:
                cur.comments.append(stripped)
            field = None
            continue

        if stripped.startswith('"'):
            if field is None:
                raise POError(f"{where}: string continuation without keyword")
            set_field(field[0], field[1], unquote(stripped, where))
            continue

        m = re.match(r"^(msgctxt|msgid_plural|msgid|msgstr)(?:\[(\d+)\])?\s+(.*)$", stripped)
        if not m:
            raise POError(f"{where}: cannot parse: {line}")
        key, index, rest = m.group(1), m.group(2), m.group(3)

        # msgctxt / msgid after a complete entry starts the next one
        if key in ("msgctxt", "msgid") and cur is not None and cur.msgstr is not None:
            finish()
        if key == "msgid" and cur is not None and cur.msgid is not None:
            finish()
        if cur is None:
            cur = Entry(path, n)
        cur.obsolete = cur.obsolete or obsolete

        if key == "msgstr" and index is not None:
            name = "msgstr_plural"
            cur.msgstr = cur.msgstr or ""
        else:
            name = key
            if index is not None:
                raise POError(f"{where}: {key} cannot have an index")
            if getattr(cur, name) is not None:
                raise POError(f"{where}: duplicate {key}")
        field = (name, int(index) if index is not None else None)
        if name == "msgstr_plural":
            cur.msgstr_plural[field[1]] = ""
        else:
            setattr(cur, name, "")
        set_field(name, field[1], unquote(rest, where))
    finish()

    for e in entries:
        if e.msgstr is None:
            raise POError(f"{e.where()}: entry without msgstr")
    return entries


def header_fields(entry):
    fields = {}
    for line in entry.msgstr.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip().lower()] = v.strip()
    return fields


def canonical_context(ctx):
    m = CONTEXT_RE.match(ctx or "")
    if not m:
        return None
    if m.group(3) is not None:
        return f"ask {int(m.group(3), 16):04X}"
    return f"bark {int(m.group(1), 16):04X}:{int(m.group(2), 16):04X}"


def norm_lang(s):
    return s.strip().lower().replace("-", "_")


def collect(lang, inputs):
    files = []
    for p in inputs:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                files += [os.path.join(root, n) for n in names if n.endswith(".po")]
        else:
            files.append(p)
    files.sort()
    if not files:
        raise POError("no PO files found")

    errors, seen, out = [], {}, {}
    stats = {"files": len(files), "translated": 0, "untranslated": 0, "fuzzy": 0, "obsolete": 0}
    for path in files:
        try:
            entries = parse_po(path)
        except POError as e:
            errors.append(str(e))
            continue
        for e in entries:
            if e.obsolete:
                stats["obsolete"] += 1
                continue
            if e.msgid == "" and e.msgctxt is None:
                file_lang = header_fields(e).get("language", "")
                if file_lang and norm_lang(file_lang) != norm_lang(lang):
                    errors.append(f"{e.where()}: header Language {file_lang} is not {lang}")
                continue
            ctx = canonical_context(e.msgctxt)
            if ctx is None:
                errors.append(f"{e.where()}: missing or unknown msgctxt {e.msgctxt!r}")
                continue
            if e.msgid_plural is not None or e.msgstr_plural:
                errors.append(f"{e.where()}: plural entries are not supported")
                continue
            if e.msgid == "":
                errors.append(f"{e.where()}: empty msgid")
                continue
            key = (ctx, e.msgid)
            if key in seen:
                errors.append(f"{e.where()}: duplicate of {seen[key]} ({ctx} {e.msgid!r})")
                continue
            seen[key] = e.where()
            if "\0" in e.msgstr or "\0" in e.msgid:
                errors.append(f"{e.where()}: NUL character in text")
                continue
            if "fuzzy" in e.flags:
                stats["fuzzy"] += 1
                continue
            if e.msgstr == "":
                stats["untranslated"] += 1
                continue
            out[ctx + "\x04" + e.msgid] = e.msgstr
            stats["translated"] += 1
    if errors:
        raise POError("\n".join(errors))
    return out, stats


def write_mo(path, lang, entries):
    header = ("Content-Type: text/plain; charset=UTF-8\n"
              "Content-Transfer-Encoding: 8bit\n"
              f"Language: {lang}\n"
              "X-Generator: u8 po_compile.py\n")
    items = [(b"", header.encode("utf-8"))]
    items += sorted((k.encode("utf-8"), v.encode("utf-8")) for k, v in entries.items())
    n = len(items)
    orig_table = 28
    trans_table = orig_table + 8 * n
    data_start = trans_table + 8 * n

    blob = bytearray()
    orig, trans = [], []
    for k, _ in items:
        orig.append((len(k), data_start + len(blob)))
        blob += k + b"\0"
    for _, v in items:
        trans.append((len(v), data_start + len(blob)))
        blob += v + b"\0"

    out = bytearray(struct.pack("<7I", 0x950412DE, 0, n, orig_table, trans_table, 0, data_start))
    for length, off in orig + trans:
        out += struct.pack("<2I", length, off)
    out += blob
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "wb") as f:
        f.write(out)
    return len(out)


def main():
    ap = argparse.ArgumentParser(description="Compile U8 translation PO files into one MO catalog")
    ap.add_argument("lang", help="language code, e.g. zh_TW")
    ap.add_argument("inputs", nargs="+", help="PO files or directories (searched recursively)")
    ap.add_argument("-o", "--output", required=True, help="output .mo file")
    a = ap.parse_args()

    try:
        entries, stats = collect(a.lang, a.inputs)
    except POError as e:
        print(f"ERROR:\n{e}", file=sys.stderr)
        sys.exit(1)
    size = write_mo(a.output, a.lang, entries)
    print(f"{a.output}: {stats['translated']} entries from {stats['files']} files, {size} bytes "
          f"(skipped: {stats['untranslated']} untranslated, {stats['fuzzy']} fuzzy, "
          f"{stats['obsolete']} obsolete)")


if __name__ == "__main__":
    main()
