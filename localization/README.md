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
  - `bark CCCC:IIII` 台詞與查看名稱、`ask CCCC` 對話選項、`book` / `scroll` / `grave` / `plaque CCCC:IIII` 書、捲軸、墓碑、牌匾、`param CCCC:varXX` 句型參數的值、`ui` 介面文字
- `msgid`：英文原文，**一個字都不能改**（包含結尾空白）。遊戲以完全相同的英文比對。
- `msgstr`：譯文。空白 = 尚未翻譯（遊戲顯示英文）。
- `#.` 註解：抽取工具產生的上下文，每次更新會重寫。
- `# ` 註解：譯者自己的備註，更新時保留。
- `#, fuzzy`：待確認的譯文（英文改過、或由翻譯記憶帶入）。**遊戲不會使用 fuzzy 條目**，確認後刪掉 `fuzzy` 標記。

### 要保留的符號

| 符號 | 意思 |
|---|---|
| `{name}` `{num}` `{varXX}` `{call_XXXX}` | 句型的佔位符號：遊戲執行時換成玩家名字、數字、參數。譯文必須用到同樣的佔位符號（順序可以不同） |
| `~` | 換行 |
| `*` | 換頁（台詞）或換行（墓碑、牌匾的英文雕刻）。墓碑與牌匾的譯文是字幕，不必跟著英文換行 |
| `%` `^` `@` `&` | 其他排版控制字元，數量要與英文一致 |

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
