# Phase P3 Report — UTF-8 / CJK Foundation

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`（由 upstream `master` @ `71cb05b1` 開出）
- Commit: `96bfc46318`（本機，未 push）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，Ultima 引擎 0 warning
- Unit test build: WSL Ubuntu（g++ 15.2），`configure --backend=null --disable-all-engines --enable-engine=ultima,ultima8 --disable-freetype2`，`make test`
- Game data: GOG Ultima VIII Gold Edition, English（未修改）

## Scope Performed

依 Master Plan v2 §22 的工作項目，把 Phase 2 spike 的字型部分**重新寫成正式實作**（不含翻譯查表，那是 P4 的範圍）。

| 項目 | 內容 |
|---|---|
| `Font::UTF8Traits` | UTF-8 解碼。**不合法的 UTF-8 序列改以原本的 8-bit 表（CP437）逐 byte 解碼**，而不是 U+FFFD（見 Findings 1）。`advance()` / `length()` / `unicode()` 共用同一個 `sequenceLength()`，步數保證一致 |
| 中文換行 | `endsWord()`：每個 CJK 字元都是可斷行點；`canBreakAfter()`：繁中標點禁則。舊有的 `Traits` 與 `SJISTraits` 的 `endsWord` 永遠回傳 false，行為不變 |
| `typesetText` 修正 | 一個字元比整行還寬時，原本會無限迴圈（英文路徑也一樣），改為讓該字元單獨一行（見 Findings 2） |
| `TTFont` | 與 SJIS 並列的 UTF-8 模式；`toUnicode` 改為逐字附加（修正多 byte 文字造成的斷言失敗） |
| `FontManager::addCJKOverride` | 每個字型可個別設定反鋸齒，像素字型關閉反鋸齒時，不影響其他 TTF 字型 |
| `GameData::setupCJKOverrides` | 設定 `font_cjk_file` 後，對話字型改用 CJK 字型；顏色與黑框沿用 `[fontoverride]` |
| 除錯指令 | `Ultima8Engine::barkTestFile <file> [line]`：讓主角說出 UTF-8 檔案中的某一行，用來檢查繪製 |
| 單元測試 | `test/engines/ultima/ultima8/gfx/font_utf8.h`（12 項） |
| 字集檢查工具 | `tools/validate/font_coverage.py`（主 repo） |

設定（遊戲設定檔，暫定名稱，P4 確認）：

```ini
font_cjk_file=Cubic_11.ttf
font_cjk_size=12
font_cjk_antialiasing=false
```

## Evidence

### 單元測試

```text
Running cxxtest tests (466 tests)....................OK!
```

全部通過，包括 ScummVM 原有的全部測試與新增的 12 項：

| 測試 | 內容 |
|---|---|
| `test_decode_required_strings` | Master Plan §22 的 5 個必測字串：長度與碼位 |
| `test_decode_malformed` | 截斷、孤立延續 byte、不合法 lead byte、多餘延續 byte、lead byte 後接 ASCII |
| `test_original_game_text_unchanged` | 原版英文遊戲中 4 個含 CP437 字元的句子：UTF-8 模式與原路徑解碼結果完全相同 |
| `test_kinsoku` | `中|，` 不可斷、`「|這` 不可斷、拉丁字母之間不可斷 |
| `test_wrap_pure_chinese` | 純中文逐字換行 |
| `test_no_punctuation_at_line_start` | 「，」不出現在行首 |
| `test_wrap_mixed_text_without_gap` | 「我是在 Lurker 領域的深處」中英混排不留空白 |
| `test_u8_specials_in_utf8_text` | `~` 換行、`*` 分頁 |
| `test_page_height_limit` | 高度限制與 `remaining`（byte offset） |
| `test_very_narrow_rectangle` | 寬度小於一個字（中文與英文都測） |
| `test_legacy_traits_unchanged` | 英文 Traits 換行結果不變，`endsWord` 為 false |
| `test_sjis_traits_unchanged` | SJIS 解碼不變（日本 → U+65E5 U+672C） |

### 遊戲內繪製（Windows build，Cubic 11 12px，關閉反鋸齒）

以 `barkTestFile` 讓主角說出測試字串，並截圖確認：

| 測試字串 | 結果 |
|---|---|
| 中英混排長句（「我也不太清楚……我是在 Lurker 領域的深處……」） | ✅ 逐字換行，`Lurker` 後不留空白 |
| 純中文長句加標點禁則 | ✅ 每頁 3 行；「，」不在行首 |
| 原版 CP437 文字 `Ich heiße Salkind. Enchanté, schöner Name.` | ✅ ß、é、ö 正確顯示 |
| 開場動畫字幕、名字輸入畫面、Devon 的英文選項 | ✅ 以像素字型正常顯示 |

### 字集覆蓋檢查

```text
font: Cubic_11.ttf  glyphs: 10268
distinct characters used: 113  missing: 0      ← POC 翻譯表
```

刻意加入的罕用字（龘、𠀋）會被正確列為缺字。

## Findings

### Observed

1. **原版英文文字含有 CP437 字元。** 全部 11,238 個 literal 中，有 4 句、共 10 個 byte ≥ 0x80（SALKIND、DARION、MYTHRAN 的德文與法文，例如 `hei\xE1e`）。若 UTF-8 模式把它們解成 U+FFFD 會造成英文退化，因此改為「不合法的序列 → 以 CP437 解碼」。這樣既能顯示中文，原文也完全不變。
2. **原版的換行程式在「一個字元比整行還寬」時會無限迴圈。** 空行不斷增加，直到記憶體耗盡（單元測試中發生 `std::bad_alloc`）。英文路徑也有相同問題，只是遊戲中的文字框夠寬，從不觸發。已修正，只影響原本會當掉的情況。
3. **CJK 字型會套用到所有對話字型**：開場字幕、名字輸入、英文選項都改用像素字型。這符合預期（未翻譯的英文仍需要顯示），但英文的外觀會與原版不同。
4. **ScummVM 的 MSVC `--tests` 模式會停用所有引擎**，Ultima8 的單元測試在 Windows 無法建置，因此改在 WSL 以 upstream 的 `make test` 執行。WSL 需要三個繞道：`VER_REV=…`（避免 `git describe` 掃描 Windows 檔案系統）、以 `python3` 執行 `cxxtestgen`（CRLF 與 `python` shebang 問題）、`make -o test/runner.cpp`。

### Inferred

- `font_cjk_*` 設定目前只要有字型檔就會啟用。P4 的 localization 開關，應該同時決定「是否載入 CJK 字型」與「是否查翻譯表」，並在字型載入失敗時停用翻譯。

### Unknown

- 日文版的實際執行（本機沒有日文版資料）。程式碼層級：SJIS Traits 的單元測試通過；`toUnicode` 的修改對 SJIS 文字的輸出結果與原本相同（逐字附加 vs 預先配置）。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `96bfc46318`）：11 個檔案，+531 / −12
- 主 repo：`docs/reports/P3-cjk-foundation.md`、`tools/validate/font_coverage.py`、Master Plan 進度更新
- 本機：`private_test/launch-dev.bat`、`scummvm-dev.ini`、`extra/p3_test_strings.txt`

## Regressions

- ScummVM 全部 466 項單元測試通過。
- 英文：舊有 Traits 的單元測試通過；原版 CP437 文字在 UTF-8 模式下顯示正確。
- 日文：SJIS 單元測試通過；沒有實機資料。
- 未設定 `font_cjk_file` 時，程式路徑與原版相同（除了 `toUnicode` 的配置方式與窄寬度修正，兩者輸出相同或只影響原本會當掉的情況）。

## Risks

1. 在 Windows 跑單元測試需要 WSL，且有三個繞道（Findings 4）。
2. 啟用 CJK 字型後，英文文字的外觀也會改變（Findings 3）。

## Blockers

無。

## 其他事項

- **存檔遺失：** `private_test/saves/` 中的 `p1-after` 存檔（`ultima8.001`）在 2026-10-06 00:15 前後消失，原因不明。Agent 沒有執行任何刪除存檔的指令。不影響本 Phase 的結果。

## Next Phase Readiness

**READY**：Phase 4（Localization Manager）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 3 as required. Phase 4 was not started.
