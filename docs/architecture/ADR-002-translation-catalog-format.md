# ADR-002 — Translation Catalog Format

**狀態：** Accepted（使用者決策，2026-10-06）。正式工具於 Phase 10 實作。

## 背景

Master Plan §29 把翻譯檔格式（PO / TSV / JSON）留到 Phase 10 決定。Phase 2 的抽取示範證明：可以從 `EUSECODE.FLX` 離線抽出全部對話，並依對話流程排列。因此提早確定格式方向，讓 ID 設計（ADR-001）與檔案格式一致。

U7 中文化專案的作法是：以 Exult 工具把 Usecode 反組譯成 `.es` 腳本，翻譯後重新編譯回遊戲。U8 不修改遊戲資料，因此不需要「重新編譯回去」，但保留「依事件分檔、看得到上下文」的翻譯體驗。

## 決策

1. **原始檔格式：gettext PO。**
   - `msgctxt`：ADR-001 的 ID（`bark 0402:0964`、`ask 0402`、`param 040A:varF7`）
   - `msgid`：英文原文或句型（區分大小寫，保留結尾空白）
   - `msgstr`：譯文
   - `#.`：抽取工具產生的上下文，例如「玩家選擇 Who are you? 之後」、參數說明
   - `#,`：狀態旗標（`fuzzy` 等），對應 Master Plan §32 的翻譯狀態
2. **依 Usecode class 分檔**（約 515 個），例如 `localization/zh_TW/dialog/0402_DEVON.po`。條目依對話流程排列。
3. **執行時使用單一編譯檔**（例如 `u8_zh_TW.dat`）。由建置工具檢查並合併所有 PO 檔。引擎不需要內建 PO parser。
4. **英文原文放進 repo**（使用者決策，比照 U7 中文化專案）。
5. **重新抽取時依 ID 合併**（類似 `msgmerge`），既有譯文不會被覆蓋。
6. Excel / CSV 只作為輸出的報表（統計、審稿、術語檢查），不作為原始檔。

## 補充：執行時的編譯檔格式（Phase 4，2026-10-06）

決策 3 的單一編譯檔採用 **gettext MO**，檔名 `u8_<語言>.mo`（例如 `u8_zh_TW.mo`），以 `localization_file` 可改用其他檔名。

- key 為 `msgctxt + "\x04" + msgid`，與 gettext 處理 context 的方式相同；引擎依「context + 英文原文」查表。
- 檔頭 `Language` 必須與設定的語言相符，否則不使用。
- 編譯工具：`tools/catalog/po_compile.py <語言> <PO 檔或目錄>... -o <輸出.mo>`。檢查 `msgctxt` 格式、重複條目、複數條目、檔頭語言；略過未翻譯、fuzzy、過時條目。
- 理由：標準格式，`msgfmt`、Poedit 都能產生，Python `gettext` 可直接讀取驗證；引擎端只需要簡單的讀取程式，不需要 PO parser。
- 引擎在載入時檢查所有 offset 與長度；結構錯誤時整個檔案不使用，個別錯誤條目（非 UTF-8、未知 context 等）則略過。

## 補充：工具鏈與權威檔（Phase 10，2026-10-06）

- 抽取 + 合併：`tools/catalog/u8catalog.py update <語言>` 產生 `localization/<語言>/dialog/CCCC_NAME.po`（394 個），保留既有譯文；英文改變的條目標為 fuzzy；不再出現的條目保留為 obsolete。結果是決定性的。
- 檢查與統計：`check`、`stats`；說明見 `localization/README.md`。
- **權威檔** `localization/<語言>/authority.tsv`（使用者要求）：人名、地名、物品、魔法、生物、稱號、組織的唯一譯名（`keep` = 保留英文、`approved` = 使用譯名）。`terms` 指令自動收集候選詞並保留手動欄位；`check` 依權威檔檢查譯文。
- 新 context：`book` / `scroll` / `grave` / `plaque CCCC:IIII`（讀物 intrinsic 的呼叫點）。
- MO 的 key：context + `\x04` + 英文，英文以遊戲的 CP437 編碼（PO 以 UTF-8 存放）。

## 理由

- 語境：依 NPC 分檔並依流程排列，譯者看得到前後文。
- 版本控制：純文字、檔案小，差異清楚，多人分工時不易衝突。
- 工具：Poedit、Weblate、Crowdin 可直接使用（翻譯記憶、搜尋、fuzzy）。ScummVM 本身的介面翻譯也使用 PO。
- 驗證：佔位符號、控制字元（`~ % * ^`）、標點都容易自動檢查。

## 風險

- 英文原文進 repo 屬於遊戲文字的引用。Master Plan §14 禁止的是原始遊戲資料檔；此項依使用者決策處理，並在 `LICENSES.md`（Phase 14）中說明。
- PO 的 `msgid` 會保留結尾空白，部分編輯器可能自動刪除。建置工具必須檢查 `msgid` 與抽取結果完全一致。
