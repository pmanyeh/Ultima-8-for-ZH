# 授權

## 本中文化

| 內容 | 授權 |
|---|---|
| 譯文（`u8_zh_TW.mo`、原始 PO 檔、權威檔） | GNU General Public License v3.0 或更新版本（GPL-3.0-or-later） |
| ScummVM 與其中的中文化修改（`scummvm.exe`） | GNU General Public License v3.0 或更新版本（GPL-3.0-or-later），全文見 `COPYING.txt` |
| 翻譯工具（`tools/`，在原始碼 repo 中） | GNU General Public License v3.0 或更新版本 |

依 GPL，你可以自由使用、修改、散布，散布時須一併提供原始碼並保留授權。原始碼：

- 引擎：<https://github.com/pmanyeh/scummvm>（分支 `ultima8-zh-tw-dev`；本包對應的 commit 見 `CHANGELOG.md`）
- 翻譯檔與工具：<https://github.com/pmanyeh/Ultima-8-for-ZH>

## 遊戲與遊戲文字

- *Ultima VIII: Pagan* 及其文字的著作權屬於原權利人（Origin Systems / Electronic Arts）。**本包不含任何遊戲資料**，玩家須自備正版遊戲。
- 翻譯檔（`.mo` / `.po`）中保留英文原文，作為顯示時比對原文、找出對應譯文之用。
- Ultima 是 Electronic Arts 的商標。本專案與 Electronic Arts、ScummVM 官方無關。

## 字型

- Cubic 11（俐方體 11 號）：SIL Open Font License 1.1，見 `extra/Cubic_11-OFL.txt`。
- jf open 粉圓（jf open huninn）2.1，justfont 發行：SIL Open Font License 1.1，見 `extra/jf-openhuninn-OFL.txt`。

## ScummVM 使用的第三方函式庫

`scummvm.exe` 旁的 DLL 是 ScummVM 使用的第三方函式庫，各自採用其授權（授權全文見 `LICENSES` 資料夾）：

| 函式庫 | 授權 |
|---|---|
| SDL2、SDL2_net、zlib | zlib License |
| FreeType | FreeType License（BSD 類） |
| FluidSynth、FriBidi | LGPL-2.1 |
| FLAC、libogg、libvorbis | BSD |
| libcurl | curl License（MIT 類） |
| libpng | libpng License |
| libjpeg-turbo | IJG / BSD |
| Brotli | MIT |
| bzip2 | BSD 類 |
| Microsoft Visual C++ 執行階段（`vcruntime140*.dll`、`msvcp140*.dll`） | Microsoft Visual C++ 可轉散發套件授權 |
