# Text Surface Inventory — Ultima VIII（Phase 8）

**日期：** 2026-10-06
**範圍：** 英文版 Ultima VIII（GOG Gold Edition）在 ScummVM 中所有玩家看得到的文字。只做 inventory，不實作（Master Plan §27 Rule）。
**依據：** `scummvm-src`（`ultima8-zh-tw-dev` @ `5a8b1e7e5b`）原始碼；遊戲資料統計（`tools/diagnostics/text_survey.py`）；P1 研究（[u8-text-pipeline.md](u8-text-pipeline.md)）；日文版的處理方式（`ultima8.dat` 中的 `u8japanese.ini`）。

---

## 1. 總表

**Status 圖例：** ✅ 已完成（P4–P7）· 🟢 可沿用現有機制 · 🟡 需要新的掛點或字型設定 · 🟠 需要設計決定 · ⚪ 不翻譯 / 不在範圍

| # | Surface | Source | Renderer（字型） | Dynamic | Translation Method | Status |
|---|---|---|---|---|---|---|
| 1 | NPC 台詞（對話） | Usecode `Item::bark`（0x49），event `use` 等 | `BarkGump` → `TextWidget`（0、5、6、7、8，依角色） | 113 個句型（`{name}` 等） | `bark CCCC:IIII`；句型 + `param` | ✅ P5 / P7 |
| 2 | 對話選項 | Usecode `Item::ask`（0x4A） | `AskGump` → `ButtonWidget`（同上） | 否 | `ask CCCC` + 英文 | ✅ P6 |
| 3 | 查看物品 / 人物的名稱與描述 | Usecode `bark`，event `look`（00）：831 個呼叫點、574 種文字（例：`rope `、`Acolyte's key `、`fisherman `） | `BarkGump`（同 1） | 少量 | 同 1（P7 已翻 Devon 的 `00CC`） | 🟢 |
| 4 | NPC 自言自語、環境台詞 | Usecode `bark`，event `enterFastArea`（322）、`leaveFastArea`（203）、`justMoved`（185）等 | `BarkGump` | 少量 | 同 1；存檔策略同 P5 | 🟢 |
| 5 | Guardian 的嘲諷 | Usecode `bark`，class `AVATAR`（0401）event `guardianBark`（0x15），23 個 | `BarkGump`（字型 6） | 否 | 同 1。**可能有語音**，可作為 §49 #18 的語音測試對象 | 🟢 |
| 6 | 書本 | Usecode `Book::read`（0x6E）：86 個呼叫點、14 個 class、約 111,000 字元（最長 7,861） | `BookGump`：左右兩頁 `TextWidget`（字型 9），分頁 | 1 本動態（`SALKLOG 017A:0C32`） | 新掛點 `I_readBook` → `book CCCC:IIII`；並存 `_TL_()` 修正（見 §4.3） | 🟡 |
| 7 | 捲軸 | Usecode `Scroll::read`（0x6F）：22 個、約 7,300 字元 | `ScrollGump` → `TextWidget`（字型 9），分頁 | 否 | 新掛點 `I_readScroll` → `scroll CCCC:IIII` | 🟡 |
| 8 | 墓碑 | Usecode `Grave::read`（0x70）：68 個、約 2,600 字元；`*` 換行 | `ReadableGump` → `TextWidget`（**字型 11**，雕刻風格，未在 `[fontoverride]`） | 否 | 新掛點 `I_readGrave`；先採方案 A：英文雕刻 + 中文字幕（§4.1） | 🟡 |
| 9 | 牌匾 / 告示 | Usecode `Plaque::read`（0x71）：63 個、約 1,400 字元 | `ReadableGump`（**字型 10**，未在 `[fontoverride]`） | 否 | 同 8 | 🟡 |
| 10 | 開場動畫字幕 | `STATIC/EINTRO.SKF`：5 句（約 280 字元，Guardian 的台詞） | `SKFPlayer` → 字型 6 `renderText` | 否 | 新掛點 `SKFPlayer`：`movie EINTRO:<object>` | 🟡 |
| 11 | 結局動畫 | `STATIC/ENDGAME.SKF`：**沒有字幕物件** | — | — | 不需要 | ⚪ |
| 12 | 製作人員名單 | `STATIC/ECREDITS.DAT`（加密）：123 行、約 5,600 字元；`&` `}` `~` `@` `+` 格式碼 | `CreditsGump`（字型 6、8） | 否 | **不翻譯**（使用者決定） | ⚪ |
| 13 | 開發者語錄（Quotes） | `STATIC/QUOTES.DAT`（加密）：104 行、約 8,100 字元。主選單「7.Quotes」，**看完製作人員名單或破關後才出現**（設定 `quotes=true`） | `CreditsGump` | 否 | 是否翻譯待決定 | 🟠（低優先） |
| 14 | 主選單項目 | 圖片：`U8GUMPS.FLX` shape 37 frame 0–15（英文版是圖） | `MenuGump` → `ButtonWidget`（圖片）；日文版改為文字按鈕（`_TL_SHP_` → 0，字型 0） | 否 | 沿用日文版機制：shape 對應到 0 → 文字按鈕 + 譯文 | 🟡 P9 |
| 15 | 離開確認 | 圖片：shape 18（「Quit?」）＋ Yes/No 按鈕圖 | `QuitGump`；日文版改為文字（字型 6）；按鍵 `Yy` / `Nn` | 否 | 同 14；按鍵字母需保留英文 | 🟡 P9 |
| 16 | 輸入名字 | `_TL_("Give thy name:")` | `MenuGump` → `TextWidget`（字型 6） | 否 | engine 字串（見 §4.2） | 🟡 P9 |
| 17 | 名字輸入框 | 玩家輸入 | `EditWidget`（字型 6） | 是 | 不翻譯；只能輸入 ASCII | ⚪ |
| 18 | 存讀檔（日記） | `_TL_("The Beginning...")` ＋ 玩家輸入的存檔描述 | `U8SaveGump` → `TextWidget` / `EditWidget`（**字型 4**，未在 `[fontoverride]`） | 描述是 | 「The Beginning...」= engine 字串；描述不翻譯 | 🟡 P9 |
| 19 | 角色狀態 | `_TL_("STR")`、`INT`、`DEX`、`ARMR`、`HITS`、`MANA`、`WGHT` | `PaperdollGump::PaintStat`：`getGameFont(0)` **不允許 override**（一律 shape font） | 數值 | engine 字串；需改程式讓它可用 CJK 字型 | 🟡 P9 |
| 20 | 死亡畫面 | `_TL_("HERE LIES*THE AVATAR*REST IN PEACE")` | `ReadableGump`（字型 11，同墓碑） | 否 | engine 字串；顯示方式同 8（方案 A） | 🟡 P9 |
| 21 | 數量選擇（拿取堆疊物品） | 數字 | `SliderGump`（字型 0，不允許 override） | 是 | 只有數字，不需翻譯 | ⚪ |
| 22 | 其他圖片中的文字 | `U8GUMPS.FLX` 等的圖片（遊戲標題、gump 標題等） | 圖片 | 否 | P9 逐一檢視（ShapeViewer） | 🟠 P9 |
| 23 | ScummVM 介面（GMM、遊戲選項、存讀檔對話框） | ScummVM GUI | ScummVM 字型 | 否 | ScummVM 本身的翻譯。**繁中 `po/zh_Hant.po` 沒有任何譯文**（P9 實測：設 `gui_language=zh_Hant` 會顯示英文）；簡中 `po/zh.po` 有 1,084 / 3,258 條。繁中介面需要向 ScummVM upstream 貢獻翻譯 | ⚪ 不在本專案範圍 |
| 24 | 引擎錯誤訊息框 | `MessageBoxGump`（引擎內英文） | TTF Vera（ScummVM 內建字型） | 否 | 很少出現；保留英文 | ⚪ |
| 25 | 除錯主控台 | `Debugger` | ScummVM 主控台 | — | 開發者用，不翻譯 | ⚪ |
| 26 | 瞄準提示 | `_TL_("TARGETING RETICLE ...")` | `MessageBoxGump` | — | **只有 Crusader**，U8 不會出現 | ⚪ |

