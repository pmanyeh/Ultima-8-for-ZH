# Phase P0 Report — Baseline

## Result

**PASS**

前一版報告（BLOCKED：工作區沒有 ScummVM 原始碼）的 blocker 已解除：upstream ScummVM 已 clone 至 `scummvm-src/`，並以未修改的原始碼完成 Debug 與 Release 建置。

Build、detection、launch、TTF override 由 Agent 驗證（log 為證據）。互動遊玩項目（intro、移動、對話、選項、物品欄、存檔/讀檔、音效、字幕、TTF 實際畫面）由使用者於 2026-10-05 以 `private_test/launch-p0.bat`（Release x64）實際遊玩確認，全部 OK。

## Environment

| 項目 | 值 |
|---|---|
| Workspace | `D:\git\Ultima 8 for ZH`（本身不是 git repo） |
| ScummVM repository | `https://github.com/scummvm/scummvm.git`（upstream，blobless clone）→ `scummvm-src/` |
| Branch | `master` |
| Commit | `71cb05b1c03aa6bdcd34f78c20cef12c10067ba5`（2026-10-05，"I18N: Update translations templates"） |
| Working tree | clean（`git status --porcelain` 無輸出；`build-scummvm/` 已被 upstream `.gitignore` 的 `/build*` 排除） |
| ScummVM version string | `ScummVM 2026.3.1git` |
| IDE / Compiler | Visual Studio Community 2026（18.8.12023.21），MSVC 14.51.36231，Windows SDK 10.0.26100.0 |
| Platform | x64（`-arch=x64 -host_arch=x64`） |
| vcpkg | 獨立安裝於 `D:\vcpkg`，commit `19780d9cdf84d0944cf9a318666703b89ab6629c`（tool 2026-09-26） |
| vcpkg installed dir | `D:\vcpkg\installed_scummvm\x64-windows`（37 packages，依 upstream `vcpkg.json` manifest） |
| Game data | GOG *Ultima VIII – Pagan*（gameId 1207659015），`Ultima 8\ENGLISH\` |

## Build Commands

建置流程依照 upstream `.github/workflows/ci.yml` 的 Windows job，差異列於下方〈Deviations〉。

```bat
rem 0) VS developer environment
call "C:\Program Files\Microsoft Visual Studio\18\Community\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64

rem 1) create_project
cd scummvm-src\devtools\create_project\cmake
cmake .
cmake --build . --config Debug

rem 2) generate solution (ultima engine only)
mkdir scummvm-src\build-scummvm & cd scummvm-src\build-scummvm
..\devtools\create_project\cmake\Debug\create_project.exe .. --msvc --vcpkg --disable-all-engines --enable-engine=ultima,ultima8

rem 3) dependencies (run from scummvm-src, uses upstream vcpkg.json)
set VCPKG_ROOT=D:\vcpkg
set VCPKG_OVERLAY_PORTS=<scummvm-src>\.github\vcpkg-ports
D:\vcpkg\vcpkg.exe install --triplet x64-windows --x-install-root=D:\vcpkg\installed_scummvm

rem 4) build (Configuration = Debug | Release)
msbuild scummvm.sln /m /p:Configuration=Debug /p:Platform=x64 /p:PreferredToolArchitecture=x64 ^
  /p:VcpkgRoot=D:\vcpkg\ /p:VcpkgEnableManifest=true /p:VcpkgManifestInstall=false ^
  /p:VcpkgInstalledDir=D:\vcpkg\installed_scummvm\ ^
  /p:ForceImportAfterCppTargets=D:\vcpkg\scripts\buildsystems\msbuild\vcpkg.targets
