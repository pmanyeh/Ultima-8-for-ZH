# ADR-001 — Translation Identity

**狀態：** Accepted（Phase 2，2026-10-06）  
**依據：** [docs/research/u8-text-pipeline.md](../research/u8-text-pipeline.md)、Phase 2 spike（`scummvm-src` 分支 `exp/u8-p2-identity-spike`）

---

## 背景

Ultima VIII 的 Usecode 以英文字串「內容」決定對話分支（`strcmp`、slist union/sub，見 research §2–3），而且同一句英文會在不同語境重複出現（11,238 個 literal 中只有 5,980 種不同的文字）。因此：

- 翻譯不能寫回 string heap（會改變遊戲邏輯）→ 採用 presentation-time localization。
- 不能只用英文原文當 key（無法區分語境）。
- 字串在送到 Gump 之前會被複製 1–3 次，`push string`（0x0D）的位置資訊無法自然傳到顯示端。

## 決策

### D1. NPC 台詞（bark）

```text
ID = bark:<class>:<IP of the Item::bark calli>      例：bark 0402:0633
```

- 在 `Item::I_bark` 執行時，由 `Kernel::getRunningProcess()` 取得 `UCProcess` 的 `classId` 與 `ip`。IP 要等該指令執行完才寫回，所以此時正好指向 `calli` 本身（research §5 Q2）。
- 不需要 string provenance，也不需要修改 UCMachine。

### D2. 對話選項（ask）

```text
ID = ask:<呼叫 Item::ask 的 class>:<英文答案原文>    例：ask 0402 "Who are you? "
```

- 遊戲本身就以內容辨識答案，所以同一個 class 裡英文相同的答案在邏輯上就是同一個選項。這個 key 的區分程度與遊戲邏輯完全一致。
- 英文比對**區分大小寫、保留結尾空白**（`"Who are you? "`），與 Usecode 的 `strcmp` 相同。

### D3. 動態句子（template）

```text
同一個 bark ID，英文以句型表示：
  "Greetings again {varF7}. Will ye be havin' another {call_0BCF}?"
參數類型：
  {name}        getName()（玩家名字，不翻譯）
  {num}         numToStr()
  {varXX}       作為參數的 string local（例：stranger / 玩家名字）
  {call_OOOO}   同 class 函式的回傳字串（例：酒名）
參數值另有翻譯條目：
  param:<class>:<varXX|call_OOOO>  "stranger "  →  "陌生人"
```

執行時：用 bark ID 找到句型 → 拿完整英文去比對句型的固定部分，取出參數 → 參數若有翻譯就替換 → 填入譯文句型。比對失敗就顯示英文（D5）。

### D4. 不改動的部分（不變條件）

以下內容永遠保持英文原文：

- UCMachine string heap 與所有 string ID
- `AskGump::_answers`、`_processResult`
- `BarkGump::_barked`（語音比對、顯示時間計算、存檔）

譯文只交給 `TextWidget` / `ButtonWidget` 顯示。

### D5. Fallback（一律 fail open）

| 情況 | 行為 |
|---|---|
| 沒有對應條目（MISS） | 顯示英文 |
| ID 命中但英文不符（SOURCE-MISMATCH） | 顯示英文，並記錄 log |
| 翻譯表格式錯誤的行 | 忽略該行，並記錄 warning |
| 找不到翻譯表 | 全部顯示英文 |
| localization 關閉 | 與原版完全相同的路徑 |
| **CJK 字型載入失敗** | **必須自動停用翻譯**（否則 UTF-8 會被 shape font 畫成亂碼）。spike 尚未實作，列為 Phase 4 必要項目。 |

## 驗證（Phase 2 Acceptance）

| 項目 | 結果 | 證據 |
|---|---|---|
| 同一段對話，兩次執行得到相同 ID | **PASS** | spike log：多次獨立執行，`0402:0633`、`0402:060F`、`0402:0A84`、`0402:1A04`、`0402:1B1D` 的 ID 都相同 |
| 靜態抽取的 ID 與執行期 ID 一致 | **PASS** | POC 翻譯表的 ID 全部由反組譯工具離線算出，遊戲中全部 HIT |
| 相同英文、不同語境 → 不同 ID | **PASS** | 382 句英文出現在 1,038 個呼叫點，各自有 ID，例如 `"Farewell. "` 由 9 個 NPC 說出 |
| AskGump 穩定 ID | **PASS** | `ask 0402 "Who are you? "` 等條目多次執行都 HIT；點擊中文「再見。」後進入原始的 Goodbye 分支 |
| 動態句子策略 | **已定義** | D3；抽取工具自動還原 113 個句型，全遊戲 bark 4,526 個中只有 5 個無法解析（0.1%） |
| Fallback 語意 | **已定義** | D5 |
| 不改變遊戲邏輯 | **PASS** | 只有顯示文字被替換；Usecode 與 string heap 未受影響 |

## 後果

**好處**
- 不需要 provenance sidecar，UCMachine 的熱點路徑不用修改。
- ID 可以完全離線產生，翻譯不需要玩遊戲；遊玩只用來做 QA。
- 遊戲資料版本固定，抽取結果可以重現。

**代價與風險**
1. 同一句英文出現在多個呼叫點時，要翻譯多次。對策：PO 工具的翻譯記憶，或建置工具自動帶入相同英文的既有譯文（仍可個別覆寫）。
2. 若同一個呼叫點會 bark 多種字串（經由變數的情況），ID 不唯一。對策：條目同時比對英文（D5 的 SOURCE-MISMATCH）。必要時可在同一 ID 下列出多個英文版本。
3. 由其他 class 代為發話的情況，例如共用的 `METHOD`（`057C`），ID 屬於代為發話的 class，而不是 NPC 本身。對話脈絡要由抽取工具補上。
4. 自言自語的 bark 會把 `TextWidget::_text`（顯示文字）寫進存檔。需要在 Phase 4/5 決定：讀檔時以 `_barked` 重建顯示文字，或接受存檔中有譯文。

## 未採用的方案

| 方案 | 不採用的理由 |
|---|---|
| 修改 string heap 的內容 | 會改變 `strcmp` 結果與遊戲邏輯；中文會進入存檔與語音比對 |
| 只用英文原文當 key | 1,913 種文字重複出現，無法區分語境 |
| `push string`（0x0D）的 literal offset + provenance sidecar | 要在 duplicate、copyList、concat 全部傳遞 provenance，侵入性高；同一答案又有多個 offset |
| 只用 `ask` 的呼叫點 | Devon 所有輪次共用同一個呼叫點（`0402:08C2`），無法區分答案 |
