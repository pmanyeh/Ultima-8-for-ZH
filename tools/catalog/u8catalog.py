"""U8 translation catalog maintenance: extract + merge, check, statistics.

  python u8catalog.py update <lang> [--classes 0402,040A] [--tm] [--dry-run]
      Extract the text of every usecode class from the game data and merge it
      into localization/<lang>/dialog/CCCC_NAME.po (one file per class, entries
      in conversation order). Existing translations are kept:
        - same context + English        -> translation kept
        - same call site, other English -> translation kept as fuzzy
        - --tm: same English translated elsewhere -> copied as fuzzy
        - entries no longer extracted   -> kept at the end as obsolete (#~)
      Translator comments ("# ...") and flags are kept; extracted comments
      ("#. ...") are regenerated. Repeated runs give identical files.

  python u8catalog.py check <lang> [--font Cubic_11.ttf]
      Errors: bad context, template placeholders, entries whose English is no
      longer in the game (stale), msgid outside the game code page.
      Warnings: control characters (~ * % ^ @ & tab) differ between English
      and translation, glossary terms not used, characters missing in the font.

  python u8catalog.py terms <lang>
      Update the authority file localization/<lang>/authority.tsv: candidate
      names collected from the game text (look texts of items, people and
      creatures, spell foci, recurring proper names), with a guessed category,
      count and an example. Entries edited by hand (translation, status,
      category, note) are kept. `check` uses the entries whose status is
      "approved" or "keep" (keep = stays English).

  python u8catalog.py stats <lang> [--csv report.csv]
      Translated / fuzzy / untranslated per kind and class, duplicated English
      (same text in several contexts) and inconsistent translations of it.

Game data is read-only; only localization/ is written.
"""
import argparse
import collections
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "extract"))
sys.path.insert(0, os.path.join(HERE, "..", "diagnostics"))
sys.path.insert(0, os.path.join(HERE, "..", "validate"))

import po_compile  # noqa: E402
from po_compile import parse_po, canonical_context, placeholder_error, POError  # noqa: E402

CONTROL_CHARS = "~*%^@&\t"
KIND_ORDER = ["bark", "ask", "param", "book", "scroll", "grave", "plaque", "ui"]


def lang_dir(lang):
    return os.path.join(ROOT, "localization", lang)


def po_quote(s):
    out = s.replace("\\", "\\\\").replace('"', '\\"').replace("\t", "\\t")
    if "\n" in out:
        parts = out.split("\n")
        lines = [p + "\\n" for p in parts[:-1]] + ([parts[-1]] if parts[-1] else [])
        return '""\n' + "\n".join(f'"{l}"' for l in lines)
    return f'"{out}"'


class Item:
    """One catalog entry as written by this tool."""
    def __init__(self, ctx, msgid, msgstr="", notes=(), flags=(), comments=(), previous=None):
        self.ctx, self.msgid, self.msgstr = ctx, msgid, msgstr
        self.notes = list(notes)          # extracted comments (#.)
        self.flags = sorted(set(flags))   # #, flags
        self.comments = list(comments)    # translator comments (# )
        self.previous = previous          # #| msgid of a fuzzy match

    def render(self, obsolete=False):
        lines = [f"# {c}" if c else "#" for c in self.comments]
        if not obsolete:
            lines += [f"#. {n}" for n in self.notes]
        if self.flags:
            lines.append("#, " + ", ".join(self.flags))
        if self.previous is not None and not obsolete:
            lines.append(f"#| msgid {po_quote(self.previous)}")
        body = [f"msgctxt {po_quote(self.ctx)}", f"msgid {po_quote(self.msgid)}",
                f"msgstr {po_quote(self.msgstr)}"]
        if obsolete:
            body = ["#~ " + l for b in body for l in b.split("\n")]
        return "\n".join(lines + body) + "\n"


def header_text(lang, title):
    return (f"# Ultima VIII: Pagan - translation ({lang})\n"
            f"# {title}\n"
            "#\n"
            "# Generated and merged by tools/catalog/u8catalog.py; translations are kept\n"
            "# when the file is updated. msgctxt = where the text is shown (ADR-001),\n"
            "# msgid = the exact English text (keep trailing spaces).\n"
            'msgid ""\n'
            'msgstr ""\n'
            '"Content-Type: text/plain; charset=UTF-8\\n"\n'
            '"Content-Transfer-Encoding: 8bit\\n"\n'
            f'"Language: {lang}\\n"\n')


