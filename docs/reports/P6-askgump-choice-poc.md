# Phase P6 Report — First AskGump Chinese Choice POC ★

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `b04657abfb`（本機，未 push；接續 P5 的 `a1a2282aae`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），477 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（未修改）
- 遊戲內測試：使用者操作（2026-10-06 16:50–16:53）

## Scope Performed

依 Master Plan §25 與「v2：P6 工作項目」，讓玩家的對話選項以繁體中文顯示，同時完全保留 Usecode 的字串 identity。

| 項目 | 內容 |
|---|---|
| 掛點 | `Item::I_ask` 以 running process 的 class 查每個選項的譯文，傳給 `AskGump(owner, answers, displayAnswers)` |
| `AskGump::_displayAnswers` | 只用來產生按鈕文字 `"@ " + 譯文`，不寫入存檔；`_answers`（string ID）不變 |
| 回傳值 | `ChildNotify` 仍以按鈕 index 取 `_answers` 的 string ID 作為 `_processResult`（未修改） |
| 字型檢查（§49 #17） | 對話字型不能畫 UTF-8 → 全部選項顯示英文並寫 warning |
| 存檔 | `ButtonWidget::setSaveText()` → 其 TextWidget 存英文 `"@ " + 原文`（沿用 P5 的 `TextWidget::setSaveText`） |
| POC 翻譯 | 新增 `Hello, Devon.`、`What should I do?` 兩個選項（這個存檔實際會出現），共 21 條 |

## 設計決定

### `AskGump::loadData` 不需要掛點

v2 工作項目原本規劃在 `loadData` 重建按鈕時也替換文字，並在存檔中記錄 class。實際檢查 `loadData` 後發現：按鈕（ButtonWidget 與其 TextWidget）本身就是存檔中的子 gump，`loadData` 只是重新排列它們，並不從 string heap 重建文字。

因此採用與 P5 相同的策略：按鈕存檔時寫入英文，讀檔後該次選項以英文顯示。存檔格式不變，也不需要記錄 class。而且對話期間無法存檔（`setAvatarInStasis`），實際上不會發生。

### 譯文由 `I_ask` 查好再傳入

與 P5 的 bark 一致：gump 不依賴 `Localization`，只接收「要顯示的文字」。localization 關閉時傳入空陣列，AskGump 走原本的路徑。

### 按鈕寬度與點擊範圍

不需要額外處理：原版的排版就是依各按鈕實際的 `getDims()` 排列（每列 160px 換行），ButtonWidget 的大小取自其 TextWidget，所以中文選項的寬度與點擊範圍會自動正確。使用者確認反白與點擊都正常。

## Evidence

### A. 中文選項與分支（`launch-dev.bat 1`，log `dev-20261006-165043.log`）

```text
[U8-L10N] bark 0402:060F MISS src="Hello there, Pman."
[U8-L10N] ask 0402 HIT src="Hello, Devon. "          → ● 你好，Devon。
[U8-L10N] ask 0402 HIT src="Goodbye. "               → ● 再見。
[U8-L10N] bark 0402:235D MISS src="Good day. "        ← 點「你好，Devon。」→ 原本的 Hello 分支
[U8-L10N] ask 0402 HIT src="What should I do? "      → ● 我該怎麼做？
[U8-L10N] ask 0402 HIT src="Goodbye. "
[U8-L10N] bark 0402:3311 HIT src="Well, I suppose ..."  ← 點「我該怎麼做？」→ 原本的分支
[U8-L10N] ask 0402 HIT src="Goodbye. "
[U8-L10N] bark 0402:338E MISS src="Farewell, friend Pman, and good luck."  ← 點「再見。」→ 原本的 Goodbye 分支
```

每個中文選項後出現的 bark 都屬於該選項在 Usecode 中的分支（`u8extract.py 0402`）：

| 點擊的中文選項 | 英文原文 | Usecode 分支中的 bark | 實際出現 |
|---|---|---|---|
| 你好，Devon。 | `Hello, Devon. ` | `235D`+`2398` 或 `23CA`（隨機） | `235D`（第 1 次）、`23CA`（第 2 次） |
| 我該怎麼做？ | `What should I do? ` | `3120` 或 `3311` | `3311` |
| 再見。 | `Goodbye. ` | `338E` / `3498` | `338E` |

### B. 英文模式對照（`launch-dev.bat 1 en`，log `dev-20261006-165134.log`）

使用者以相同順序點選英文選項，Devon 的回答與 A 相同。log 沒有任何 `[U8-L10N]` 訊息（localization off）。

### C. 存檔與讀檔

- 第 3 格（`ultima8.003`）在 B 的英文對話結束後存檔。
- 以中文模式讀取（`launch-dev.bat 3`，log `dev-20261006-165226.log`，`Starting New Game (slot 3)`）：選項顯示中文，分支正常（`Hello, Devon.` → `23CA`、`What should I do?` → `3311`、`Goodbye.` → `338E`）。
- `save_text_check.py saves/ultima8.003` → `OK: no CJK text in the save`。中文模式的存檔已在 P5 的 `ultima8.002` 驗證。

## Acceptance（Master Plan §25）

| 項目 | 結果 | 證據 |
|---|---|---|
| both Chinese | ✅ | 「你好，Devon。」「我該怎麼做？」「再見。」 |
| button dimensions correct | ✅ | 使用者確認；按鈕大小取自實際文字 |
| hitboxes correct | ✅ | 使用者確認反白與點擊範圍 |
| Option A triggers original A branch | ✅ | 你好，Devon。 → `235D` / `23CA` |
| Option B triggers original B branch | ✅ | 我該怎麼做？ → `3311` |
| returned string identity unchanged | ✅ | `_answers` 與 `ChildNotify` 未修改；分支與英文模式相同 |
| English mode works | ✅ | B |
| save/load works | ✅ | C |

Critical Invariant：中文顯示文字不會成為 game logic 的回傳值。✅

## Findings

### Observed

1. `AskGump::loadData` 不從 string heap 重建按鈕文字，而是使用存檔中的按鈕子 gump。因此只需在存檔時寫入英文，不需要第二個掛點。
2. Devon 對 `Hello, Devon.` 的回答是隨機的（`235D`+`2398` 或 `23CA`），測試時兩種都出現了。

### Inferred

- 其他使用 ButtonWidget 顯示遊戲文字的地方（P8 的其他 surface）可以沿用 `setSaveText()`。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `b04657abfb`）：5 個檔案，+41 / −7
- 主 repo：本報告、`0402_DEVON.po`（+2 條）、Master Plan 與 HANDOFF

## Regressions

- 477 項單元測試通過。
- localization off：`displayAnswers` 為空陣列，按鈕文字與原版相同，不呼叫 `setSaveText()`。
- `ButtonWidget::setSaveText()` 只有 AskGump 在顯示譯文時呼叫，其他 ButtonWidget 不受影響。

## Risks

無新的風險。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 7（First Complete Conversation）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 6 as required. Phase 7 was not started.