## 2. 統計

`python tools/diagnostics/text_survey.py`（遊戲資料唯讀）：

| 來源 | 呼叫點 / 項目 | 不重複文字 | 字元數（不重複） |
|---|---|---|---|
| bark（全部） | 4,533 個呼叫點、381 個 class | 3,751 | 約 330,000 |
| └ 其中 event `look` | 831 | 574 | — |
| ask | P2 統計：969 個（class + 英文） | — | — |
| Book::read | 86 | 85 | 約 111,000 |
| Scroll::read | 22 | 21 | 約 7,300 |
| Grave::read | 68 | 68 | 約 2,600 |
| Plaque::read | 63 | 62 | 約 1,400 |
| ECREDITS.DAT | 123 行 | — | 約 5,600 |
| QUOTES.DAT | 104 行 | — | 約 8,100 |
| EINTRO.SKF 字幕 | 5 句 | — | 約 280 |
| engine 字串（`_TL_`，U8 會出現的） | 15 個 | — | 約 150 |

bark 的 event 分布：`use` 2,499（對話為主）、`look` 831、共用函式 410、`enterFastArea` 322、`leaveFastArea` 203、`justMoved` 185、`calledFromAnim` 26、`guardianBark` 23。

（本工具以「呼叫前最後一個字串常值」判斷常值，與 P2 抽取工具的句型分析方法不同，bark 數字略有差異：P2 為 4,526 個呼叫點、4,408 個常值、113 個句型、5 個無法解析。）

