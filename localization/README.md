# 翻譯檔說明（Ultima VIII 繁體中文化）

## 目錄

| 路徑 | 內容 |
|---|---|
| `zh_TW/dialog/CCCC_NAME.po` | 每個 Usecode class 一個檔（共 394 個）：NPC 台詞、對話選項、查看物品時的名稱、書、捲軸、墓碑、牌匾。條目依對話流程排列 |
| `zh_TW/ui/engine.po` | 引擎介面文字（主選單、離開確認等） |
| `zh_TW/authority.tsv` | **權威檔**：人名、地名、物品、魔法、生物、稱號、組織的唯一譯名 |

PO 檔可以用 Poedit 等工具編輯，也可以直接用文字編輯器。

## 條目格式

```po
#. event 01 (use (talk)), after "Who are you? "
#. sentence template: keep the {placeholders}
msgctxt "bark 0402:0964"
msgid "I am Devon, my strange friend. And I am glad to see you are feeling better, {name}."
msgstr "我是 Devon，我奇特的朋友。很高興看到你好多了，{name}。"
```

- `msgctxt`：文字出現的位置（ADR-001）。**不要修改。**
  - `bark CCCC:IIII` 台詞與查看名稱、`ask CCCC` 對話選項、`book` / `scroll` / `grave` / `plaque CCCC:IIII` 書、捲軸、墓碑、牌匾、`param CCCC:varXX|call_XXXX|partN` 句型參數的值、`ui` 介面文字
- `msgid`：英文原文，**一個字都不能改**（包含結尾空白）。遊戲以完全相同的英文比對。
- `msgstr`：譯文。空白 = 尚未翻譯（遊戲顯示英文）。
- `#.` 註解：抽取工具產生的上下文，每次更新會重寫。
- `# ` 註解：譯者自己的備註，更新時保留。
- `#, fuzzy`：待確認的譯文（英文改過、或由翻譯記憶帶入）。**遊戲不會使用 fuzzy 條目**，確認後刪掉 `fuzzy` 標記。

### 要保留的符號

| 符號 | 意思 |
|---|---|
| `{name}` `{num}` `{varXX}` `{call_XXXX}` `{partN}` | 句型的佔位符號：遊戲執行時換成玩家名字、數字、參數。譯文必須用到同樣的佔位符號（順序可以不同） |
| `~` | 換行 |
| `*` | 換頁（台詞）或換行（墓碑、牌匾的英文雕刻）。墓碑與牌匾的譯文是字幕，不必跟著英文換行 |
| `%` `^` `@` `&` | 其他排版控制字元，數量要與英文一致 |

### 動態組合的句子（Phase 11）

- **同一個 `msgctxt` 可以有多個條目**：遊戲用分支組出不同句子時（單複數、物品種類…），每一種結果各一條，例如 `bark 018B:0300` 的 `{num} vial of blood`、`{num} vials of blood`、`{num} pile of wood`…。中文沒有單複數，兩條可以譯成一樣。
- **參數的值**（`param`）：`{varXX}`、`{call_XXXX}`、`{partN}` 的每個可能值各有一條，例如 `param 040A:call_0BCF` 的 `Blackwine ` → `黑酒`。值的英文常有結尾空白，**譯文不要帶空白**，句型譯文自行決定標點與空白。沒有翻譯的值以英文顯示；`{name}`（玩家名字）與 `{num}`（數字）不翻譯。
- **`{partN}`**：組合太多（例如魔杖的「種類 × 法術 × 次數」、時間 focus 的「時辰 × 星期 × 月份」）時，句子拆成片段，各片段是 `param CCCC:partN`。譯文可以調整順序：`{part1}of {part2}with {num} uses remaining` → `{part2}{part1}（剩 {num} 次）`。
- 同一位置有多個句型都符合時，遊戲採用固定文字最多的那一個；完全相同的整句條目優先於句型。

### 長度與顯示時間

- 台詞框 194×55 px：英文一頁 5 行，中文（Cubic 11、行距 18 px）一頁 3 行、每行約 16 字。超過就自動分頁，不必手動加 `*`。
- 顯示時間依字數計算：一個中文字算 3 個英文字母（與英文句子的顯示時間相當）。玩家也可以點擊翻頁。
- 量測全部譯文的頁數與寬度：`tools/catalog/measure.py`（說明在檔案開頭）。

## 流程

```bash
# 1. 從遊戲資料重新抽取並合併（不會覆蓋譯文）
python tools/catalog/u8catalog.py update zh_TW
#    --tm：相同英文已有譯文時，自動帶入為 fuzzy

# 2. 更新權威檔的候選詞（保留手動填寫的欄位）
python tools/catalog/u8catalog.py terms zh_TW

# 3. 檢查（佔位符號、控制字元、過時條目、權威檔、字型缺字）
python tools/catalog/u8catalog.py check zh_TW --font private_test/extra/Cubic_11.ttf

# 4. 進度統計（--csv 輸出每個檔案的報表）
python tools/catalog/u8catalog.py stats zh_TW

# 5. 編譯成遊戲讀取的翻譯檔
python tools/catalog/po_compile.py zh_TW localization/zh_TW -o private_test/extra/u8_zh_TW.mo
```

遊戲內檢查：`private_test/launch-dev.bat`，主控台（`Ctrl+Alt+D`）：

- `Localization::read book|scroll|grave|plaque <class>:<ip>`：直接開啟書、捲軸、墓碑、牌匾
- `Localization::bark <class>:<ip>`：讓主角說出某句台詞
- `Localization::say <class>:<ip> <英文>`：讓主角以該位置說出任意英文（測試句型與參數），例如 `Localization::say 040A:1F16 Greetings again stranger . Will ye be havin' another Blackwine ?`；要保留特殊空白時把英文放在雙引號中
- `Localization::guardianBark <1-23>`：Guardian 的嘲諷（有語音），檢查語音與字幕
- `Localization::info`：翻譯檔狀態

## 權威檔（`authority.tsv`）

欄位：`category`、`english`、`translation`、`status`、`count`、`example`、`note`（tab 分隔）。

| status | 意思 |
|---|---|
| `keep` | 保留英文（目前的專有名詞，例如 Tenebrae、Lithos） |
| `approved` | 使用 `translation` 的譯名 |
| `proposed` | 建議，尚未確定 |
| `todo` | 尚未決定 |

- 候選詞由 `terms` 指令自動收集（查看名稱、魔法的 focus、全部文字中反覆出現的大寫名詞），`category` 是猜測的，需要人工確認。
- `check` 會對 `keep` 與 `approved` 的詞檢查：英文中出現這個詞，譯文卻沒有使用規定的譯名 → 警告。
- 新增或修改譯名後，重跑 `check` 找出需要一起修改的譯文。
