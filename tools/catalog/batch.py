"""Work on a translation batch: list the untranslated entries of some classes
and apply translations written in a simple text file.

  python batch.py dump <lang> <class hex>... [--all]
      the entries in conversation order with their notes (--all: also the
      translated ones), as a translation file to fill in

  python batch.py apply <lang> <file> [--comment "P13 batch 1"]
      write the translations into the PO files

Translation file (UTF-8): one block per entry, blank lines between blocks
  @ <msgctxt>
  < <English msgid; differences in spacing do not matter>
  > <translation>
"#" lines are comments (dump writes the notes there). An entry with an empty
"> " line is left untranslated.

apply checks that the translation keeps the control characters (~ * % ^ @ &)
and placeholders of the English text, and that each block names exactly one
entry of the PO files; nothing is written if a block is wrong.
"""
import argparse
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from po_compile import parse_po, canonical_context, placeholder_error  # noqa: E402
import u8catalog  # noqa: E402

CONTROL = "~*%^@&"


def po_quote(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def class_files(lang, classes):
    files = u8catalog.existing_class_files(lang)
    out = []
    for c in classes:
        cls = int(c, 16)
        if cls not in files:
            sys.exit(f"no PO file for class {c}")
        out.append(files[cls])
    return out


def cmd_dump(a):
    for path in class_files(a.lang, a.classes):
        print(f"# ===== {os.path.basename(path)}")
        for e in parse_po(path):
            if not e.msgid or e.obsolete or (e.msgstr and not a.all):
                continue
            for c in e.comments:
                if c.startswith("#."):
                    print("# " + c[2:].strip())
            print(f"@ {e.msgctxt}")
            print(f"< {e.msgid}")
            print(f"> {e.msgstr}")
            print()


def read_blocks(path):
    blocks, cur = [], None
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if line.startswith("#") or not line.strip():
            continue
        tag, text = line[:2], line[2:]
        if tag == "@ ":
            cur = {"ctx": text.strip(), "line": n}
            blocks.append(cur)
        elif tag == "< " and cur is not None:
            cur["en"] = text
        elif tag in ("> ", ">") and cur is not None:
            cur["zh"] = text.strip()
        else:
            sys.exit(f"{path}:{n}: unexpected line: {line[:60]}")
    return blocks


def norm(text):
    """English for matching: runs of spaces / tabs count as one space"""
    return " ".join(text.split())


def check_text(en, zh):
    for ch in CONTROL:
        if en.count(ch) != zh.count(ch):
            return f"'{ch}' {en.count(ch)} in English, {zh.count(ch)} in the translation"
    if "{" in en + zh:
        return placeholder_error(en, zh)
    return None


def cmd_apply(a):
    blocks = [b for b in read_blocks(a.file) if b.get("zh")]
    # every PO entry by (context, English without spaces at the end)
    index = collections.defaultdict(list)
    pos = {}
    for path in u8catalog.all_po_files(a.lang):
        for e in parse_po(path):
            if e.msgid and not e.obsolete:
                ctx = canonical_context(e.msgctxt)
                index[(ctx, norm(e.msgid))].append((path, e))
    errors, todo = [], collections.defaultdict(dict)
    for b in blocks:
        where = f"{a.file}:{b['line']}"
        ctx = canonical_context(b["ctx"])
        found = index.get((ctx, norm(b.get("en", ""))), [])
        if len(found) > 1:
            # entries that differ only in spacing: the exact English decides
            found = [f for f in found if f[1].msgid == b.get("en", "")]
        if len(found) != 1:
            errors.append(f"{where}: {len(found)} entries for {b['ctx']} {b.get('en', '')[:50]!r}")
            continue
        path, e = found[0]
        err = check_text(e.msgid, b["zh"])
        if err:
            errors.append(f"{where}: {err}")
            continue
        todo[path][(e.msgctxt, e.msgid)] = b["zh"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    total = 0
    for path, items in todo.items():
        lines = open(path, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(lines):
            if lines[i].startswith("msgctxt "):
                ctx_line, j = lines[i], i + 1
                # msgid may span several lines
                k = j
                while k < len(lines) and not lines[k].startswith("msgstr"):
                    k += 1
                entry = next((x for x in parse_entry(lines[i:k + 1]) if x), None)
                if entry in items:
                    end = k + 1
                    while end < len(lines) and lines[end].startswith('"'):
                        end += 1
                    lines[k:end] = [f'msgstr "{po_quote(items[entry])}"']
                    if a.comment:
                        c = i
                        while c > 0 and lines[c - 1].startswith("#"):
                            c -= 1
                        tag = f"# {a.comment}"
                        if tag not in lines[c:i]:
                            lines.insert(c, tag)
                            i += 1
                    total += 1
                i = k + 1
            else:
                i += 1
        open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"{total} translations written to {len(todo)} files")


def parse_entry(chunk):
    """(msgctxt, msgid) of the lines msgctxt ... msgstr"""
    from po_compile import unquote
    ctx, msgid, cur = None, None, None
    for line in chunk:
        if line.startswith("msgctxt "):
            ctx, cur = unquote(line[8:], ""), "ctx"
        elif line.startswith("msgid "):
            msgid, cur = unquote(line[6:], ""), "id"
        elif line.startswith('"'):
            if cur == "ctx":
                ctx += unquote(line, "")
            elif cur == "id":
                msgid += unquote(line, "")
        elif line.startswith("msgstr"):
            break
    yield (ctx, msgid) if ctx is not None and msgid is not None else None


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dump")
    d.add_argument("lang")
    d.add_argument("classes", nargs="+")
    d.add_argument("--all", action="store_true")
    p = sub.add_parser("apply")
    p.add_argument("lang")
    p.add_argument("file")
    p.add_argument("--comment", default="")
    a = ap.parse_args()
    {"dump": cmd_dump, "apply": cmd_apply}[a.cmd](a)


if __name__ == "__main__":
    main()