## 3. 字型對照

`[fontoverride]`（`ultima8.dat` 的 `u8game.ini`）只包含字型 **0、5、6、7、8、9**。CJK 字型（P3/P4）只會替換這 6 個字型。

| 字型 | 用途 | 在 `[fontoverride]` | CJK 可用 |
|---|---|---|---|
| 0 | Avatar 以外部分角色的台詞、選單文字按鈕、狀態欄標籤、數量選擇 | ✅ | ✅（但 `PaperdollGump`、`SliderGump` 用 `getGameFont(n)` 不允許 override） |
| 4 | 存讀檔畫面 | ❌ | ❌ |
| 5 / 7 / 8 | NPC 台詞（依角色編號） | ✅ | ✅ |
| 6 | Avatar / Guardian 台詞、名字輸入、開場字幕、名單標題、日文版的墓碑字幕 | ✅ | ✅ |
| 9 | 書本、捲軸 | ✅ | ✅ |
| 10 | 牌匾（雕刻風格） | ❌ | ❌ |
| 11 | 墓碑、死亡畫面（雕刻風格） | ❌ | ❌ |
| 1–3、12–16 | U8 中未見於上述 surface | ❌ | — |

P5 / P6 的 `Font::isUTF8()` 檢查，會讓不能畫 UTF-8 的字型顯示英文，不會出現亂碼。

## 4. 需要決定的事項

### 4.1 墓碑、牌匾、死亡畫面的顯示方式（#8、#9、#20）

**決定（2026-10-06）：先採方案 A。** 使用者的 U7 中文化是全部改成中文，之後再評估是否改為方案 B。

這三種文字使用雕刻風格的 shape font（10、11），是畫面美術的一部分。可選：

