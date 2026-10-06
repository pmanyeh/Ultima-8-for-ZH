# Phase P7 Report — First Complete Conversation ★

## Result

**PASS** — **Core Localization Architecture is considered proven.**

（語音一項無法在這段對話中實測，見 Acceptance。）

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `5a8b1e7e5b`（本機，未 push；接續 P6 的 `b04657abfb`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），480 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（未修改）
- 遊戲內測試：使用者操作（2026-10-06 17:18，log `private_test/dev-20261006-171824.log`）

## Scope Performed

依 Master Plan §26，完成一段從開始到離開都是繁體中文的對話。使用者的決定：

1. 對話：**Devon 與 Avatar 的第一次見面**（新遊戲一開始就會進入）。
2. 含玩家名字的句子：**在本階段一併處理**（原規劃於 P11）。

| 項目 | 內容 |
|---|---|
| 句型（ADR-001 D3） | `TranslationCatalog` 支援句型：msgid 中的 `{name}`、`{num}`、`{varXX}`、`{call_XXXX}` 可對應任意文字，譯文使用相同的佔位符號（順序可不同） |
| 參數譯文 | `param CCCC:varXX` / `param CCCC:call_XXXX` 條目：同 class 的參數值若有譯文就替換（例如 `stranger ` → 陌生人），否則照原樣顯示；`{name}`、`{num}` 不翻譯 |
| 檢查 | 引擎：譯文的佔位符號與英文不一致 → 略過該條目。編譯工具：同樣檢查（錯誤時中止），並支援 `param` context |
| 翻譯 | `0402_DEVON.po` 改寫為 Devon 第一次見面的完整對話：28 句台詞（4 句句型）、24 個選項，加上 P5/P6 的少數條目，共 57 條 |
| 啟動檔 | `launch-dev.bat new`：開新遊戲（設定檔複本去掉 `lastSave`） |

翻譯原則（POC，正式術語表留到 P10）：

- 專有名詞保留英文：Tenebrae、Lithos、Mordea、Hydros、Bentic、Tempest、Lurker。
- 一般名詞意譯：Sea of Rains → 雨之海、Necromancers → 死靈法師、Titan → 泰坦、Mountain King → 山之王。
- 英文原文全部由抽取結果（`u8extract.py 0402`）產生，不手打。

### 句型比對

```text
英文句型：I am Devon, my strange friend. And I am glad to see you are feeling better, {name}.
遊戲文字：I am Devon, my strange friend. And I am glad to see you are feeling better, Pman.
            → {name} = "Pman"
譯文句型：我是 Devon，我奇特的朋友。很高興看到你好多了，{name}。
顯示文字：我是 Devon，我奇特的朋友。很高興看到你好多了，Pman。
```

- 先查完全相符的條目，沒有才試該呼叫點的句型。
- 佔位符號至少對應一個字元；比對時從最短開始並可回溯，所以名字中含有句型後面的文字（例如 `Dr. Who`）也能正確比對（單元測試）。
- 不符合句型 → SOURCE-MISMATCH，顯示英文。

## Evidence

### 遊戲內：完整對話（使用者操作）

`launch-dev.bat new` → 新遊戲 → Devon 的第一次見面 → 再見 → Devon 自言自語 → 再次對話 → 再見。

```text
localization zh_TW active, 57 entries from u8_zh_TW.mo
Starting New Game (slot -1)...
bark 0402:0633 HIT "Hello there. "                          你好啊。
ask  0402 HIT "Who are you? " / "Goodbye. "
bark 0402:0964 HIT "I am Devon, ... feeling better, {name}." ← 句型
ask  0402 HIT "How do you know my name? " / "Where am I? " / "Goodbye. "
bark 0402:22CF HIT "I am sorry. I did not mean to pry, ..."
bark 0402:0A84 HIT "Why, on the shore, friend, ..."
ask  0402 HIT "What happened to me? " / "Shore of what? " / "Found me? "
bark 0402:1A04 HIT "I am unsure, my friend. ..."
bark 0402:1B1D HIT "Aye, 'tis what we sometimes call the sea. ..."
bark 0402:1C48 HIT "Aye! Not only would it have meant death for you, ..."
bark 0402:1D55 HIT "Ages ago, our people forged a covenant with Lithos ..."
bark 0402:207B HIT "We call him the Mountain King. ..."
bark 0402:21C9 HIT "The Lurker? That is our name for Hydros, ..."
bark 0402:1E3E HIT "Through his Necromancers, ..."
bark 0402:1FA8 HIT "I am amazed at how little you know, friend. ..."
bark 0402:3498 HIT "Farewell, friend Pman, and good luck. You are welcome ..." ← 句型
bark 0402:34FD HIT "I can already see a crowd gathering there on the docks."   ← 對話結束後自言自語
bark 0402:352D HIT "That can mean only trouble."
bark 0215:0098 MISS "rope "                                  ← 使用者查看物品（P8 範圍）
bark 0402:060F HIT "Hello there, Pman."                      ← 再次對話，句型
ask  0402 HIT "Hello, Devon. " / "What should I do? " / "Goodbye. "
bark 0402:235D MISS "Good day. "                              ← 未翻譯（第二次對話的隨機問候）
bark 0402:3311 HIT "Well, I suppose now that you are better, ..."
bark 0402:338E HIT "Farewell, friend Pman, and good luck."   ← 句型
```