def translator_comments(entry):
    """Comments a translator wrote: "# text" (not #. #, #| #~ #:)."""
    out = []
    for c in entry.comments:
        if c.startswith("#.") or c.startswith("#:") or c.startswith("#|"):
            continue
        if c.startswith("# ") or c == "#":
            out.append(c[2:])
    return out


# ---------------------------------------------------------------- extraction

def extract_all(classes=None):
    """{class: (name, [(ctx, msgid, notes)])} in class and flow order."""
    import u8dis
    import u8extract
    data, ents = u8dis.load_flex(u8dis.USECODE)
    names = u8dis.class_names(data, ents)
    out = {}
    for cls in range(len(ents) - 2):
        if classes is not None and cls not in classes:
            continue
        name, _, cat, _ = u8extract.extract(cls, data, ents, names)
        items, seen = [], set()
        for kind, pid, text, typ, note in cat:
            if not text:
                continue          # unresolved bark: nothing to translate
            ctx = f"{kind} {pid}"
            if (ctx, text) in seen:
                continue
            seen.add((ctx, text))
            notes = [note] if note else []
            if typ == "template":
                notes.append("sentence template: keep the {placeholders}")
            elif typ == "answer check":
                notes.append("answer compared by the conversation code")
            elif kind == "param":
                notes = [note, "parameter value inserted into sentence templates"]
            items.append((ctx, text, notes))
        if items:
            out[cls] = (name, items)
    return out


def class_file(lang, cls, name):
    safe = re.sub(r"[^A-Za-z0-9_]", "_", name)
    return os.path.join(lang_dir(lang), "dialog", f"{cls:04X}_{safe}.po")


def existing_class_files(lang):
    d = os.path.join(lang_dir(lang), "dialog")
    out = {}
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            m = re.match(r"^([0-9A-Fa-f]{4})_.*\.po$", fn)
            if m:
                out[int(m.group(1), 16)] = os.path.join(d, fn)
    return out


def load_entries(path):
    """Non-header entries of a PO file (obsolete ones included)."""
    return [e for e in parse_po(path) if not (e.msgid == "" and e.msgctxt is None)]


def translation_memory(lang):
    tm = {}
    for path in all_po_files(lang):
        for e in load_entries(path):
            if e.msgstr and "fuzzy" not in e.flags and not e.obsolete:
                tm.setdefault(e.msgid, e.msgstr)
    return tm


def merge(lang, cls, name, items, old_path, tm):
    old = load_entries(old_path) if old_path and os.path.exists(old_path) else []
    by_key, by_ctx = {}, collections.defaultdict(list)
    for e in old:
        ctx = canonical_context(e.msgctxt) or e.msgctxt
        by_key[(ctx, e.msgid)] = e
        by_ctx[ctx].append(e)

    used = set()
    out = []
    stats = collections.Counter()
    for ctx, msgid, notes in items:
        e = by_key.get((ctx, msgid))
        if e is not None:
            used.add(id(e))
            flags = [f for f in e.flags if f == "fuzzy"]
            out.append(Item(ctx, msgid, e.msgstr, notes, flags, translator_comments(e)))
            stats["kept" if e.msgstr else "new"] += 1
            continue
        # same call site, changed English: keep the translation for review
        cand = None
        if not ctx.startswith("ask ") and not ctx.startswith("param "):
            cand = next((x for x in by_ctx.get(ctx, []) if x.msgstr and id(x) not in used), None)
        if cand is not None:
            used.add(id(cand))
            out.append(Item(ctx, msgid, cand.msgstr, notes, ["fuzzy"], translator_comments(cand),
                            previous=cand.msgid))
            stats["fuzzy-changed"] += 1
            continue
        if tm is not None and msgid in tm:
            out.append(Item(ctx, msgid, tm[msgid], notes + ["translation memory: same English elsewhere"],
                            ["fuzzy"]))
            stats["fuzzy-tm"] += 1
            continue
        out.append(Item(ctx, msgid, "", notes))
        stats["new"] += 1

    obsolete = []
    for e in old:
        if id(e) in used or not e.msgstr:
            continue
        ctx = canonical_context(e.msgctxt) or e.msgctxt
        obsolete.append(Item(ctx, e.msgid, e.msgstr, (), e.flags, translator_comments(e)))
        stats["obsolete"] += 1

    text = header_text(lang, f"{name} (usecode class {cls:04X})")
    for it in out:
        text += "\n" + it.render()
    for it in obsolete:
        text += "\n" + it.render(obsolete=True)
    return text, stats


