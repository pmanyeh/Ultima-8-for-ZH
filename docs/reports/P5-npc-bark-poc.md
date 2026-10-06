# Phase P5 Report — First NPC Bark Chinese POC ★

## Result

**PASS**（語音一項僅程式碼層級驗證，見 Acceptance）

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `a1a2282aae`（本機，未 push；接續 P4 的 `d6192426af`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），477 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（未修改）
- 遊戲內測試：使用者操作（2026-10-06 16:28–16:32）

## Scope Performed

依 Master Plan §24 與「v2：P5 工作項目」，讓 NPC 台詞（bark）以繁體中文顯示。

| 項目 | 內容 |
|---|---|
| 掛點 | `Item::I_bark` 把 `translateBark()` 的結果交給 `Item::bark(msg, displayText)` → `BarkGump(…, displayText)` |
| `BarkGump::_displayText` | 只用來建立 TextWidget，不寫入存檔；`_barked` 保持英文（語音、存檔） |
| 字型檢查（§49 #17） | `Font::isUTF8()`（`TTFont` 回傳 UTF-8 模式）。bark 的字型不能畫 UTF-8 → 顯示英文並寫 warning |
| 存檔（§49 #2） | `TextWidget::setSaveText()`：顯示譯文的 TextWidget 存檔時寫入英文原文，頁面 offset 歸零 |
| 顯示時間（§49 #3） | 有語音時，各頁時間依「實際顯示文字」的長度分配（原本除以 `_barked` 的長度） |
| 除錯指令 | `Localization::bark <class>:<ip>`：讓主角以 localization 路徑說出翻譯檔中的一句（測試存檔用） |
| POC 翻譯 | Devon 新增 2 句（`0402:2398`、`0402:3311`），共 19 條。這兩句是「已認識 Devon」的存檔實際會出現的台詞；`3311` 是長句，用來測試換行與分頁 |
| 工具 | `tools/validate/save_text_check.py`：解壓存檔，找出 CJK 文字（有就失敗）、列出 BarkGump / TextWidget 與指定英文的出現次數 |
| 啟動檔 | `launch-dev.bat <slot> en`：關閉 localization，與中文模式共用存檔 |

## 設計決定

### 存檔：寫入英文，讀檔後該句以英文顯示

自言自語的 bark 不在 stasis 中，存檔時 BarkGump 與其 TextWidget 會被寫入存檔。Master Plan 建議「讀檔時以 `_barked` 重新查表」，但查表需要 bark ID（class:IP），而 ID 不在存檔中；要存 ID 就得改存檔格式，會與 upstream 存檔不相容。

因此採用：

- TextWidget 存檔時寫入英文原文（`_barked`），offset 歸零。
- 讀檔後，這句 bark 從第一頁起以**英文**顯示剩下的幾秒，然後照常消失。之後的台詞照常顯示中文。
- 存檔格式完全不變，關閉 localization 讀檔也只會看到英文。

bark 只會停留幾秒，這個代價可以接受。

### 顯示時間

- **有語音**：原本是「本頁 byte 數 ÷ `_barked` 的 byte 數 × 語音長度」。顯示譯文時分母改為譯文長度，各頁時間的總和仍等於語音長度。未翻譯時分母相同，行為不變。
- **無語音**：「本頁 byte 數 × 480 ÷ talkspeed」不變。中文一個字 3 bytes，換算下來約為英文字母的 3 倍時間（talkspeed 預設值下約每秒 5 個中文字），不會過早消失。使用者測試確認可接受。完整調整留到 P11。

## Evidence

### 遊戲內：NPC 中文台詞（A）

`launch-dev.bat 1`（存檔 `p1-after`），與 Devon 對話。使用者確認通過：中文出現在 Devon 頭上、換行正確、沒有與英文重疊、顯示時間合理。

log `private_test/dev-20261006-163006.log`：

```text
[U8-L10N] localization zh_TW active, 19 entries from u8_zh_TW.mo
[U8-L10N] bark 0402:060F MISS src="Hello there, Pman."           ← 動態句子，英文（P11）
[U8-L10N] ask 0402 MISS src="Hello, Devon. "                     ← 選項是 P6
[U8-L10N] bark 0402:2398 HIT src="All is well, I hope. "          → 希望一切都好。
[U8-L10N] bark 0402:3311 HIT src="Well, I suppose now that you are better, ..."  → 長句，分頁顯示
[U8-L10N] bark 0402:338E MISS src="Farewell, friend Pman, and good luck."
```

對話分支與英文版相同（選 `Hello, Devon.` → `235D` / `2398`；`What should I do?` → `3311`；`Goodbye.` → `338E`）。

