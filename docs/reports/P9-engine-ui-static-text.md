# Phase P9 Report — Engine UI / Static Text

## Result

**PASS**（角色狀態欄維持英文，見 Findings 3）

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `cb69291575`（本機，未 push；接續 P7 的 `5a8b1e7e5b`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），480 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（未修改）
- 遊戲內測試：使用者操作（2026-10-06 22:50–23:20）

## Scope Performed

依 Master Plan §28 與 P8 inventory 的 #14–#16、#18–#20、#22。

| Surface | 做法 | 結果 |
|---|---|---|
| engine 字串的 identity | 翻譯檔新增 `ui` context，以英文原文辨識；**與 Usecode 的 bark / ask ID 分開**（§28 要求） | ✅ |
| 主選單（Esc） | 英文版是圖片（gump shape 37）。翻譯存在且字型能畫 UTF-8 時，改為文字按鈕（字型 0）——與日文版相同的做法 | ✅「1.開場動畫」…「6.離開」 |
| 輸入名字 | `Give thy name:` → 請報上你的名字：（字型 6） | ✅（程式碼路徑；新遊戲不經過此畫面，見 Findings 6） |
| 離開確認 | 問句圖片（shape 18）改為文字「要離開遊戲嗎？」（字型 6）；yes / no 按鈕圖片不變（日文版也保留） | ✅ |
| 日記（原版存讀檔畫面） | `The Beginning...` → 旅程的開端……；以書本字型 9（CJK，黑色）顯示，日記字型 4 不變 | ✅ |
| 死亡畫面 | 方案 A（P8 決定）：英文墓碑字 + 下方中文字幕（字型 6），沿用日文版 `ReadableGump` 的字幕方式 | ✅ |
| 角色狀態欄 | **維持英文**（STR / INT / …），見 Findings 3 | — |
| 其他圖片文字 | 以新工具檢視 `U8GUMPS.FLX`：除上述外只有「Entry」（46）、「OK」（42）、遊戲標題「PAGAN」（32）、yes / no（47、50），**維持原樣** | — |

另外修正：

- **`TTFont::renderText` 寫出圖片範圍**（Findings 1）：文字與游標的每個像素都檢查範圍；游標位置改以「字」而不是 byte 計算。
- 新增 `AvatarDeathProcess::showGravestone()` 與主控台指令 `Localization::gravestone`（只顯示墓碑，不會讓主角死亡），用於測試。
- 新增工具 `tools/diagnostics/u8shapes.py`：把 U8 的 shape 檔轉成 PNG（只在本機檢視，**圖片不放進 repo**）。

新增翻譯檔 `localization/zh_TW/ui/engine.po`（12 條）。翻譯檔合計 69 條。

## 設計決定

### 圖片文字：文字按鈕而不是翻譯後的圖片

Master Plan §28 建議圖片文字「優先 translated frame」。本 Phase 改用日文版已有的機制（`_TL_SHP_` 讓圖片按鈕改為文字按鈕）：

- 不需要製作新的圖片素材與 shape 打包流程，也不會有素材授權問題。
- 譯文可以隨時修改，不必重新繪圖。
- 引擎的 `GameData::translate(FrameID)` 目前不支援從另一個 shape 檔讀取替換圖片（程式內有 TODO）。

缺點是外觀沒有原版圖片的手寫風格。之後若要改為中文圖片，可以在 P15（HD 文字層）一併評估。

### `ui` 文字的字型檢查

`Localization::uiText(英文, 字型)`：只有 localization 啟用、有譯文、而且該字型能畫 UTF-8 時才回傳中文，否則回傳遊戲原本的 `_TL_()` 文字。各個介面再依「是否為譯文」決定要不要從圖片改成文字。

## Evidence

### 遊戲內（使用者操作）

| 項目 | 結果 |
|---|---|
| 主選單 | ✅ 中文文字按鈕，排列與點擊正常 |
| 離開確認 | ✅「要離開遊戲嗎？」；no 取消正常 |
| 死亡畫面（`Localization::gravestone`） | ✅ 英文墓碑字 + 中文字幕 |
| 日記：讀取 | ✅ 第一格「旅程的開端……」；其他格的描述（p2、p3）在正確位置 |
| 日記：寫入 | ✅ 輸入英文描述「123qweqe」存到 Entry 4，位置與游標正常（修正後） |
| 角色狀態欄 | 第一版中文標籤重疊 → 改回英文 |
| 英文模式（`launch-dev.bat 1 en`） | ✅ 原本的圖片與文字 |

