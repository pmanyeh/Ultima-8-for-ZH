# Phase P10 Report — Extraction & Translation Catalog Toolchain

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `47541ad4bb`（本機，未 push；接續 P9 的 `cb69291575`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），481 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（唯讀）
- 遊戲內測試：使用者操作（2026-10-06 23:30）

## Scope Performed

依 Master Plan §29（格式已由 ADR-002 決定：PO，依 class 分檔）。

| 項目 | 內容 |
|---|---|
| 抽取工具 | `tools/extract/u8extract.py` 擴充：書（`Book::read`）、捲軸、墓碑、牌匾；對話選項另外收集「被比對的答案」（補上 §49 #19 漏列的選項）；每個條目附上流程位置（event、在哪個答案之後）；文字以遊戲的 CP437 解碼 |
| 翻譯檔 | `tools/catalog/u8catalog.py update`：全部 394 個有文字的 class → `localization/zh_TW/dialog/CCCC_NAME.po`（共 6,552 條），依對話流程排列 |
| 合併 | 同 context + 英文 → 保留譯文；同呼叫點但英文改變 → 保留為 fuzzy（附 `#|` 舊英文）；`--tm` 相同英文已有譯文 → 帶入為 fuzzy；不再出現的條目 → 保留為 obsolete（`#~`）；譯者註解保留 |
| 檢查 | `u8catalog.py check`：context 格式、句型佔位符號、**過時條目**（英文已不在遊戲中）、CP437 可表示、控制字元（`~ * % ^ @ &` tab）數量、權威檔譯名、字型缺字 |
| 統計 | `u8catalog.py stats`：依種類的條目數 / 字元數 / 完成率；重複英文與翻譯不一致的報告；`--csv` 每個檔案的報表 |
| 權威檔 | `u8catalog.py terms` → `localization/zh_TW/authority.tsv`（使用者要求）：人名、地名、物品、魔法、生物、稱號、組織的唯一譯名，自動收集候選詞並保留手動欄位 |
| 編譯工具 | `po_compile.py`：新增 `book` / `scroll` / `grave` / `plaque` context；MO 的 key 以 CP437 編碼英文（與遊戲的 byte 一致） |
| 引擎 | 書、捲軸顯示譯文；墓碑、牌匾為英文雕刻 + 中文字幕（方案 A）；主控台 `Localization::read <kind> <class>:<ip>` |
| 說明文件 | `localization/README.md`：翻譯檔格式、要保留的符號、流程、權威檔 |
| POC 譯文 | 書（衛兵日誌）、捲軸（購物清單）、墓碑 2 個、牌匾 2 個。翻譯檔合計 75 條 |

## 抽取結果

| 種類 | 條目 | 說明 |
|---|---|---|
| bark | 4,528 | 常值 4,413、句型 115；另有 5 個呼叫點無法解析（PYROS、SORCERER ×2、METHOD ×2，與 P2 相同） |
| ask | 1,775 | 「加入選項」941 + 「被比對的答案」834（後者可能包含少數不是選項的字串比較，未使用的條目不影響遊戲） |
| param | 11 | 句型參數的值（例如 Orlok 的 `stranger `） |
| book / scroll / grave / plaque | 86 / 22 / 67 / 63 | |
| ui | 12 | 介面文字（P9） |
| **合計** | **6,564** | 英文約 **522,000 字元**；目前完成 1.1%（以英文字元計） |

同一句英文出現在多個 context：506 句、1,433 個條目（例如 `Goodbye. `、`Who are you? `）。可用 `update --tm` 帶入既有譯文。

權威檔：725 個詞（物品 382、其他專有名詞 235、人名 43、稱號 34、魔法 27、地名 2、組織 2），其中 8 個保留英文、6 個已核定（Avatar → 聖者、Sea of Rains → 雨之海、Necromancer(s) → 死靈法師、Titan → 泰坦、Mountain King → 山之王），其餘待決定。分類為自動猜測，需要人工確認（例如 Bloodwatch、Firstebb 是時段名稱，被猜成人名）。

## Evidence

### 決定性與 ID 穩定

- `update` 連續執行兩次：395 個 PO 檔的 MD5 完全相同；第二次寫入 0 個檔案。
- `terms` 連續執行兩次：`authority.tsv` 相同（修正大小寫排序後）。
- 既有 57 條 Devon 譯文在改為自動產生後全部保留，編譯結果與之前**位元組完全相同**（69 條）。
- context 由「class + 呼叫指令的 IP」組成，只取決於遊戲資料；遊戲資料不變，ID 就不變。

