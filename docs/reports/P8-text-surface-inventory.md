# Phase P8 Report — Remaining Text Surface Inventory

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`（`ultima8-zh-tw-dev` @ `5a8b1e7e5b`，本 Phase 未修改）
- Game data: GOG Ultima VIII Gold Edition, English（唯讀）
- 本 Phase 只做研究，沒有建置或遊戲內測試

## Scope Performed

依 Master Plan §27：找出所有玩家看得到的文字類型，**只做 inventory，不實作**。

| 項目 | 內容 |
|---|---|
| 原始碼盤點 | 搜尋 `ultima8/` 中所有建立文字元件、繪製文字、使用 `_TL_()` 與取得字型的地方，排除 Crusader 專用的 gump |
| 遊戲資料統計 | 新增 `tools/diagnostics/text_survey.py`：Usecode 中顯示文字的 intrinsic（bark、ask、書、捲軸、墓碑、牌匾）的呼叫點、event、字數；`ECREDITS.DAT`、`QUOTES.DAT`（解密）；`EINTRO.SKF`、`ENDGAME.SKF` 的字幕 |
| 參考日文版 | `ultima8.dat` 的 `u8japanese.ini`：日文版翻譯了哪些 engine 字串、哪些圖片改成文字、墓碑如何加字幕 |
| 產出 | [docs/research/text-surface-inventory.md](../research/text-surface-inventory.md) |

## Evidence

### Inventory（摘要）

共 26 項，依狀態：

| 狀態 | 項目 |
|---|---|
| ✅ 已完成（P5–P7） | NPC 台詞、對話選項 |
| 🟢 可沿用現有機制 | 查看物品 / 人物名稱（`look` bark，574 種文字）、NPC 自言自語、Guardian 的嘲諷 |
| 🟡 需要新掛點或字型設定 | 書（86 本，約 111,000 字元）、捲軸（22）、開場字幕（5 句）、主選單、離開確認、輸入名字、存讀檔、角色狀態 |
| 🟠 需要設計決定 | 墓碑（68）、牌匾（63）、死亡畫面、製作人員名單、開發者語錄、圖片中的其他文字 |
| ⚪ 不翻譯 / 不在範圍 | 結局動畫（沒有字幕）、名字與存檔描述的輸入、數量選擇（只有數字）、ScummVM 介面（由 ScummVM 本身的 `zh_Hant.po` 處理）、引擎錯誤訊息、除錯主控台、瞄準提示（只有 Crusader） |

### 文字量

| 來源 | 字元數（不重複） |
|---|---|
| NPC 台詞（含查看名稱） | 約 330,000 |
| 書 | 約 111,000 |
| 名單 + 語錄 | 約 13,700 |
| 捲軸 | 約 7,300 |
| 墓碑 + 牌匾 | 約 4,000 |
| engine 字串、開場字幕 | 約 430 |

## Findings

### Observed

1. **CJK 字型只覆蓋字型 0、5、6、7、8、9**（`[fontoverride]`）。墓碑（11）、牌匾（10）、存讀檔（4）的字型不在其中；角色狀態與數量選擇以不允許 override 的方式取字型。這些 surface 需要額外處理，否則只能顯示英文（P5/P6 的 `isUTF8()` 檢查會避免亂碼）。
2. **日文版已有可借用的做法**：
   - 墓碑 / 牌匾：文字中以 `%` 分隔，後半段用字型 6 顯示成字幕（保留英文雕刻）。
   - 主選單與離開確認：把圖片按鈕對應到 0，改為文字按鈕（`_TL_SHP_`）。
   - engine 字串：`u8japanese.ini` 的 `[text]` 翻譯了 11 個 `_TL_()` 字串。
3. 書、捲軸、墓碑、牌匾的 gump 都是 `ModalGump`，**不會寫入存檔**，不需要 P5 那種存檔處理。
4. Guardian 的嘲諷（class `AVATAR` 0401，event `guardianBark`，23 句）可能有語音，可作為尚未完成的語音測試（§49 #18）的對象。
5. 結局動畫（`ENDGAME.SKF`）沒有字幕物件。
6. 只有一本書是動態組成的（`SALKLOG 017A:0C32`）。

### Inferred

- 書、捲軸、墓碑、牌匾都是「Usecode intrinsic + 字串參數」，可沿用 bark 的「呼叫點 ID + 英文比對」模式，新增 `book` / `scroll` / `grave` / `plaque` 的 context。
- 書的分頁（每頁 123×129）在中文下頁數會改變，但 `BookGump` 的分頁是依實際文字計算的，預期不需要特別處理（P11 驗證）。

### Unknown

- 圖片中的文字（遊戲標題、其他 gump 標題）尚未逐一檢視，列為 P9 工作。
- 靜態統計的呼叫點是否全部會在遊戲中出現，未逐一確認。

## 需要使用者決定的事項

1. **墓碑、牌匾、死亡畫面**：A. 英文雕刻 + 中文字幕（日文版做法，建議）／ B. 直接換成中文。
2. **製作人員名單與開發者語錄**：是否翻譯（建議職稱翻譯、人名保留；語錄可不翻）。
3. 其他項目依 inventory 的建議 Phase 分配（P9：engine UI 與圖片按鈕；P10：抽取工具與書 / 捲軸 / 墓碑 / 牌匾；P11：分頁與時間）。

## Files Changed

- 主 repo：`docs/research/text-surface-inventory.md`、`tools/diagnostics/text_survey.py`、本報告、Master Plan 與 HANDOFF
- `scummvm-src`：無

## Regressions

無（沒有修改程式）。

## Risks

1. 書本的文字量（約 111,000 字元）接近台詞的三分之一，翻譯工作量大，P10 的工具與術語表要先準備好。
2. 角色狀態、存讀檔畫面需要修改字型取得方式，P9 需注意不影響英文與日文版。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 9（Engine UI / Static Text）。建議先決定上面的事項 1。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 8 as required. Phase 9 was not started.