### 單元測試

```text
Running cxxtest tests (480 tests)....OK!
```

`test_canonical_context` 加入 `ui` context。

### 啟動檢查

OFF、zh_TW、缺字型三種情境結果與 P4 相同；zh_TW 載入 69 條。

## Acceptance（Master Plan §28）

| 項目 | 結果 | 說明 |
|---|---|---|
| known engine UI strings translated | ✅ | 主選單、輸入名字、離開確認、日記、死亡畫面（狀態欄除外，見 Findings 3） |
| original fallback works | ✅ | localization off、沒有譯文、或字型不能畫 UTF-8 → 原本的圖片與英文 |
| translated Gump mapping works where needed | ✅ | 主選單與離開確認的圖片 → 文字（日文版的對應方式） |
| no proprietary assets committed | ✅ | 沒有提交任何遊戲圖片；`u8shapes.py` 只在本機輸出 PNG |

## Findings

### Observed

1. **`TTFont::renderText` 會寫到圖片範圍外（upstream 既有的問題）。** 游標在行尾、或輸入框比字型還矮時，游標的像素寫到圖片緩衝區之外，Debug 版跳出 `HEAP CORRUPTION DETECTED`。原版的日記輸入框使用點陣字型，從來不會走到這段程式；P9 第一版把日記字型換成 CJK TTF 後才觸發。已加上範圍檢查。可考慮回報 upstream。
2. **輸入框（`EditWidget`）使用 high-res TTF 時位置錯誤。** 日記輸入框改用 CJK 字型後，輸入的文字被畫到畫面底部。最後改為不替換日記字型（4），輸入框維持原版字型，「旅程的開端……」改用書本字型（9）。根本原因尚未修正，列為 §49 #23（使用者：之後再修）。
3. **角色狀態欄放不下中文。** 七個欄位的間距只有 9 個遊戲像素，中文字約 11 像素高，會互相重疊。日文版這裡也維持英文。STR / INT / DEX 等是常見的 RPG 縮寫，維持英文。
4. **ScummVM 沒有繁體中文介面翻譯。** `po/zh_Hant.po` 沒有任何譯文（設 `gui_language=zh_Hant` 會顯示英文）；簡體 `po/zh.po` 有 1,084 / 3,258 條。ScummVM 自己的選單、存讀檔畫面不在本專案範圍。
5. **ScummVM 預設使用自己的存讀檔畫面。** 遊戲選單的「讀取 / 寫入日記」只有在勾選「Use original save/load screens」（`originalsaveload`）時才會使用 U8 原版的日記畫面。測試設定檔已開啟。
6. 原版日記的 Entry N 對應 ScummVM 第 N 格存檔，Entry 1 固定是「旅程的開端」（開新遊戲），所以第 1 格存檔只會出現在 ScummVM 的存讀檔畫面。屬原版行為。

### Inferred

- 「輸入名字」畫面只在特定情況出現（P7 的新遊戲直接進入與 Devon 的對話），本 Phase 只有程式碼層級的確認。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `cb69291575`）：15 個檔案，+136 / −29
- 主 repo：本報告、`localization/zh_TW/ui/engine.po`、`tools/catalog/po_compile.py`（`ui` context）、`tools/diagnostics/u8shapes.py`、inventory 修正、Master Plan 與 HANDOFF
- 本機：`private_test/scummvm-dev.ini`、`scummvm-dev-en.ini`（`originalsaveload=true`）

## Regressions

- 480 項單元測試通過。
- localization off：`uiText()` 回傳 `_TL_()` 的結果，所有介面走原本的路徑（圖片按鈕、圖片問句、日記字型 4）。
- 日文版：主選單與離開確認的日文路徑（`_TL_SHP_` → 0）保留；localization 對日文版不啟用。
- `TTFont::renderText` 的修改只影響原本會寫出範圍的像素；游標位置對單一 byte 字元的結果不變。

## Risks

1. 主選單的中文文字按鈕沒有原版圖片的手寫風格。
2. `EditWidget` 的 high-res 問題（§49 #23）會影響之後任何讓輸入框使用 CJK 字型的情況。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 10（Extraction & Translation Catalog Toolchain）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 9 as required. Phase 10 was not started.