def cmd_update(a):
    classes = None
    if a.classes:
        classes = {int(c, 16) for c in a.classes.split(",")}
    print("extracting usecode text ...", file=sys.stderr)
    extracted = extract_all(classes)
    existing = existing_class_files(a.lang)
    tm = translation_memory(a.lang) if a.tm else None
    total = collections.Counter()
    written = 0
    for cls, (name, items) in sorted(extracted.items()):
        old_path = existing.get(cls)
        new_path = class_file(a.lang, cls, name)
        text, stats = merge(a.lang, cls, name, items, old_path, tm)
        total.update(stats)
        total["entries"] += len(items)
        if a.dry_run:
            continue
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        old_text = open(old_path, encoding="utf-8").read() if old_path and os.path.exists(old_path) else None
        if old_path and old_path != new_path:
            os.remove(old_path)
        if text != old_text or old_path != new_path:
            with open(new_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            written += 1
    # classes that no longer have text keep their file (translations are not lost)
    print(f"classes with text: {len(extracted)}, files written: {written}, "
          f"entries: {total['entries']}, translations kept: {total['kept']}, "
          f"fuzzy (changed English): {total['fuzzy-changed']}, fuzzy (memory): {total['fuzzy-tm']}, "
          f"obsolete: {total['obsolete']}" + (" (dry run)" if a.dry_run else ""))


# ---------------------------------------------------------------- checking

def all_po_files(lang):
    out = []
    for root, _, files in os.walk(lang_dir(lang)):
        out += [os.path.join(root, f) for f in files if f.endswith(".po")]
    return sorted(out)


AUTHORITY_COLUMNS = ["category", "english", "translation", "status", "count", "example", "note", "annotate"]
CATEGORIES = ["person", "place", "item", "spell", "creature", "title", "faction", "other"]
STATUSES = ["keep", "approved", "proposed", "todo", "ignore"]


def authority_path(lang):
    return os.path.join(lang_dir(lang), "authority.tsv")


def load_authority(lang):
    """{english: row dict} from the authority file (comments skipped)."""
    rows = {}
    path = authority_path(lang)
    if not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or line.startswith("category\t"):
            continue
        cols = (line.split("\t") + [""] * len(AUTHORITY_COLUMNS))[:len(AUTHORITY_COLUMNS)]
        row = dict(zip(AUTHORITY_COLUMNS, cols))
        if row["english"]:
            rows[row["english"]] = row
    return rows


def load_glossary(lang):
    """(english, translation) pairs that translations must follow."""
    terms = []
    for en, row in load_authority(lang).items():
        if row["status"] == "keep":
            terms.append((en, row["translation"] or en))
        elif row["status"] == "approved" and row["translation"]:
            terms.append((en, row["translation"]))
    return terms


# words that start sentences or are capitalised for other reasons
COMMON_WORDS = set("""I A An The And But Or Nor So Yet For If Then Than When While Where Why How What Who Whom
Whose Which This That These Those There Here It Its He She We You They Me Him Her Us Them My Your His Our Their
Aye Nay Yes No Not Oh Ah Well Now Perhaps Indeed Alas Hail Farewell Greetings Hello Goodbye Good Thank Thanks
Please Sorry Come Go Let Do Does Did Is Are Was Were Be Been Am Have Has Had Will Would Shall Should Can Could
May Might Must Ye Thee Thou Thy Thine Tis Twas Mr Sir Lady Lord My Mine Some Any All None One Two Three Each
Every Many Much More Most Only Even Just Also Still Yet Again Once After Before Since Until Unless Though Although
With Without Within Into Onto Upon From To In On At By Of Off Out Over Under About Above Below Between Through
Hey Hmm Ha Bah Ugh Eh Huh Please Don't I'm I'll I've I'd It's That's What's There's You're You'll Let's""".split())


def guess_category(text, cls_name, cls):
    t = text.strip()
    if t.endswith(" focus"):
        return "spell"
    if 0x400 <= cls < 0x500:          # NPC classes
        return "person" if t[:1].isupper() else "title"
    return "item"


def collect_terms():
    """{english: (category, count, example context)}"""
    import u8dis
    import u8extract
    data, ents = u8dis.load_flex(u8dis.USECODE)
    names = u8dis.class_names(data, ents)
    found = {}
    counts = collections.Counter()
    proper = collections.Counter()
    examples = {}
    texts = []
    for cls in range(len(ents) - 2):
        name, _, cat, _ = u8extract.extract(cls, data, ents, names)
        for kind, pid, text, typ, note in cat:
            if not text:
                continue
            ctx = f"{kind} {pid}"
            texts.append((ctx, text))
            # look texts: names of items, people, creatures
            if kind == "bark" and note.startswith("event 00") and typ == "literal":
                t = text.strip()
                # messages, not names
                if not (1 < len(t) <= 40) or any(ch in t for ch in "!?:()") or "." in t[:-1]:
                    continue
                t = t.rstrip(".")
                if 0x400 <= cls < 0x500:
                    # NPC classes: a name ("Bentic the Librarian", "Darion, Captain
                    # of the Guard" -> the name) or a short role ("librarian")
                    if "," in t:
                        t = t.split(",")[0].strip()
                    elif re.match(r"^[A-Z][a-z]+ the ", t):
                        t = t.split(" ")[0]
                    words = t.split()
                    if len(words) > 3:
                        continue
                    if t[:1].isupper() and not all(w[:1].isupper() for w in words if w not in ("of", "the")):
                        continue          # a message, not a name
                counts[t] += 1
                found.setdefault(t, (guess_category(t, name, cls), ctx))
                if t.endswith(" focus"):
                    spell = t[:-len(" focus")]
                    counts[spell] += 1
                    found.setdefault(spell, ("spell", ctx))
    # recurring capitalised names in all text (not at the start of a sentence)
    name_re = re.compile(r"(?<![.!?~*\"'] )(?<!^)\b([A-Z][a-z][A-Za-z']*(?:(?: of(?: the)?| the)? [A-Z][a-z][A-Za-z']*)*)")
    for ctx, text in texts:
        for sentence in re.split(r"(?<=[.!?~*])\s+", text):
            for m in name_re.finditer(sentence):
                if m.start() == 0:
                    continue
                term = m.group(1)
                words = term.split()
                if all(w in COMMON_WORDS for w in words if w[0].isupper()):
                    continue
                if words[0] in COMMON_WORDS:
                    term = " ".join(words[1:])
                    if not term or not term[0].isupper():
                        continue
                term = re.sub(r"'s?$", "", term)        # possessive: Orlok's, Pyros'
                if not term or term in COMMON_WORDS:
                    continue
                proper[term] += 1
                examples.setdefault(term, ctx)
    for term, n in proper.items():
        if n >= 3 and term not in found:
            found[term] = ("other", examples[term])
        if term in found:
            counts[term] += n
    return {t: (cat, counts[t], ctx) for t, (cat, ctx) in found.items()}


def cmd_terms(a):
    print("collecting names from the game text ...", file=sys.stderr)
    collected = collect_terms()
    old = load_authority(a.lang)
    rows = []
    for en in sorted(set(collected) | set(old), key=lambda x: x.lower()):
        o = old.get(en)
        c = collected.get(en)
        row = {k: "" for k in AUTHORITY_COLUMNS}
        row["english"] = en
        if c:
            row["category"], row["count"], row["example"] = c[0], str(c[1]), c[2]
        if o:
            # hand-edited fields win; counts and examples are refreshed
            for k in ("category", "translation", "status", "note", "annotate"):
                if o[k]:
                    row[k] = o[k]
            if not c:
                row["count"], row["example"] = "0", o["example"]
        row["status"] = row["status"] or "todo"
        rows.append(row)
    rows.sort(key=lambda r: (CATEGORIES.index(r["category"]) if r["category"] in CATEGORIES else 99,
                             r["english"].lower(), r["english"]))
    path = authority_path(a.lang)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Ultima VIII: Pagan - authority file (names and terms), tab separated\n"
                "# Generated by: python tools/catalog/u8catalog.py terms <lang>  (hand edits are kept)\n"
                "#\n"
                "# category    person, place, item, spell, creature, title, faction, other\n"
                "#             (guessed for new entries: please check)\n"
                "# translation the one translation to use everywhere\n"
                "# status      keep = stays English, approved = use translation,\n"
                "#             proposed = suggestion, todo = not decided,\n"
                "#             ignore = not a name (a capitalised word at the start of a sentence)\n"
                "# count       occurrences in the game text, example = one context\n"
                "# annotate    the first time the name is shown in a conversation (or book), the\n"
                "#             game adds the English: \u4e0d\u5217\u985b\u5c3c\u4e9e(Britannia). yes / no; empty = yes for\n"
                "#             person, place and faction, no for the other categories\n"
                "# `u8catalog.py check` warns when an approved / keep term is not used.\n")
        f.write("\t".join(AUTHORITY_COLUMNS) + "\n")
        for r in rows:
            f.write("\t".join(r[k] for k in AUTHORITY_COLUMNS) + "\n")
    by_cat = collections.Counter(r["category"] for r in rows)
    by_status = collections.Counter(r["status"] for r in rows)
    print(f"{path}: {len(rows)} terms; " + ", ".join(f"{k} {v}" for k, v in sorted(by_cat.items())) +
          "; status " + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())))


