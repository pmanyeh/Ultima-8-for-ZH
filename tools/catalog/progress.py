"""Write the translation progress into README.md and README_EN.md.

The statistics come from the PO files (as `u8catalog.py stats`) and replace
the text between the markers <!-- progress:start --> and <!-- progress:end -->.

  python tools/catalog/progress.py zh_TW
"""
import argparse
import collections
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from po_compile import parse_po  # noqa: E402
import u8catalog  # noqa: E402

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
KINDS = ["bark", "ask", "book", "scroll", "grave", "plaque", "param", "ui"]
LABELS = {
    "zh": {"bark": "台詞與物品名稱", "ask": "對話選項", "book": "書", "scroll": "捲軸",
           "grave": "墓碑", "plaque": "牌匾", "param": "句子參數", "ui": "介面文字"},
    "en": {"bark": "Lines and item names", "ask": "Conversation answers", "book": "Books",
           "scroll": "Scrolls", "grave": "Gravestones", "plaque": "Plaques",
           "param": "Sentence pieces", "ui": "Interface"},
}
# usecode classes that are not a person
CLASS_LABELS = {"EXCUTION": ("處決場景", "Execution scene"),
                "COINS": ("黑曜石幣", "Obsidian coins"),
                "GUARD1": ("城門衛兵", "Gate guard")}
MARK_START, MARK_END = "<!-- progress:start -->", "<!-- progress:end -->"


def collect(lang):
    kinds = collections.defaultdict(lambda: [0, 0, 0, 0])   # entries, done, chars, chars done
    classes = []
    for path in u8catalog.all_po_files(lang):
        total = done = 0
        for e in parse_po(path):
            if not e.msgid or e.obsolete or not e.msgctxt:
                continue
            kind = e.msgctxt.split()[0]
            ok = bool(e.msgstr) and "fuzzy" not in e.flags
            k = kinds[kind]
            k[0] += 1
            k[2] += len(e.msgid)
            total += 1
            if ok:
                k[1] += 1
                k[3] += len(e.msgid)
                done += 1
        m = re.match(r"^([0-9A-F]{4})_(.*)\.po$", os.path.basename(path))
        if m and total:
            classes.append((m.group(2), total, done))
    return kinds, classes


def names(lang):
    """lowercase English name -> Chinese, from the authority file"""
    out = {}
    for en, row in u8catalog.load_authority(lang).items():
        if row["category"] == "person" and row["translation"]:
            out[en.lower()] = row["translation"]
    return out


def bar(pct, width=20):
    n = round(pct / 100 * width)
    return "█" * n + "░" * (width - n)


def render(kinds, classes, zh_names, ui):
    L = LABELS[ui]
    entries = sum(k[0] for k in kinds.values())
    done = sum(k[1] for k in kinds.values())
    chars = sum(k[2] for k in kinds.values())
    chars_done = sum(k[3] for k in kinds.values())
    pct = 100 * chars_done / chars if chars else 0
    today = datetime.date.today().isoformat()
    out = []
    if ui == "zh":
        out.append(f"**整體進度（以英文字元計）：`{bar(pct)}` {pct:.1f}%**"
                   f"（{done:,} / {entries:,} 條，更新於 {today}）\n")
        out.append("| 類別 | 已翻譯 / 全部（條） | 英文字元 | 進度 |")
    else:
        out.append(f"**Overall (by English characters): `{bar(pct)}` {pct:.1f}%** "
                   f"({done:,} / {entries:,} entries, updated {today})\n")
        out.append("| Kind | Translated / total (entries) | English characters | Progress |")
    out.append("|---|---|---|---|")
    for kind in KINDS:
        k = kinds.get(kind)
        if not k:
            continue
        p = 100 * k[3] / k[2] if k[2] else 0
        out.append(f"| {L[kind]} | {k[1]:,} / {k[0]:,} | {k[2]:,} | {p:.1f}% |")
    complete = []
    for name, total, d in sorted(classes, key=lambda c: c[0]):
        if d == total:
            zh, en = CLASS_LABELS.get(name, (zh_names.get(name.lower()), name.capitalize()))
            complete.append((zh or name.capitalize()) if ui == "zh" else en)
    if complete:
        out.append("")
        out.append(("已完成的角色與場景：" if ui == "zh" else "Characters and scenes done: ") +
                   ("、" if ui == "zh" else ", ").join(complete))
    return "\n".join(out)


def update(path, text):
    s = open(path, encoding="utf-8").read()
    a, b = s.index(MARK_START) + len(MARK_START), s.index(MARK_END)
    s = s[:a] + "\n" + text + "\n" + s[b:]
    open(path, "w", encoding="utf-8", newline="\n").write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lang")
    a = ap.parse_args()
    kinds, classes = collect(a.lang)
    zh_names = names(a.lang)
    update(os.path.join(ROOT, "README.md"), render(kinds, classes, zh_names, "zh"))
    update(os.path.join(ROOT, "README_EN.md"), render(kinds, classes, zh_names, "en"))
    print("README.md, README_EN.md updated")


if __name__ == "__main__":
    main()