```

這個做法**沒有**執行 `vcpkg integrate install`，因此不會改動使用者全域的 MSBuild 設定。

產生的 config 已確認包含 `ENABLE_ULTIMA`、`ENABLE_ULTIMA8`、`USE_FREETYPE2`、`USE_HIGHRES`、`USE_RGB_COLOR`、`USE_IMGUI`。

## Runtime Command

```bat
scummvm-src\build-scummvm\Debugx64\scummvm.exe ^
  --config=<scratch>\p0_scummvm.ini ^
  --extrapath="D:\git\Ultima 8 for ZH\scummvm-src\dists\engine-data" ^
  --logfile=<scratch>\p0_launch.log --debuglevel=1 --debugflags=Graphics ultima8
```

所有測試都使用獨立的 `--config` 檔，不寫入使用者的 `%APPDATA%\ScummVM\scummvm.ini`。（第一次執行 `--version` 時，沒帶 `--config` 而建立了一個 0 byte 的預設檔，已立即刪除。）

## Deviations From Upstream CI

| 項目 | Upstream CI | 本次 | 原因 |
|---|---|---|---|
| vcpkg commit | `ef7dbf94…` | `19780d9c…`（master） | CI 固定版本的 vcpkg tool（2025-06）無法辨識 VS 2026 / MSVC 14.51：`Unable to find a valid Visual Studio instance` |
| Engines | `--enable-all-engines` | `--disable-all-engines --enable-engine=ultima,ultima8` | Phase 0 只需要 Ultima；縮短建置時間 |
| Optional features | `--enable-discord --enable-faad --enable-gif --enable-mikmod --enable-mpeg2 --enable-vpx` | 預設 | 與 Ultima VIII 無關 |
| Platform | win32 / x64 / arm64 | x64 | 本機開發平台 |
| vcpkg integration | `vcpkg integrate install`（全域） | `ForceImportAfterCppTargets`（單次建置） | 避免改動使用者全域設定 |

## Build Results

| Configuration | Result | Output | Notes |
|---|---|---|---|
| Debug x64 | **PASS**（exit 0） | `build-scummvm\Debugx64\scummvm.exe` | 87 warnings，全部在 Ultima 引擎之外：`common/singleton.h` C4506 ×85、`backends/graphics/opengl/renderer3d.cpp` C4146 ×2。Ultima 引擎 0 warning。 |
| Release x64 | **PASS**（exit 0） | `build-scummvm\Releasex64\scummvm.exe` | Warnings 與 Debug 相同（C4506 ×85、C4146 ×2）。Smoke test：TTF override 已套用、`-- Game Initialized --`、20 秒無 crash。 |

已知非致命訊息：vcpkg 的 applocal DLL 複製步驟找不到 `pwsh.exe`（只裝了 Windows PowerShell 5.1），但 runtime DLL 有正確複製到輸出目錄，執行檔可正常啟動。

## Runtime Results

### Observed

- `scummvm.exe --list-engines`：只列出 `ultima  Ultima`，符合預期。
- `scummvm.exe --detect --path=…\ENGLISH`：
  `ultima:ultima8  Ultima VIII: Pagan (Gold Edition/DOS/English)`
- Detection 依據（`engines/ultima/detection_tables.h:282`）：
  - `usecode/eusecode.flx` 前 5000 bytes MD5 = `c61f1dacde591cb39d452264e281f234`，size 1251108 — 相符
  - `static/eintro.skf` 前 5000 bytes MD5 = `b34169ece4286735262ac3430c441909`，size 1297731 — 相符
- 啟動（預設字型）：完成 `Initializing Pentagram`、`Load GameData`、`Load Shapes`、`Loading translation: u8english.ini`、`Starting new Ultima 8 game`、`-- Game Initialized --`；25 秒後 process 仍在執行，log 中沒有 error。
- 啟動（`font_override=true`、`font_antialiasing=true`、`font_highres=true`）：
  `Opened TTF: Vera.ttf` / `VeraBd.ttf`；`Added TTF override for font 0, 5, 6, 7, 8, 9`。20 秒後 process 仍在執行。

### Manual Gameplay Verification（使用者驗證，2026-10-05）

測試方式：`private_test/launch-p0.bat`（Release x64），設定檔 `private_test/scummvm-p0.ini`（`font_override=true`、`font_antialiasing=true`、`font_highres=true`、`subtitles=true`，savepath `private_test/saves/`）。

- [x] intro 播放
- [x] new game → 移動
- [x] 一段 NPC 對話（BarkGump）
- [x] 一個玩家回答選項（AskGump）
- [x] 物品欄
- [x] 存檔 / 讀檔
- [x] 音效 / 音樂 / 語音
- [x] 字幕
- [x] TTF override 的實際畫面（anti-alias、high-res 文字）

說明：上述結果為使用者回報，Agent 沒有獨立的畫面或錄影證據。

## Source Map（P0.5，唯讀）

所有路徑相對於 `scummvm-src/engines/ultima/ultima8/`。

| 元件 | 檔案 | 關鍵位置 |
|---|---|---|
| GameData | `games/game_data.cpp` | `loadTranslation()` :144、`translate(const String&)` :179、`translate(FrameID)` :189、`loadU8Data()` :226（讀 `<lang>usecode.flx`、`u8game.ini`）、`setupFontOverrides()` :360、`setupJPOverrides()` :367、`setupTTFOverrides()` :395、`getSpeechFlex()` :427；macros `_TL_` / `_TL_SHP_` 定義於 `games/game_data.h:140-141` |
| UCMachine | `usecode/uc_machine.cpp` | `execProcess()` :152；opcode `0x0D` push string :302；`0x16` string concat :481-495；`getString()` :2013；`assignString()` :2033；`duplicateString()` :2042；`freeString()` :2057；`saveStrings()` :2292 / `loadStrings()` :2317（由 `ultima8.cpp:1264` / `:1524` 呼叫） |
| Bark / Ask 入口 | `world/item.cpp` | `Item::bark()` :2033（`new BarkGump`）、`Item::I_bark()` :3053、`Item::I_ask()` :3149（`new AskGump(1, answers)`） |
| Font | `gfx/fonts/font.h` / `font.cpp` | `Font::Traits`、`Font::SJISTraits`、`typesetText<T>()`（template，於 `font.cpp:368-376` 對兩種 Traits 實例化） |
| TTFont | `gfx/fonts/tt_font.cpp` | ctor :35（bullet glyph 選擇）、`toUnicode<T>()` :75、`getStringSize()` :93、`getTextSize()` :108、`renderText()` :195；`_SJIS` bool 決定 Traits |
| FontManager | `gfx/fonts/font_manager.cpp` | `getTTF_Font()` :87、`addTTFOverride()` :137、`addJPOverride()` :155、`loadTTFont()` :183；ConfMan keys `font_override`、`font_antialiasing`、`font_highres` |
| JPFont | `gfx/fonts/jp_font.cpp` | 使用 `SJISTraits` 的 shape-based 日文字型 |
| BarkGump | `gumps/bark_gump.cpp` | ctor :49、`InitGump()` :78（建立 TextWidget、`playSpeech(_barked…)`）、`NextText()` :128、`calculateTicks()` :142、`run()` :161、`saveData()` :204 |
| AskGump | `gumps/ask_gump.cpp` | `InitGump()` :50（`getString(_answers->getStringIndex(i))` → ButtonWidget）、`ChildNotify()` :90（`_processResult = string index`） |
| ReadableGump | `gumps/readable_gump.cpp` | ctor :44、`I_readGrave()` :91、`I_readPlaque()` :104 |
| BookGump *（計劃未列）* | `gumps/book_gump.cpp` | `InitGump()` :50（使用 `_TL_`）、`I_readBook()` :124 |
| ScrollGump *（計劃未列）* | `gumps/scroll_gump.cpp` | `I_readScroll()` :99 |
| TextWidget | `gumps/widgets/text_widget.cpp` | ctor :40、`setupNextText()` :105、`renderText()` :145、`saveData()` :203 |
| ButtonWidget | `gumps/widgets/button_widget.cpp` | text ctor :41、`saveData()` :181 |
| Engine data | `devtools/create_ultima8/*.ini` → `dists/engine-data/ultima8.dat` | `u8game.ini [fontoverride]`、`u8<lang>.ini [text]/[gumps]/[jpfonts]/[fontoverride]`、`Vera.ttf` / `VeraBd.ttf` |

## Findings

### Observed

1. **Ultima8 是 `ultima` 引擎的子引擎。** 建置時必須啟用 `ultima`（含 `ultima8`）；`--detect` 回報的 ID 是 `ultima:ultima8`。
2. **Bark 字串在 `Item::bark()` 以 `Common::String` 傳入 `BarkGump`。** `BarkGump::_barked` 會：
   - 交給 `TextWidget` 顯示（`bark_gump.cpp:90`）
   - 作為 speech lookup key（`playSpeech` / `getSpeechLength` / `isSpeechPlaying` / `stopSpeech`）
   - 用 `_barked.size()` 計算顯示時間（`:150`）
   - 寫入存檔（`saveData` :212-213）
   這與 Master Plan §24 的「`_barked` 必須保持原文」一致。
3. **AskGump 用 UCList 的 string index 識別答案。** 按下按鈕時，`ChildNotify()` 會把 `_answers->getStringIndex(child->GetIndex())` 設成 `_processResult`。顯示文字只用來建立 `ButtonWidget`。這與 Master Plan §25 的假設一致。
4. **TextWidget 會把實際顯示的 `_text` 與分頁 byte offset（`_currentStart` / `_currentEnd`）寫入存檔**（`text_widget.cpp:209-215`）。若在建立 TextWidget 之前就把文字換成中文，存檔裡會出現中文與以 UTF-8 計算的 offset。**這是 Phase 1/2 必須處理的存檔相容性議題。**
5. **String heap 會進存檔**（`UCMachine::saveStrings` / `loadStrings`）。
6. **Usecode 會直接比對字串內容。** `uc_machine.cpp:310-316` 有一段針對德文版字串 `" Irgendetwas stimmt nicht!"` 的 workaround，證明 Usecode 邏輯依賴字串內容。這支持「不得覆寫 string heap」的原則。
7. **已有 key 為英文全文的翻譯機制：** `GameData::translate()` 讀 `u8<lang>.ini` 的 `[language] text` 區段，透過 `_TL_()` 用於 BookGump、MenuGump、PaperdollGump、QuitGump、U8SaveGump、AvatarDeathProcess、TargetReticleProcess。`u8english.ini` 也用它修正書本內容。程式中有 `TODO: maybe cache these lookups`，代表每次呼叫都會查 config。
8. **Japanese path：** `GameData::setupFontOverrides()` 只在 `GAMELANG_JAPANESE` 時呼叫 `setupJPOverrides()`，套用 `[jpfonts]`（JPFont / SJISTraits）以及 `setupTTFOverrides("language", true)`（`u8japanese.ini` 指定 `kanji.ttf`，SJIS=true）。`u8japanese.ini` 的 `[text]` 是 **Shift-JIS bytes，不是 UTF-8**。
9. **TTFont 的編碼是二選一：** `_SJIS` 為 true 時使用 `SJISTraits`；否則使用 `Traits`，透過 `encoding[]` 把單一 byte 對應到 Unicode。目前沒有 UTF-8 路徑。
10. **TTF override 在 runtime 確實生效**（見 Runtime Results）。預設字型是 `ultima8.dat` 內附的 Bitstream Vera。
11. **控制字元與 Master Plan §9 不完全相同：**
    - `Traits::isSpace`：`%` `~` `*` `^`
    - `Traits::isTab`：`%`
    - `Traits::isBreak`：`~` `*`
    - `Traits::isPageBreak`：`*`
    - `@` **不在** Traits 裡。只有 `TTFont::toUnicode()` 會把 `@` 換成 bullet glyph（`tt_font.cpp:83`），credits gump 也有另外的處理。
12. **計劃未列出的文字 surface：** `BookGump`、`ScrollGump`、`MenuGump`、`QuitGump`、`U8SaveGump`、`CreditsGump`。

### Inferred

- 若在 `BarkGump::InitGump()` 建立 TextWidget 時才替換顯示文字，可以保持 `_barked` 不變，但 TextWidget 本身仍會把中文存進存檔（見 Observed #4）。需要 Phase 1 決定：是在 TextWidget 繪製或分頁時才翻譯，還是接受存檔中有顯示文字並在讀檔時重建。
- `AskGump::InitGump()` 組 `str_answer` 的位置是顯示層，替換那裡的文字應該不會影響 `_processResult`。但 ButtonWidget 的存檔內容仍需在 Phase 1 確認。
- 繁中需要第三種 Traits（UTF-8）。`Common::String` / `Common::U32String` 已有可用的 UTF-8 轉換 API，Phase 3 應優先使用。
- 現有 `GameData::translate()` 的 key 是英文全文，不能直接作為對話 translation identity（Master Plan §7），但可以沿用到 engine UI（Phase 9）。

### Unknown

- 原版英文資料中，NPC 台詞實際用到哪些 concat 路徑（`0x16` 之外的 list 操作等）——Phase 1。
- ButtonWidget / AskGump 存檔是否包含答案文字——Phase 1。
- Japanese runtime regression 的 baseline：本機沒有日文版資料。

## Files Changed

- `docs/reports/P0-baseline.md`：以本報告取代先前的 BLOCKED 版本。
- 新增 `scummvm-src/`（未修改的 upstream clone），以及其中被 gitignore 的建置輸出 `scummvm-src/build-scummvm/`。
- Workspace 外：`D:\vcpkg`（vcpkg 與已安裝的相依套件）。
- **沒有修改** ScummVM 原始碼、Ultima VIII 遊戲資料或 Usecode。沒有建立翻譯，也沒有新增語言 enum 或 dependency。

## Tests

| Test | Result |
|---|---|
| create_project build | PASS |
| Solution generation (ultima only) | PASS |
| vcpkg dependencies (37) | PASS |
| Debug build | PASS |
| Release build | PASS（含 launch smoke test） |
| Engine list | PASS |
| Game detection | PASS（Gold Edition / English） |
| Launch → new game initialized（default font） | PASS（log；25 秒無 crash） |
| Launch with TTF override | PASS（log；6 個 override 已套用） |
| Interactive gameplay checklist | PASS（使用者驗證） |

## Regressions

無：沒有修改任何程式碼。

## Risks

1. 存檔會保存顯示文字（`TextWidget::_text`、`BarkGump::_barked`、string heap），所以 presentation-time localization 的掛點必須避開所有會被序列化的欄位，否則會違反 Master Plan §16「save game 必須儲存翻譯後字串 → STOP」。
2. 換行與分頁使用 byte offset（`remaining`、`_currentStart` / `_currentEnd`）；改成 UTF-8 後，offset 的語意需要重新定義。
3. 使用的 vcpkg 版本比 upstream CI 新（為了支援 VS 2026），未來和 upstream 同步時可能有差異。
4. 本機沒有日文版資料，Japanese regression 只能做到 code-path 層級。

## Blockers

無。

## Recommendation

1. 審閱 Observed #4（TextWidget 會存顯示文字）與 #11（控制字元差異）。這兩點會影響 Phase 1 的研究方向，以及 Master Plan §9 的內容。
2. 決定是否要在 GitHub 建立自己的 ScummVM fork，並把 `scummvm-src/` 改成指向該 fork 的 submodule（Master Plan §12-13）。Agent 不會自行 push。

## Phase 0 Acceptance

- [x] Debug build PASS
- [x] Release build PASS
- [x] English Ultima VIII launches
- [x] conversation works
- [x] save/load works
- [x] TTF override confirmed
- [x] source map recorded
- [x] no code modified

## Next Phase Readiness

**READY**：Phase 1 待使用者審閱本報告並明確指示後才開始。

## STOP

Work stopped after Phase 0 as required. Phase 1 was not started.