def cmd_check(a):
    errors, warnings = [], []
    current = None
    if not a.no_stale:
        print("extracting usecode text for the stale check ...", file=sys.stderr)
        current = {(ctx, msgid) for _, items in extract_all().values() for ctx, msgid, _ in items}
    glossary = load_glossary(a.lang)
    cmap = None
    if a.font:
        import font_coverage
        cmap = font_coverage.read_cmap(a.font)
    missing_chars = collections.Counter()

    for path in all_po_files(a.lang):
        rel = os.path.relpath(path, ROOT)
        try:
            entries = load_entries(path)
        except POError as ex:
            errors.append(str(ex))
            continue
        for e in entries:
            if e.obsolete:
                continue
            where = f"{rel}:{e.line}"
            ctx = canonical_context(e.msgctxt)
            if ctx is None:
                errors.append(f"{where}: unknown msgctxt {e.msgctxt!r}")
                continue
            try:
                e.msgid.encode(po_compile.GAME_ENCODING)
            except UnicodeEncodeError:
                errors.append(f"{where}: msgid not representable in the game code page")
            if current is not None and ctx != "ui" and (ctx, e.msgid) not in current:
                errors.append(f"{where}: stale: {ctx} {e.msgid[:50]!r} is not in the game text")
            if not e.msgstr:
                continue
            if ctx.startswith("bark ") and "{" in e.msgid + e.msgstr:
                err = placeholder_error(e.msgid, e.msgstr)
                if err:
                    errors.append(f"{where}: {err}")
            for ch in CONTROL_CHARS:
                # gravestones and plaques: the translation is a subtitle, its
                # line breaks need not follow the engraving
                if ch == "*" and (ctx.startswith("grave ") or ctx.startswith("plaque ") or ctx == "ui"):
                    continue
                if e.msgid.count(ch) != e.msgstr.count(ch):
                    name = {"\t": "tab"}.get(ch, ch)
                    warnings.append(f"{where}: control character {name!r}: English {e.msgid.count(ch)}, "
                                    f"translation {e.msgstr.count(ch)}")
            for en, zh in glossary:
                if re.search(r"(?<![A-Za-z])" + re.escape(en) + r"(?![A-Za-z])", e.msgid) and zh not in e.msgstr:
                    warnings.append(f"{where}: glossary: {en!r} -> {zh!r} not used")
            if cmap is not None:
                for ch in e.msgstr:
                    if ord(ch) > 127 and ord(ch) not in cmap:
                        missing_chars[ch] += 1

    for ch, n in sorted(missing_chars.items()):
        warnings.append(f"font: character {ch!r} (U+{ord(ch):04X}) missing, used {n} times")
    for w in warnings:
        print("WARNING:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


# ---------------------------------------------------------------- statistics

def cmd_stats(a):
    per_kind = collections.defaultdict(collections.Counter)
    per_file = []
    by_english = collections.defaultdict(list)
    for path in all_po_files(a.lang):
        rel = os.path.relpath(path, lang_dir(a.lang)).replace(os.sep, "/")
        c = collections.Counter()
        for e in load_entries(path):
            if e.obsolete:
                c["obsolete"] += 1
                continue
            ctx = canonical_context(e.msgctxt) or "?"
            kind = ctx.split(" ")[0]
            state = "fuzzy" if "fuzzy" in e.flags else ("translated" if e.msgstr else "untranslated")
            per_kind[kind][state] += 1
            per_kind[kind]["chars"] += len(e.msgid)
            if state == "translated":
                per_kind[kind]["chars_done"] += len(e.msgid)
            c[state] += 1
            c["total"] += 1
            by_english[e.msgid].append((ctx, e.msgstr if state == "translated" else "", rel))
        per_file.append((rel, c))

    print(f"{'kind':8} {'total':>7} {'done':>7} {'fuzzy':>6} {'todo':>7} {'chars':>9} {'done %':>7}")
    tot = collections.Counter()
    for kind in KIND_ORDER + sorted(set(per_kind) - set(KIND_ORDER)):
        c = per_kind.get(kind)
        if not c:
            continue
        total = c["translated"] + c["fuzzy"] + c["untranslated"]
        tot.update(c)
        pct = 100.0 * c["chars_done"] / c["chars"] if c["chars"] else 0
        print(f"{kind:8} {total:7} {c['translated']:7} {c['fuzzy']:6} {c['untranslated']:7} "
              f"{c['chars']:9} {pct:6.1f}%")
    total = tot["translated"] + tot["fuzzy"] + tot["untranslated"]
    pct = 100.0 * tot["chars_done"] / tot["chars"] if tot["chars"] else 0
    print(f"{'all':8} {total:7} {tot['translated']:7} {tot['fuzzy']:6} {tot['untranslated']:7} "
          f"{tot['chars']:9} {pct:6.1f}%   (by English characters)")

    dup = {en: v for en, v in by_english.items() if len(v) > 1}
    inconsistent = {en: v for en, v in dup.items() if len({t for _, t, _ in v if t}) > 1}
    partial = {en: v for en, v in dup.items() if any(t for _, t, _ in v) and not all(t for _, t, _ in v)}
    print(f"\nsame English in several contexts: {len(dup)} texts, "
          f"{sum(len(v) for v in dup.values())} entries")
    print(f"  translated differently: {len(inconsistent)}; translated only in some contexts: {len(partial)}")
    for en, v in list(inconsistent.items())[:a.show]:
        print(f"  ~ {en[:60]!r}: " + " | ".join(f"{ctx}={t}" for ctx, t, _ in v if t))
    for en, v in list(partial.items())[:a.show]:
        print(f"  + {en[:60]!r}: untranslated in " + ", ".join(ctx for ctx, t, _ in v if not t))

    if a.csv:
        with open(a.csv, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["file", "total", "translated", "fuzzy", "untranslated", "obsolete"])
            for rel, c in per_file:
                w.writerow([rel, c["total"], c["translated"], c["fuzzy"], c["untranslated"], c["obsolete"]])
        print(f"\nper-file report: {a.csv}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("update")
    u.add_argument("lang")
    u.add_argument("--classes", help="comma separated hex class numbers (default: all)")
    u.add_argument("--tm", action="store_true", help="fill new entries from identical English (fuzzy)")
    u.add_argument("--dry-run", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("lang")
    c.add_argument("--font", help="TTF/OTF to check the characters against")
    c.add_argument("--no-stale", action="store_true", help="skip the comparison with the game text")
    t = sub.add_parser("terms")
    t.add_argument("lang")
    s = sub.add_parser("stats")
    s.add_argument("lang")
    s.add_argument("--csv")
    s.add_argument("--show", type=int, default=10)
    a = ap.parse_args()
    {"update": cmd_update, "check": cmd_check, "stats": cmd_stats, "terms": cmd_terms}[a.cmd](a)


if __name__ == "__main__":
    main()
