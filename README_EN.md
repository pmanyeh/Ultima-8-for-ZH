# Ultima VIII: Pagan — Traditional Chinese Translation

[正體中文](README.md)

A fan project to play *Ultima VIII: Pagan* in **Traditional Chinese**. It builds on the Ultima 8 engine of [ScummVM](https://www.scummvm.org/) and shows conversations, answers, books, scrolls, gravestones and the interface in Chinese — without modifying the original game data.

> **Status: in development, no release yet.** The technical architecture is complete and verified in game (Phases 0–12); the full translation is in progress.

## Features

- **Game data untouched**: the game logic always runs on the original English strings; text is replaced only when it is drawn. Conversation branches, speech and savegames work exactly as in the original.
- **Savegames stay English**: saves made in Chinese and English mode are interchangeable; you can switch back to the original at any time.
- **Complete conversations**: lines, answers (choosing a Chinese answer takes the original branch), books, scrolls, gravestones, plaques, main menu and journal.
- **Names with the English original**: the first time a name appears in a conversation, the English is added, e.g. 不列顛尼亞(Britannia), so players can relate it to the original game and walkthroughs.
- **Dynamic sentences**: sentences built from the player's name, quantities or item kinds (e.g. "50 piles of wood", "wand of ignite with 3 uses remaining") are translated correctly.
- **Speech and subtitles**: speaking characters keep their English voice with Chinese subtitles, pages follow the speech.
- **Chinese font**: the [Cubic 11](https://github.com/ACh-K/Cubic-11) pixel font (SIL OFL 1.1), close to the look of the original; Chinese line breaking and punctuation rules.
- **Safe fallback**: a missing translation, a broken catalog or a missing font always shows the English text — never garbage or a crash.

## Translation progress

<!-- progress:start -->
**Overall (by English characters): `██████░░░░░░░░░░░░░░` 30.7%** (2,244 / 6,944 entries, updated 2026-10-08)

| Kind | Translated / total (entries) | English characters | Progress |
|---|---|---|---|
| Lines and item names | 1,551 / 4,828 | 375,387 | 40.6% |
| Conversation answers | 662 / 1,811 | 35,841 | 35.8% |
| Books | 1 / 87 | 116,622 | 0.2% |
| Scrolls | 1 / 22 | 7,864 | 1.0% |
| Gravestones | 2 / 67 | 2,609 | 1.1% |
| Plaques | 2 / 63 | 1,410 | 2.3% |
| Sentence pieces | 13 / 54 | 505 | 23.8% |
| Interface | 12 / 12 | 152 | 100.0% |

Characters and scenes done: Aramina, Basket, Bentic, Obsidian coins, Devon, Execution scene, Fight, Food, Gate guard, Guard10, Guard2, Guard3, Guard4, Guard5, Guard6, Guard7, Guard8, Guard9, Guardman, Guard_ew, Jenna, Kilandra, Korick, Mordea, Morefish, Orlok, Rhian, Shaana, Tarna, Toran, Winchns
<!-- progress:end -->

The translation follows the story: the first batch is the opening (Devon → the execution on the docks of Tenebrae). Names and terms are kept consistent in the [authority file](localization/zh_TW/authority.tsv).

## How it works

```text
game (usecode) ── English strings ──▶ dialogue, comparisons, speech, saves (all stay English)
                        │
                        ▼ only when a text widget is created
          catalog lookup (gettext MO): call site + English text → Chinese
                        │
                        ▼
                Chinese on screen (CJK font)
```

- Every line is identified by its usecode class and call site, every answer by class and English text. A translation is shown only when the English matches exactly, so it can never appear in the wrong place.
- Translations are PO files, one per usecode class (`localization/zh_TW/dialog/`), in conversation order; edit them with Poedit or any text editor.
- Design: [Master Plan](ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md) and [docs/architecture](docs/architecture/); implementation and verification of each phase: [docs/reports](docs/reports/) (in Chinese).

## Repository layout

| Path | Contents |
|---|---|
| `localization/zh_TW/dialog/` | Translation files (394, one per usecode class) |
| `localization/zh_TW/authority.tsv` | Authority file: the one translation of every name and term |
| `localization/README.md` | Guide for translators (format, symbols to keep, workflow) |
| `tools/extract/` | Text extraction from the game data (conversation flow and branches) |
| `tools/catalog/` | Merge, check, statistics, compile, translation batches |
| `tools/validate/`, `tools/automation/` | Font coverage, savegame checks, save/load matrix, startup regression |
| `tools/diagnostics/` | Usecode disassembler and other research tools |
| `docs/` | Plan, architecture decisions (ADR), phase reports |

## What you need

- **Your own legal copy of Ultima VIII** (e.g. the GOG *Ultima VIII Gold Edition*, English). This repository contains **no** game data files, music, speech or savegames.
- The modified ScummVM: the engine changes are on the [`ultima8-zh-tw-dev` branch of pmanyeh/scummvm](https://github.com/pmanyeh/scummvm/tree/ultima8-zh-tw-dev) (GPL, source available). For now you have to build it yourself; ready-made builds and installation instructions will follow.

## Contributing translations

See [localization/README.md](localization/README.md) (in Chinese) for the file format, the symbols to keep, and how to check and compile.

```bash
python tools/catalog/u8catalog.py check zh_TW      # check translations
python tools/catalog/u8catalog.py stats zh_TW      # statistics
python tools/catalog/progress.py zh_TW             # update the progress on this page
```

## Copyright and license

- *Ultima VIII: Pagan* and its text are copyright of their owners (Origin Systems / Electronic Arts). The English text kept in the translation files is quoted for reference while translating.
- The Cubic 11 font is licensed under the SIL Open Font License 1.1.
- The license of this project will be decided before the first release.

## Thanks

- [ScummVM](https://www.scummvm.org/) and the Pentagram team for the Ultima 8 engine
- [Cubic 11](https://github.com/ACh-K/Cubic-11)
- All Ultima fans