### 遊戲內：存檔（B）

1. 對話結束後，主控台 `Localization::bark 0402:1A04`，主角說出長段中文。
2. 中文顯示中，以 ScummVM 選單存到第 2 格（`ultima8.002`）。
3. `launch-dev.bat 2 en`（localization off）讀檔：使用者確認沒有出現中文。log `dev-20261006-163149.log` 沒有任何 `[U8-L10N]` 訊息。

存檔檢查：

```text
private_test/saves/ultima8.002: 131080 bytes, gzip at 0, 500202 bytes decompressed
  BarkGump: 1 occurrence(s)
  TextWidget: 1 occurrence(s)
  "I am unsure, my friend.": 2 occurrence(s)      ← BarkGump::_barked 與 TextWidget 的存檔文字
  "water-logged body": 2 occurrence(s)
OK: no CJK text in the save
```

存檔中確實有正在顯示的 bark（BarkGump + TextWidget），兩處都是英文。

### 單元測試

```text
Running cxxtest tests (477 tests)....OK!
```

新增 `test_find_context`（`Localization::bark` 使用的查詢）。BarkGump / TextWidget 依賴整個引擎，無法放進單元測試（見 P4 Findings 2），以遊戲內測試驗證。

### 其他

- 啟動檢查（`startup_check.ps1`）：OFF、zh_TW、缺字型三種情境結果與 P4 相同。
- 字集：`font_coverage.py Cubic_11.ttf 0402_DEVON.po` → missing 0。

## Acceptance（Master Plan §24）

| 項目 | 結果 | 證據 |
|---|---|---|
| real NPC Chinese appears | ✅ | Devon `2398`、`3311` HIT，畫面顯示中文 |
| original English does not visually overlap | ✅ | 使用者確認；TextWidget 只建立一個 |
| correct actor | ✅ | 顯示在 Devon 頭上（`ItemRelativeGump`，owner 不變） |
| correct position | ✅ | 同上 |
| wrap correct | ✅ | `3311` 長句逐字換行、分頁（P3 的換行規則） |
| duration reasonable | ✅ | 使用者確認；見「顯示時間」 |
| speech still works | ⚠️ 程式碼層級 | 語音只用 `_barked`（未改）。遊戲只有 9 個角色有語音檔（`SOUND/E44.FLX` 等），Devon 沒有，無法在本 Phase 實測。移到 P7 |
| localization OFF restores English | ✅ | `launch-dev.bat 2 en` 讀檔只有英文 |
| save/load PASS | ✅ | `ultima8.002` 讀檔正常；存檔中沒有中文 |
| 自言自語 bark 顯示中文時存檔 → 關閉 localization 讀檔 → 顯示英文（v2） | ✅ | 測試 B |

Critical Constraint：`_barked`、語音查詢、Usecode string heap、存檔中的遊戲狀態都保持英文。✅

## Findings

### Observed

1. 正在顯示的 bark 會完整進入存檔（BarkGump 與 TextWidget 各一份文字），證實了 P1 的推論。
2. U8 的語音檔只有 9 個（依角色 shape 編號），大多數 NPC 沒有語音。
3. `Hello, Devon.` 這類尚未翻譯的選項，log 已正確記為 MISS（P4 的修正）。

### Inferred

- 讀檔後的英文 bark 只持續幾秒，對遊玩影響很小。若之後要讓它也顯示中文，需要在存檔中加入 bark ID（改格式）或以英文反查（同一句英文有多個譯文時不唯一）。

### Unknown

- 有語音的 NPC 在 localization 下的語音與字幕同步（P7 驗證）。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `a1a2282aae`）：13 個檔案，+121 / −18
- 主 repo：本報告、`tools/validate/save_text_check.py`、`0402_DEVON.po`（+2 條）、Master Plan 與 HANDOFF
- 本機：`private_test/launch-dev.bat`（`en` 參數）、`scummvm-dev-en.ini`、`extra/u8_zh_TW.mo`

## Regressions

- 477 項單元測試通過。
- localization off：`Item::bark` 的 `displayText` 為空，BarkGump 與 TextWidget 走原本的路徑；`calculateTicks` 的分母與原本相同（TextWidget 的文字就是 `_barked`）。
- TextWidget 的存檔只有在 `setSaveText()` 被呼叫時才不同；其他使用 TextWidget 的 gump 不受影響。

## Risks

1. 有語音的台詞尚未實測（見 Acceptance）。
2. `Localization::bark` 只供測試，讓主角說出任意 NPC 的台詞。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 6（First AskGump Chinese Choice POC）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 5 as required. Phase 6 was not started.
