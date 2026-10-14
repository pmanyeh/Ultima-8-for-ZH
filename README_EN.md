# Ultima VIII: Pagan — Traditional Chinese Translation

[正體中文](README.md)

A fan project to play *Ultima VIII: Pagan* in **Traditional Chinese**. It builds on the Ultima 8 engine of [ScummVM](https://www.scummvm.org/) and shows conversations, answers, books, scrolls, gravestones and the interface in Chinese — without modifying the original game data.

> **Status: version 1.0.3.** The whole game is translated (99.8%). Ready-to-run packages for Windows and macOS (Apple Silicon and Intel) are available, see [Download and install](#download-and-install).

## Features

- **Game data untouched**: the game logic always runs on the original English strings; text is replaced only when it is drawn. Conversation branches, speech and savegames work exactly as in the original.
- **Savegames stay English**: saves made in Chinese and English mode are interchangeable; you can switch back to the original at any time.
- **Complete conversations**: lines, answers (choosing a Chinese answer takes the original branch), books, scrolls, gravestones, plaques, main menu and journal.
- **Names with the English original**: the first time a name appears in a conversation, the English is added, e.g. 不列顛尼亞(Britannia), so players can relate it to the original game and walkthroughs.
- **Dynamic sentences**: sentences built from the player's name, quantities or item kinds (e.g. "50 piles of wood", "wand of ignite with 3 uses remaining") are translated correctly.
- **Speech and subtitles**: speaking characters keep their English voice with Chinese subtitles, pages follow the speech.
- **Chinese font**: the [Cubic 11](https://github.com/ACh-K/Cubic-11) pixel font (SIL OFL 1.1), close to the look of the original; Chinese line breaking and punctuation rules.
- **High-resolution Chinese text**: the game keeps its original 320×200 picture, while the Chinese text is drawn at the window resolution in [jf open huninn](https://justfont.com/huninn/), which also makes room for a Chinese status panel (on by default, can be turned off in the game options).
- **Engravings in Chinese**: gravestones, plaques and the death screen are engraved in Chinese ([Wang Han Zong](https://code.google.com/archive/p/wangfonts/) Weibei font with an engraved shadow); English engravings with Chinese subtitles are an option.
- **Quick action icons**: icons in the bottom right corner, shown when the mouse is there (as in Exult), for the backpack, inventory, map, menu, saving and loading, combat, keyring and recall.
- **Walk to use**: double-clicking a door, chest or book out of reach makes the Avatar walk there and use it.
- **Conversations and windows**: in a conversation a click anywhere turns the page (as in Ultima VII); Escape closes the frontmost container or inventory before it opens the menu.
- **Play and combat assists**: targeted jumps land on the middle of the target; in combat a double click on an enemy turns the Avatar to him and strikes; damage numbers (with Blocked and Miss) and enemy health bars; potions named by their effect. Each can be turned off on the Chinese settings page.
- **Settings**: font, size, spacing, the size of the speech bubbles and the music device (General MIDI, AdLib, Roland MT-32) can be adjusted; the common ones on a Chinese settings page of the game options (popups and sliders), and the ScummVM interface is in Traditional Chinese.
- **Safe fallback**: a missing translation, a broken catalog or a missing font always shows the English text — never garbage or a crash.

## Translation progress

<!-- progress:start -->
**Overall (by English characters): `████████████████████` 99.8%** (6,986 / 7,035 entries, updated 2026-10-14)

| Kind | Translated / total (entries) | English characters | Progress |
|---|---|---|---|
| Lines and item names | 4,827 / 4,835 | 375,445 | 99.8% |
| Conversation answers | 1,822 / 1,863 | 36,829 | 99.8% |
| Books | 87 / 87 | 116,622 | 100.0% |
| Scrolls | 22 / 22 | 7,864 | 100.0% |
| Gravestones | 67 / 67 | 2,609 | 100.0% |
| Plaques | 63 / 63 | 1,410 | 100.0% |
| Sentence pieces | 60 / 60 | 544 | 100.0% |
| Interface | 38 / 38 | 564 | 100.0% |

Characters and scenes done: Abacus, Agware, Airfocus, Altar, Altar_ew, Amostat, Anctones, Anvil, Aorta, Apastat, Appear, Aramina, Arcadion, Armguard, Armor, Axe, Axe2, Axeblade, Backpack, Bag, Bane, Bane2, Barentry, Barrel, Basebook, Basescrl, Basket, Bathstuf, Bellows, Benchew, Bentic, Beren, Berenhch, Bgate, Bigdemst, Bigugly, Bladstrk, Blankets, Boat, Bones, Bones2, Bones3, Bones4, Book1, Bookbloo, Bookmark, Bottle, Branches, Bribook, Bribook2, Bribook3, Bribook4, Bribook5, Bribook6, Brock, Brokchar, Broken, Brokstf1, Bug, Burndout, Calguard, Campfire, Candlbra, Candle, Canopy, Canopyew, Canopytp, Cauldron, Chair, Chest_ew, Chest_ns, Child, Chimney, Chopblk, Cloth, Clothes, Clothing, Codew, Codns, Obsidian coins, Corinth, Cuffs, Cup, Cusion, Cyrrus, Daemscen, Daemspel, Dagger, Dagger2, Dart, Dartbord, Deadcloz, Deadew, Deadns, Deathdis, Deceiver, Demnstat, Demon, Deskew, Deskns, Deskpict, Devon, Door_ns, Dtable, Dummy, Earthmag, Ebrock, Endgate, Endgate2, Endhydro, Endlamp, Endlith, Endskul, Endstrat, Erthitem, Erthreag, Erthspel, Ethereag, Evilsorc, Ewbpaint, Ewcrops, Ewhollog, Ewlamptp, Ewshelf, Ewshfsid, Ewspaint, Execution scene, Eye, Fallrock, Fan, Febarsew, Febarsns, Fenalia, Fgrenade, Fight, Firefeld, Fireglob, Fireitem, Firepit, Fireplac, Fireplew, Fireplns, Firereag, Fireshld, Fireshro, Firespel, Fireswmp, Firewood, Fish, Fish2, Fishbonz, Fishnet, Fishpole, Flamstng, Flask, Floatin, Flour, Food, Free, Ftableew, Ftablens, Gargoyle, Gateskul, Gemofpro, Ghost, Ghosthed, Ghoul, Girlsstu, Golem, Gorgrond, Graveii, Grave_ew, Grave_ns, Greentre, Grenade, Grimoire, Gate guard, Guard10, Guard2, Guard3, Guard4, Guard5, Guard6, Guard7, Guard8, Guard9, Guardman, Guard_ew, Gwillim, Hammer, Hamostr, Hay, Helmet, Hourglas, Hydros, Intern, Ironman, Jbox, Jenna, Jewelry, Jug, Kegew, Kegns, Key, Keyonec, Keyring, Kilandra, Kingbdew, Kingbdns, Kith, Korgfang, Korick, Lamp1, Lamp2, Lamp3, Lamppost, Lava, Lavasink, Layghoul, Lchst_ew, Lchst_ns, Legging, Legs, Lever, Lithos, Litlmush, Logbook, Logbook2, Logbook3, Logbook4, Logo, Loom, Lothalt, Lothcorp, Lothlay, Mace, Mace2, Magarm, Magarmr2, Magarms, Maghelm, Maglegs, Magscrol, Magshld, Malchir, Marble, Melbook, Method, Mir, Monfast, Mordea, Mordeabe, Mordstat, Morebrok, Morefish, Morefood, Move, Mushcap, Mushgrup, Mushroom, Mythran, Nec1, Nitstand, Nsbpaint, Nscrops, Nshollog, Nslamptp, Nsrunwod, Nsshelf, Nsshfsid, Nsspaint, Nssticks, Oaktblew, Oaktblns, Odistat, Offsup, Opnbdrol, Orlok, Oven, Pedestal, Pent, Pesant1, Pesant2, Pesant3, Plaqueew, Plaquens, Platefoo, Pole, Potion, Potplant, Potspans, Protectr, Pulchnew, Pulchnns, Pyros, Rainbarl, Rat, Recall, Rhian, Rope, Sabre, Salklog, Schair, Scimitar, Scimokg, Screamer, Scroll1, Scroll2, Sgargl, Sgbook, Shaana, Shchimne, Shield, Shortmsh, Silvore, Sinking, Skeleton, Skulcand, Skullhea, Skulz, Slayer, Smalmush, Sorcerer, Sorchat, Spelcmbt, Spider, Spiky, Spitter, Spout, Stalag, Statue, Statue1, Statuet, Stellos, Stevbook, Stmite, Stovpipe, Strathat, Stratos, Straw, Sword, Sword2, Tablware, Tallcand, Tankard, Tapestew, Tapestns, Tarna, Thurgist, Tomb, Toran, Torax, Torch, Tortchar, Tortrack, Torwin, Tossrock, Toys, Trap, Tree, Trialhat, Tring, Troll, Troodle, Troughew, Troughns, Trowel, Vanish, Vardion, Vardion2, Vase, Vivalter, Vivdagr, Vividos, Wallswit, Wardew, Wardns, Wbench, Well, Winchew, Winchns, Wool, Woundtor, Wtable, Wtableew, Wthrone, _
<!-- progress:end -->

All conversations, books and the interface are translated; the few entries left are untranslated on purpose (the cheat menu's passwords and coordinates, number answers 0–9 and the like). Names and terms are kept consistent in the [authority file](localization/zh_TW/authority.tsv). The credits and the developers' quotes stay in English, and so does the speech.

## Download and install

Download from [Releases](https://github.com/pmanyeh/Ultima-8-for-ZH/releases):

| File | For |
|---|---|
| `Ultima8-zhTW-<version>.zip` | Windows (64-bit) |
| `Ultima8-zhTW-<version>-macOS-arm64.zip` | macOS, Apple Silicon (M chips) |
| `Ultima8-zhTW-<version>-macOS-x86_64.zip` | macOS, Intel |

**You need your own legal copy of the English Ultima VIII** (e.g. the GOG *Ultima 8 Gold Edition*). This project contains **no** game data, music, speech or savegames.

The packages contain ScummVM (with the translation support), the translation and the fonts; unpack and run, nothing to install. Instructions and settings come with the package (in Chinese):

- [Installation (Windows)](package/INSTALL.zh-TW.md), [Installation (macOS)](package/INSTALL-macOS.zh-TW.md)
- [Settings](package/SETTINGS.zh-TW.md): fonts, speech bubbles, music device
- [Console commands](package/CONSOLE.zh-TW.md): teleport, cheats, playing movies and music
- [Changelog](package/CHANGELOG.md)

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
| `tools/build/`, `tools/package/` | Building the engine, packaging for Windows and macOS |
| `package/` | Player documents (installation, settings, console commands, changelog), fonts, default settings |
| `.github/workflows/` | macOS build (GitHub Actions) |
| `docs/` | Plan, architecture decisions (ADR), phase reports |

## Engine source

The engine changes are on the [`ultima8-zh-tw-dev` branch of pmanyeh/scummvm](https://github.com/pmanyeh/scummvm/tree/ultima8-zh-tw-dev) (GPL, source available). To build it yourself: on Windows `tools/build/build_release.bat` and `tools/package/make_package.ps1`; for macOS see `.github/workflows/macos.yml`.

## Contributing translations

See [localization/README.md](localization/README.md) (in Chinese) for the file format, the symbols to keep, and how to check and compile.

```bash
python tools/catalog/u8catalog.py check zh_TW      # check translations
python tools/catalog/u8catalog.py stats zh_TW      # statistics
python tools/catalog/progress.py zh_TW             # update the progress on this page
```

## Copyright and license

- *Ultima VIII: Pagan* and its text are copyright of their owners (Origin Systems / Electronic Arts). The English text kept in the translation files is quoted for reference while translating.
- The Cubic 11 and jf open huninn fonts are licensed under the SIL Open Font License 1.1; the Wang Han Zong Weibei font under the GPL-2.0.
- This project (translations, authority file, tools) is licensed under the GNU General Public License v3.0 or later, see [LICENSE](LICENSE); the engine changes follow ScummVM's GPL-3.0.

## Thanks

- [ScummVM](https://www.scummvm.org/) and the Pentagram team for the Ultima 8 engine
- [Cubic 11](https://github.com/ACh-K/Cubic-11)
- [jf open huninn](https://justfont.com/huninn/) (justfont)
- Professor Wang Han Zong's [free fonts](https://code.google.com/archive/p/wangfonts/)
- All Ultima fans