第一次見面的對話中：**出現的 15 句台詞全部 HIT（含 2 句句型），所有選項全部 HIT**。再次對話的 4 句中 3 句 HIT（含 2 句句型），`235D` 未在翻譯範圍內。使用者確認畫面全程中文、操作正常。

### 單元測試

```text
Running cxxtest tests (480 tests)....OK!
```

新增 3 項：`test_placeholders`（解析、格式錯誤、`canonicalParam`）、`test_match_template`（單一 / 多個佔位符號、回溯、不符合、空值）、`test_template_lookup`（句型 HIT、參數譯文、無參數譯文時保留原值、佔位符號不一致的條目略過、句型只屬於自己的呼叫點）。`test_canonical_context` 加入 `param`。

### 編譯工具

```text
private_test/extra/u8_zh_TW.mo: 57 entries (4 templates) from 1 files, 12478 bytes
```

字集：`font_coverage.py` → 464 個不同字元，missing 0。

## Acceptance（Master Plan §26）

| 必測項目 | 結果 | 說明 |
|---|---|---|
| multiple pages | ✅ | `1A04`、`1FA8`、`21C9`、`3498` 等長句分頁顯示 |
| repeated text | ✅ | `Goodbye.` 在每一輪選項中出現，每次都是「再見。」 |
| same English appearing in different context | ✅ | `Farewell, friend {name}, and good luck.` 在 `3498`（第一次，較長）與 `338E`（第二次）兩個呼叫點各自比對、各自顯示正確的譯文；`Hello there.` 系列在 `0633`（不認識）與 `060F`（認識，含名字）分開 |
| conversation bullet | ✅ | 「● 你是誰？」等，AskGump 的 `@` 圓點 |
| click target | ✅ | 使用者確認 |
| speech | ⚠️ 無法實測 | 遊戲只有 9 個角色有語音檔（`SOUND/E44.FLX` 等），Devon 沒有。程式碼層級：語音只使用 `_barked`（P5）。列為 §49 #18 |
| text timing | ✅ | 使用者確認 |
| closing Gump | ✅ | 再見後對話框關閉，Devon 自言自語（`34FD`、`352D`）照常出現 |
| restarting conversation | ✅ | 再次對話：`060F`「你好啊，Pman。」、分支正常 |

> 玩家可以從對話開始到離開，全程使用繁中而不破壞任何 conversation logic。✅

## Findings

### Observed

1. 新遊戲一開始就直接進入與 Devon 的對話；對話中無法存檔，所以測試第一次見面一律從新遊戲開始。
2. 原本規劃在 P11 的句型比對，以 ADR-001 D3 的設計直接實作即可運作；Devon 的 4 個句型全部在遊戲中 HIT。
3. 抽取工具列出的選項並不完整：`Sea of Rains? `、`Tenebrae? `、`What is the lovelier place? ` 等只出現在「when answer is」中（由其他方式加入選項清單）。本次已依「when answer is」補上，P10 的抽取工具需要處理。

### Inferred

- 參數譯文（`param`）的實際效果要等有 `{varXX}` / `{call_XXXX}` 的 NPC（例如 Orlok `040A`）才能在遊戲中驗證；目前由單元測試覆蓋。

### Unknown

- 有語音的 NPC 的字幕與語音同步（§49 #18）。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `5a8b1e7e5b`）：4 個檔案，+324 / −22
- 主 repo：本報告、`tools/catalog/po_compile.py`（`param`、佔位符號檢查）、`localization/zh_TW/dialog/0402_DEVON.po`（57 條）、Master Plan 與 HANDOFF
- 本機：`private_test/launch-dev.bat`（`new`）、`extra/u8_zh_TW.mo`

## Regressions

- 480 項單元測試通過。
- localization off：查表不會被呼叫，行為與原版相同（P4–P6）。
- 既有的完全相符查表優先；只有完全相符失敗時才試句型，所以原有條目的結果不變。

## Risks

1. 句型比對對每個呼叫點逐一嘗試，句型多時效能需留意。目前每個呼叫點通常只有 1 個句型，且只在 bark 時執行一次。
2. 譯名尚未統一（術語表在 P10），本次的意譯名詞可能之後調整。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 8（Remaining Text Surface Inventory）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 7 as required. Phase 8 was not started.
