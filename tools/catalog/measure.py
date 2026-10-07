"""Summarize the page / size measurement of the translations.

The engine lays out every catalog entry with the real fonts and text box sizes
when started with localization_measure=true and writes one log line per entry
(Localization::measureCatalog):

  [U8-L10N] measure <TAB> context <TAB> pagesEN <TAB> pagesL10N <TAB> wEN <TAB> hEN
                   <TAB> wL10N <TAB> hL10N <TAB> readEN <TAB> readL10N <TAB> source

Run it (closes the game again by itself):

  copy private_test/scummvm-dev.ini, add "localization_measure=true" under [ultima8]
  powershell tools/automation/startup_check.ps1 -Config <that ini> -Seconds 40 -Log measure.log
  python tools/catalog/measure.py measure.log [--csv out.csv]

Reported:
  - per kind: entries, pages English / translated, reading length ratio
    (readingLength(): a CJK character counts 3 letters, as the bark timing does)
  - entries that need more pages than the English text (bark, book, scroll)
  - answers wider than 160 px (AskGump puts the next answer on a new row)
  - gravestone / plaque subtitles wider than the screen (320 px)
"""
import argparse
import collections
import csv
import sys

ASK_ROW_WIDTH = 160
SCREEN_WIDTH = 320
FIELDS = ["context", "pagesEN", "pagesL10N", "wEN", "hEN", "wL10N", "hL10N",
          "readEN", "readL10N", "source"]


def read_log(paths):
    rows = []
    for path in paths:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if "[U8-L10N] measure\t" not in line:
                    continue
                parts = line.rstrip("\n").split("[U8-L10N] measure\t", 1)[1].split("\t")
                if parts[0] == "context" or len(parts) < len(FIELDS):
                    continue
                r = dict(zip(FIELDS, parts[:len(FIELDS) - 1] + ["\t".join(parts[len(FIELDS) - 1:])]))
                for k in FIELDS[1:-1]:
                    r[k] = int(r[k])
                r["kind"] = r["context"].split()[0]
                rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("log", nargs="+")
    ap.add_argument("--csv")
    a = ap.parse_args()
    rows = read_log(a.log)
    if not rows:
        sys.exit("no measure lines found (was localization_measure=true set?)")

    print(f"{'kind':8} {'entries':>7} {'pagesEN':>8} {'pagesZH':>8} {'more':>5} {'fewer':>6} "
          f"{'readEN':>7} {'readZH':>7} {'ratio':>6}")
    by_kind = collections.defaultdict(list)
    for r in rows:
        by_kind[r["kind"]].append(r)
    for kind in ["bark", "ask", "book", "scroll", "grave", "plaque"]:
        rs = by_kind.get(kind)
        if not rs:
            continue
        pe = sum(r["pagesEN"] for r in rs)
        pz = sum(r["pagesL10N"] for r in rs)
        more = sum(r["pagesL10N"] > r["pagesEN"] for r in rs if r["pagesEN"])
        fewer = sum(r["pagesL10N"] < r["pagesEN"] for r in rs)
        re_, rz = sum(r["readEN"] for r in rs), sum(r["readL10N"] for r in rs)
        print(f"{kind:8} {len(rs):7} {pe:8} {pz:8} {more:5} {fewer:6} {re_:7} {rz:7} "
              f"{rz / re_ if re_ else 0:6.2f}")

    def show(title, items):
        print(f"\n{title}: {len(items)}")
        for r, extra in items:
            print(f"  {r['context']:18} {extra:24} {r['source'][:60]}")

    show("more pages than English",
         [(r, f"pages {r['pagesEN']} -> {r['pagesL10N']}") for r in rows
          if r["kind"] in ("bark", "book", "scroll") and r["pagesL10N"] > r["pagesEN"]])
    show(f"answers wider than {ASK_ROW_WIDTH} px",
         [(r, f"width {r['wEN']} -> {r['wL10N']}") for r in rows
          if r["kind"] == "ask" and r["wL10N"] > ASK_ROW_WIDTH])
    show(f"subtitles wider than {SCREEN_WIDTH} px",
         [(r, f"width {r['wL10N']}") for r in rows
          if r["kind"] in ("grave", "plaque") and r["wL10N"] > SCREEN_WIDTH])

    if a.csv:
        with open(a.csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["kind"] + FIELDS)
            w.writeheader()
            for r in sorted(rows, key=lambda r: r["context"]):
                w.writerow(r)


if __name__ == "__main__":
    main()