| 方案 | 說明 | 參考 |
|---|---|---|
| A. **英文雕刻 + 中文字幕**（建議） | 保留原本的英文雕刻文字，下方以字型 6（CJK）顯示中文。保留美術風格 | **日文版的做法**：`ReadableGump` 遇到 `%` 時，後半段以字型 6 顯示為字幕（`readable_gump.cpp`） |
| B. 直接換成中文 | 以 CJK 字型取代雕刻字型 | 失去雕刻風格；需要把字型 10、11 加入 override |

### 4.2 engine 字串（#14–#16、#18–#20）

U8 會出現的 `_TL_()` 字串共 15 個。現有的 `_TL_()` 是依「遊戲語言」讀 `u8<語言>.ini`，英文版不會載入翻譯。可選：

- 在翻譯檔中新增 context，例如 `ui <英文>`，由 `Localization` 提供（與 bark / ask 同一個 MO 檔）。
- 主選單與離開確認的圖片按鈕，沿用日文版的 `_TL_SHP_` 機制改成文字按鈕。

字型方面：狀態欄（`PaperdollGump`）要改為允許 override；存讀檔畫面（字型 4）要決定是否加入 CJK override。

### 4.3 書本的 `_TL_()` 修正（§49 #10）

`BookGump` 對 shape 0x120 / quality 0x66 的書（The Spell of Resurrection），以 `u8english.ini` 的 `_TL_("spell of resurrection")` 換成正確的全文（修正原版 bug，ScummVM bug #12503）。新的翻譯層要以「修正後的英文」為原文，或為這本書另外建立條目。

### 4.4 製作人員名單與語錄（#12、#13）

約 13,700 字元，大多是人名與內部笑話。建議：職稱翻譯、人名保留；語錄是否翻譯由使用者決定。優先度最低。

## 5. 存檔影響

| Surface | 是否進存檔 | 對策 |
|---|---|---|
| BarkGump（含自言自語、查看名稱） | 會 | P5 已處理（存英文） |
| AskGump | 對話中不能存檔 | P6 已處理 |
| BookGump、ScrollGump、ReadableGump | 不會（`ModalGump`；`ReadableGump::saveData` 只寫 warning） | 不需要 |
| 存檔描述 | 會（玩家輸入） | 不翻譯 |

## 6. 建議的 Phase 分配

| Phase | Surface |
|---|---|
| P9 Engine UI / Static Text | #14–#16、#18–#20、#22（engine 字串、圖片按鈕、狀態欄字型、存讀檔字型） |
| P10 Extraction & Toolchain | 擴充抽取工具：書、捲軸、墓碑、牌匾、look bark、選項漏列（§49 #19）、參數、術語表 |
| P11 Dynamic Strings / Pagination / Timing | 書本與捲軸的分頁（中文頁數會不同）、`SALKLOG` 動態書、顯示速度 |
| 另立 | #6–#9 的掛點（`I_readBook`、`I_readScroll`、`I_readGrave`、`I_readPlaque`）可與 P10 一起做：與 bark 相同的「呼叫點 ID + 英文比對」模式 |
| 低優先 | #10 開場字幕、#12 / #13 名單與語錄 |
| 不做 | #11、#17、#21、#23–#26 |

## 7. 方法與限制

- 原始碼：搜尋 `ultima8/` 中所有 `new TextWidget`、`new ButtonWidget`、`renderText(`、`_TL_(`、`new EditWidget` 與 `getGameFont(`，排除 Crusader 專用的 gump（`cru_*`、`weasel`、`keypad`、`computer`、`movie_gump`）。
- 遊戲資料：Usecode 以 `u8dis.py` 反組譯；`ECREDITS.DAT` / `QUOTES.DAT` 以引擎的解密方式還原；SKF 以 flex 物件解析（字幕物件 = 6 bytes 標頭 + 文字）。
- **未涵蓋**：圖片中的文字（#22）只列出日文版替換過的 shape 18、37，其他需要在 P9 以 ShapeViewer 逐一檢視。
- 呼叫點只以靜態分析統計，實際是否都會在遊戲中出現未逐一確認。
