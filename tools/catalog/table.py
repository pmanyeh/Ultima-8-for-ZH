"""Helpers for translating a batch.py dump with a table of distinct sentences.

  python table.py prefill <dump>
      fill the empty "> " lines with the translation of the same English found
      anywhere in the PO files (except yes / no answers, whose meaning depends
      on the question); apply the dump afterwards so only new text is left

  python table.py view <dump>
      each untranslated English text once, in conversation order: [B] bark,
      [A] answer, [P] parameter value, "-- after ..." when the answer changes

  python table.py fill <dump> <table> <out>
      write translation blocks for every untranslated entry of the dump found
      in the table; the table has one "English ||| 中文" per line (spacing in
      the English does not matter); "@<msgctxt> English ||| 中文" limits a row
      to one context. Lists the entries the table misses.

Workflow: batch.py dump > d.txt; table.py prefill d.txt; batch.py apply d.txt;
batch.py dump > d.txt; table.py view d.txt; write the table;
table.py fill d.txt t.tsv out.txt; batch.py apply out.txt --comment ...
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from po_compile import parse_po  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def norm(s):
    return " ".join(s.split())


def entries(path):
    """(msgctxt, English, translation, note lines) of a dump, in order"""
    ctx = en = None
    notes = []
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("# "):
            notes.append(line[2:])
        elif line.startswith("@ "):
            ctx = line[2:]
        elif line.startswith("< "):
            en = line[2:]
        elif line.startswith(">"):
            yield ctx, en, line[1:].strip(), notes
            notes = []


def cmd_prefill(dump):
    tm = {}
    for p in glob.glob(os.path.join(ROOT, "localization", "*", "**", "*.po"), recursive=True):
        for e in parse_po(p):
            if e.msgid and e.msgstr and not e.obsolete:
                tm.setdefault(norm(e.msgid), e.msgstr)
    lines = open(dump, encoding="utf-8").read().split("\n")
    en, n = None, 0
    for i, line in enumerate(lines):
        if line.startswith("< "):
            en = norm(line[2:])
        elif line.rstrip() == ">" and en in tm and en.lower().strip(".!? ") not in ("yes", "no"):
            lines[i] = "> " + tm[en]
            n += 1
    open(dump, "w", encoding="utf-8").write("\n".join(lines))
    print("prefilled", n)


def cmd_view(dump):
    seen, after = set(), None
    for ctx, en, zh, notes in entries(dump):
        if zh or norm(en) in seen:
            continue
        seen.add(norm(en))
        ev = next((x for x in notes if x.startswith("event")), "")
        a = ev.split("after ", 1)[1] if "after " in ev else ""
        if a != after:
            after = a
            print(f"  -- after {a[:60]}" if a else "  --")
        kind = {"ask": "A", "param": "P"}.get(ctx.split()[0], "B")
        print(f"[{kind}] {norm(en)}")


def cmd_fill(dump, table, out):
    rows, ctx_rows = {}, {}
    for line in open(table, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        en, zh = (x.strip() for x in line.split("|||"))
        if en.startswith("@"):
            kind, cid, en = en[1:].split(" ", 2)
            ctx_rows[(f"{kind} {cid}", norm(en))] = zh
        else:
            rows[norm(en)] = zh
    blocks, missing = [], []
    for ctx, en, zh, _ in entries(dump):
        if zh:
            continue
        t = ctx_rows.get((ctx, norm(en)), rows.get(norm(en)))
        if t is None:
            missing.append(f"{ctx} | {en}")
        else:
            blocks.append(f"@ {ctx}\n< {en}\n> {t}\n")
    open(out, "w", encoding="utf-8").write("\n".join(blocks))
    print(len(blocks), "blocks;", len(missing), "missing")
    for m in missing:
        print("  MISSING", m)


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("prefill", "view", "fill"):
        sys.exit(__doc__)
    {"prefill": cmd_prefill, "view": cmd_view, "fill": cmd_fill}[sys.argv[1]](*sys.argv[2:])


if __name__ == "__main__":
    main()
