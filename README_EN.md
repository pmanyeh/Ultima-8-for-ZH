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
**Overall (by English characters): `████████████████████` 99.8%** (6,949 / 7,000 entries, updated 2026-10-09)

| Kind | Translated / total (entries) | English characters | Progress |
|---|---|---|---|
| Lines and item names | 4,817 / 4,827 | 375,375 | 99.8% |
| Conversation answers | 1,822 / 1,863 | 36,829 | 99.8% |
| Books | 87 / 87 | 116,622 | 100.0% |
| Scrolls | 22 / 22 | 7,864 | 100.0% |
| Gravestones | 67 / 67 | 2,609 | 100.0% |
| Plaques | 63 / 63 | 1,410 | 100.0% |
| Sentence pieces | 54 / 54 | 505 | 100.0% |
| Interface | 17 / 17 | 432 | 100.0% |

Characters and scenes done: Abacus, Agware, Airfocus, Altar, Altar_ew, Amostat, Anctones, Anvil, Aorta, Apastat, Appear, Aramina, Arcadion, Armguard, Armor, Axe, Axe2, Axeblade, Backpack, Bag, Bane, Bane2, Barentry, Barrel, Basebook, Basescrl, Basket, Bathstuf, Bellows, Benchew, Bentic, Beren, Berenhch, Bgate, Bigdemst, Bigugly, Bladstrk, Blankets, Boat, Bones, Bones2, Bones3, Bones4, Book1, Bookbloo, Bookmark, Bottle, Branches, Bribook, Bribook2, Bribook3, Bribook4, Bribook5, Bribook6, Brock, Brokchar, Broken, Brokstf1, Bug, Burndout, Calguard, Campfire, Candlbra, Candle, Canopy, Canopyew, Canopytp, Cauldron, Chair, Chest_ew, Chest_ns, Child, Chimney, Chopblk, Cloth, Clothes, Clothing, Codew, Codns, Obsidian coins, Corinth, Cuffs, Cup, Cusion, Cyrrus, Daemspel, Dagger, Dagger2, Dart, Dartbord, Deadcloz, Deadew, Deadns, Deathdis, Deceiver, Demnstat, Demon, Deskew, Deskns, Deskpict, Devon, Door_ns, Dtable, Dummy, Earthmag, Ebrock, Endgate, Endgate2, Endhydro, Endlamp, Endlith, Endskul, Endstrat, Erthitem, Erthreag, Erthspel, Ethereag, Evilsorc, Ewbpaint, Ewcrops, Ewhollog, Ewlamptp, Ewshelf, Ewshfsid, Ewspaint, Execution scene, Eye, Fallrock, Fan, Febarsew, Febarsns, Fenalia, Fgrenade, Fight, Firefeld, Fireglob, Fireitem, Firepit, Fireplac, Fireplew, Fireplns, Firereag, Fireshld, Fireshro, Firespel, Fireswmp, Firewood, Fish, Fish2, Fishbonz, Fishnet, Fishpole, Flamstng, Flask, Floatin, Flour, Food, Free, Ftableew, Ftablens, Gargoyle, Gateskul, Gemofpro, Ghost, Ghosthed, Ghoul, Girlsstu, Golem, Gorgrond, Graveii, Grave_ew, Grave_ns, Greentre, Grenade, Grimoire, Gate guard, Guard10, Guard2, Guard3, Guard4, Guard5, Guard6, Guard7, Guard8, Guard9, Guardman, Guard_ew, Gwillim, Hammer, Hamostr, Hay, Helmet, Hourglas, Hydros, Intern, Ironman, Jbox, Jenna, Jewelry, Jug, Kegew, Kegns, Key, Keyonec, Keyring, Kilandra, Kingbdew, Kingbdns, Kith, Korgfang, Korick, Lamp1, Lamp2, Lamp3, Lamppost, Lava, Lavasink, Layghoul, Lchst_ew, Lchst_ns, Legging, Legs, Lever, Lithos, Litlmush, Logbook, Logbook2, Logbook3, Logbook4, Logo, Loom, Lothalt, Lothcorp, Lothlay, Mace, Mace2, Magarm, Magarmr2, Magarms, Maghelm, Maglegs, Magscrol, Magshld, Malchir, Marble, Melbook, Method, Mir, Monfast, Mordea, Mordeabe, Mordstat, Morebrok, Morefish, Morefood, Move, Mushcap, Mushgrup, Mushroom, Mythran, Nec1, Nitstand, Nsbpaint, Nscrops, Nshollog, Nslamptp, Nsrunwod, Nsshelf, Nsshfsid, Nsspaint, Nssticks, Oaktblew, Oaktblns, Odistat, Offsup, Opnbdrol, Orlok, Oven, Pedestal, Pent, Pesant1, Pesant2, Pesant3, Plaqueew, Plaquens, Platefoo, Pole, Potion, Potplant, Potspans, Protectr, Pulchnew, Pulchnns, Pyros, Rainbarl, Rat, Recall, Rhian, Rope, Sabre, Salklog, Schair, Scimitar, Scimokg, Screamer, Scroll1, Scroll2, Sgargl, Sgbook, Shaana, Shchimne, Shield, Shortmsh, Silvore, Sinking, Skeleton, Skulcand, Skullhea, Skulz, Slayer, Smalmush, Sorchat, Spelcmbt, Spider, Spiky, Spitter, Spout, Stalag, Statue, Statue1, Statuet, Stellos, Stevbook, Stmite, Stovpipe, Strathat, Stratos, Straw, Sword, Sword2, Tablware, Tallcand, Tankard, Tapestew, Tapestns, Tarna, Thurgist, Tomb, Toran, Torax, Torch, Tortchar, Tortrack, Torwin, Tossrock, Toys, Trap, Tree, Trialhat, Tring, Troll, Troodle, Troughew, Troughns, Trowel, Vanish, Vardion, Vardion2, Vase, Vivalter, Vivdagr, Vividos, Wallswit, Wardew, Wardns, Wbench, Well, Winchew, Winchns, Wool, Woundtor, Wtable, Wtableew, Wthrone, _
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
