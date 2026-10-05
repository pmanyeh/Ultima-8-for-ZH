# Phase P1 Report — Text Architecture Audit

## Result

**PASS**

詳細研究內容見 [docs/research/u8-text-pipeline.md](../research/u8-text-pipeline.md)。

## Environment

- Repository: `scummvm-src/`（upstream `master` @ `71cb05b1c03aa6bdcd34f78c20cef12c10067ba5`，working tree clean）
- Builds:
  - `build-scummvm/`（P0 baseline）
  - `build-trace/`（Debug x64，編譯參數 `CL=/DDEBUG_USECODE`，原始碼未修改）
- Compiler: VS 2026 / MSVC 14.51.36231
- Game data: GOG Ultima VIII Gold Edition, English

## Scope Performed

1. 原始碼追蹤：UCMachine → intrinsics → BarkGump / AskGump → TextWidget / ButtonWidget → TTFont；以及存檔、語音、顯示時間相關程式碼。
2. 靜態 Usecode 反組譯：515 個 class、0 次失去同步、923 個 event 進入點全部對齊。
3. 執行期 Usecode trace：使用者與 Devon 完成一段對話（Who are you → Where am I → What happened to me → The Lurker's domain → Goodbye）。
4. 存檔分析：對話結束後的存檔。
5. 全遊戲普查：bark、ask、concat、strcmp 的用法。

## Acceptance（Master Plan §20）

- [x] one NPC line fully traced：靜態 `"Hello there. "`（`0402:061F` → calli `0402:0633`）與動態 `"I am Devon… " + getName()`
- [x] one AskGump answer fully traced：`"Who are you? "` 清單建立（`0402:083C`）→ `ask`（`0402:08C2`）→ AskGump → 按鈕 index → `_processResult` → `strcmp`（`0402:08E9`）→ 分支
- [x] string lifetime understood：每個複製點都已列出（research §3）
- [x] save implications documented（research §4）
- [x] speech implications documented（research §4.4）
- [x] candidate translation hook listed（research §7.1、§7.3）
- [x] alternative hook listed（research §7.2、§7.4）
- [x] no implementation：ScummVM 原始碼與遊戲資料皆未修改

## Files Changed

- 新增 `docs/research/u8-text-pipeline.md`
- 新增 `docs/reports/P1-text-architecture-audit.md`
- 新增 `tools/diagnostics/u8dis.py`（唯讀研究用反組譯工具）
- `private_test/launch-trace.bat`（本機，不進版控）
- `scummvm-src/build-trace/`（被 gitignore 的建置輸出）

## Key Findings

1. **Usecode 以英文字串「內容」決定對話分支**（`strcmp`、slist union/sub）。中文絕不能進入 string heap，presentation-only 原則有實證支持。
2. **Bark 的最佳 ID 候選是 intrinsic 呼叫點**（`class:calli offset`）。全遊戲 96.7% 的 bark 呼叫點與 literal 一對一，其餘是動態句型。
3. **Ask 的最佳 ID 候選是「呼叫 ask 的 class + 英文答案」**。因為遊戲本身就用內容辨識答案，這個 key 不會比遊戲邏輯更粗。
4. **對話期間無法存檔**（原版設計：`setAvatarInStasis`）。對話用的 AskGump 和 BarkGump 不會進存檔；自言自語 bark 的 `TextWidget::_text` 則會。
5. **語音以英文 `_barked` 前綴比對**，顯示時間以 byte 長度比例計算，所以 `_barked` 必須保持英文，Phase 11 需要重新設計時間計算。
6. Master Plan 有 5 項描述需要修正（research §8），其中最重要的是 §9 的 `@`，以及 §5 / §7 的 ID 來源。

## Regressions

無，沒有修改任何程式碼。

## Risks

- 經由變數 bark 的 58 個呼叫點，可能是「同一呼叫點、多種字串」，可能削弱呼叫點 ID 的唯一性。
- `TextWidget` 會把顯示文字存進存檔，Phase 2 必須明確決策。

## Blockers

無。

## Recommendation

1. 審閱 research §7 的兩個候選 ID 方案，以及 §8 對 Master Plan 的修正建議。
2. Phase 2 加入一個「最小、可移除」的驗證實驗：在 `I_bark` / `I_ask` 印出 running process 的 `classId:ip`，確認兩次執行的 ID 一致。這會是第一次修改原始碼，需要你同意，且只放在實驗分支。

## Next Phase Readiness

**READY**：等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 1 as required. Phase 2 was not started.