### 檢查工具（負面測試）

以刻意錯誤的資料測試，全部被抓到：

```text
WARNING: glossary: 'Tenebrae' -> 'Tenebrae' not used
WARNING: glossary: 'Sea of Rains' -> '雨之海' not used
WARNING: control character '~': English 2, translation 1
ERROR: stale: bark 0402:0F0B 'a~b~c' is not in the game text
ERROR: placeholders differ: msgid ['name'], msgstr []
```

實際的翻譯檔：`0 errors, 0 warnings`。

### 遊戲內（使用者操作）

| 測試 | 結果 |
|---|---|
| `Localization::read book 0592:442C` | ✅ 中文衛兵日誌，兩頁、換行正常 |
| `Localization::read scroll 057A:00DE` | ✅ 中文購物清單 |
| `Localization::read grave 00C5:0D18` | ✅ 英文墓碑 + 中文字幕 |
| `Localization::read plaque 0257:0149` | ✅ 英文牌匾 + 中文字幕 |
| 與 Devon 對話（翻譯檔改為自動產生後的回歸） | ✅ |

### 單元測試

```text
Running cxxtest tests (481 tests)....OK!
```

新增 `test_readers`；`test_canonical_context` 加入 book / scroll / grave / plaque。

## Acceptance（Master Plan §29）

| 項目 | 結果 | 證據 |
|---|---|---|
| repeat extraction deterministic | ✅ | 兩次執行 MD5 相同 |
| IDs stable | ✅ | context 只由遊戲資料決定；既有譯文全部保留 |
| no duplicate-ID conflicts | ✅ | 抽取時以（context, 英文）去重；編譯工具對重複條目報錯 |
| same-English/different-context handled | ✅ | 各 context 各自一個條目；`stats` 報告重複與不一致；`--tm` 帶入 |
| control characters preserved | ✅ | `msgid` 原樣保留；`check` 比對控制字元數量 |
| zero proprietary binary copied into repo | ✅ | repo 中沒有遊戲檔案；英文文字依使用者決策放進 repo（ADR-002） |

Required Tools：extract ✅（`update`）· validate ✅（`check`）· coverage ✅（`stats`）· duplicate detector ✅（`stats`）· control-token validator ✅（`check`）· missing translation report ✅（`stats --csv`）。

## Findings

### Observed

1. **很多選項不是以「加入選項」的方式出現**：Devon 的選項從 29 個增加到 46 個（例如 `Sea of Rains? `、`Tenebrae? `）。改為同時收集「被比對的答案」後補齊。
2. **試劑名稱是動態組合的**（`ERTHREAG` 等）：抽取結果把所有分支串在一起（`{num} vial vials of blood pile piles of ...`），需要 P11 處理（單複數、數量）。
3. 遊戲文字中有 4 句含 CP437 字元（德文、法文），PO 以 UTF-8 存放、MO 以 CP437 編碼 key，與遊戲的 byte 一致。
4. 權威檔的自動分類只能當起點：時段名稱（Bloodwatch、Firstebb…）、稱號與人名的界線都需要人工確認。

### Inferred

- 翻譯量以字元計：台詞約 361,000、書約 114,000、選項約 35,000、其他約 12,000。建議依遊戲進度（地區、NPC）分批翻譯，並先確定權威檔中的高頻詞（Lithos 123 次、Mordea 124 次、Tempest 100 次、Sorcerer 105 次等）。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `47541ad4bb`）：11 個檔案，+147 / −15
- 主 repo：`tools/extract/u8extract.py`、`tools/catalog/u8catalog.py`（新）、`tools/catalog/po_compile.py`、`localization/zh_TW/dialog/*.po`（394 個）、`localization/zh_TW/authority.tsv`（取代 `glossary.tsv`）、`localization/README.md`、本報告、Master Plan 與 HANDOFF

## Regressions

- 481 項單元測試通過。
- 翻譯檔改為自動產生後，編譯結果與 P9 相同（再加上本 Phase 的 6 條 POC）。
- localization off：書、捲軸、墓碑、牌匾走原本的路徑（`translateCallSite` 不啟用時回傳原文；書的英文修正照常）。

## Risks

1. 「被比對的答案」可能包含少數不是選項的字串，翻譯時會多出一些不會顯示的條目。
2. 權威檔的候選詞仍有雜訊，需要人工整理後才能作為正式譯名表。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 11（Dynamic Strings / Pagination / Timing）。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 10 as required. Phase 11 was not started.
