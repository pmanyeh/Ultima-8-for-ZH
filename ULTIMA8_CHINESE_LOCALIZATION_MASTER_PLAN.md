# Ultima VIII Traditional Chinese Localization — Master Plan

## ScummVM Ultima8 Engine / Traditional Chinese Localization

**文件狀態：** Master Plan v3.1（2026-10-10；v2 依 Phase 0–2 實證修訂，v2.1–v3.1 為 Phase 4–16 的結果，見 Revision Log）  
**目標遊戲：** Ultima VIII: Pagan  
**主要 Runtime：** ScummVM — Ultima8 Engine  
**架構來源：** Pentagram → ScummVM Ultima8  
**目標語言：** Traditional Chinese (`zh_TW`)  
**基礎遊戲資料：** Original English Ultima VIII data（GOG Gold Edition）  
**工作環境：** Windows 11 / Visual Studio 2026 / VS Code / Claude Code  
**開發原則：** Evidence-First / Minimal Patch / Phase Gate / STOP after each Phase

---

# Revision Log

## v2 — 2026-10-06（Phase 0–2 完成後）

依據：

- [docs/reports/P0-baseline.md](docs/reports/P0-baseline.md)
- [docs/reports/P1-text-architecture-audit.md](docs/reports/P1-text-architecture-audit.md)
- [docs/research/u8-text-pipeline.md](docs/research/u8-text-pipeline.md)
- [docs/reports/P2-translation-identity.md](docs/reports/P2-translation-identity.md)
- [docs/architecture/ADR-001-translation-identity.md](docs/architecture/ADR-001-translation-identity.md)
- [docs/architecture/ADR-002-translation-catalog-format.md](docs/architecture/ADR-002-translation-catalog-format.md)

| 章節 | 修訂內容 |
|---|---|
| §5 | 補上實際的文字流程、存檔欄位，以及「Usecode 以字串內容決定分支」 |
| §7 | 翻譯 ID 由「候選」改為已決定（ADR-001）：bark 用呼叫點、ask 用 class + 英文 |
| §8 | 動態句子：U8 沒有 `%C` 這類佔位符號，而是用串接組句；改採「句型 + 參數」 |
| §9 | `@` 不是排版控制字元，而是 AskGump 加上的選項圓點 |
| §11 | 新增中英混排的逐字換行需求 |
| §13 | 目前的 repo、分支、建置目錄、工具狀態 |
| §14 | 英文原文可以放進 repo（使用者決策，比照 U7 中文化專案）；字型授權 |
| §16 | 新增 STOP 條件：字型缺失、缺字、譯文寫入存檔 |
| §18 | Phase 進度表 |
| §19–§21 | P0–P2 驗收打勾與結果說明 |
| §22–§25 | P3–P6 依 spike 結果補充工作項目與驗收條件 |
| §27 | 已知的文字 surface（書本、捲軸、墓碑、牌匾等） |
| §29 | 翻譯檔格式已決定：PO，依 Usecode class 分檔（ADR-002）；既有工具 |
| §30 | 句型比對設計、顯示時間 |
| §34 | HD 文字層的定位 |
| §46 | P2 結果與 GO 決策 |
| 新增 §48 | 字型與解析度策略 |
| 新增 §49 | 已知待辦項目總表 |

**Phase 狀態：** P0 ✅ PASS · P1 ✅ PASS · P2 ✅ PASS（GO）· P3 ✅ PASS · P4 ✅ PASS · P5 ✅ PASS · P6 ✅ PASS · P7 ✅ PASS（**Core Localization Architecture proven**）· P8 ✅ PASS · P9 ✅ PASS · P10 ✅ PASS · P11 ✅ PASS · P12 ✅ PASS · P13 ✅ PASS · P14 ✅ PASS · P15 ✅ PASS · P16 ✅ PASS

## v3.1 — 2026-10-10（Phase 16 快捷圖示列）

依據：[docs/reports/P16-quick-bar.md](docs/reports/P16-quick-bar.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | 新增 P16（UI 改善：快捷圖示列）PASS |
| §49 | #31 跳躍撞牆 bug 已修正並回報官方（PR #7979） |

## v3.0 — 2026-10-09（Phase 15 高解析文字層）

依據：[docs/reports/P15-hd-text-layer.md](docs/reports/P15-hd-text-layer.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P15 PASS（2026-10-10） |
| §34 | HD 文字層的實際做法：恢復 Pentagram 的縮放 + 合成架構（遊戲層不變） |
| §48 | 長期方案已實作；向量字型的選擇待使用者決定 |
| §49 | #12 實作完成 |

## v2.9 — 2026-10-07（Phase 12 完成後）

依據：[docs/reports/P12-save-speech-regression.md](docs/reports/P12-save-speech-regression.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P12 PASS |
| §31 | 驗收打勾；存讀檔矩陣、語音矩陣、啟動回歸的方法與結果 |
| §49 | #18 完成；#27、#28 記錄使用者決定；新增 #29（全語音 / 中文語音，P15 額外增強）、#30（upstream：以啟動參數讀檔前的自動存檔嘗試） |

## v2.8 — 2026-10-07（Phase 11 完成後）

依據：[docs/reports/P11-dynamic-strings-pagination-timing.md](docs/reports/P11-dynamic-strings-pagination-timing.md)

| 章節 | 修訂內容 |
|---|---|
| §8.1 | 抽取改為依分支列舉句子；分段句型 `{partN}`；函式回傳值成為 `{call_XXXX}` 的參數值 |
| §18.1 | P11 PASS |
| §30 | 驗收打勾；分頁量測結果（不調整版面）；顯示時間改以 reading length 計算（CJK 字算 3） |
| §49 | #3、#7、#25 完成；新增 #27（CJK 行距）、#28（proposed 譯名待確認） |

## v2.7 — 2026-10-06（Phase 10 完成後）

依據：[docs/reports/P10-extraction-toolchain.md](docs/reports/P10-extraction-toolchain.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P10 PASS |
| §29 | 驗收打勾；工具鏈與權威檔 |
| §49 | #10、#19 完成；新增 #25（動態組合的試劑名稱）、#26（權威檔分類與譯名需人工整理） |

## v2.6 — 2026-10-06（Phase 9 完成後）

依據：[docs/reports/P9-engine-ui-static-text.md](docs/reports/P9-engine-ui-static-text.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P9 PASS |
| §28 | 驗收打勾；圖片文字改用文字按鈕（日文版做法）而非翻譯圖片 |
| §49 | #21 結案（狀態欄維持英文、日記改用字型 9）；#22 語錄也不翻譯；新增 #23（EditWidget 的 high-res 問題）、#24（TTFont 越界修正可回報 upstream） |

## v2.5 — 2026-10-06（Phase 8 完成後）

依據：[docs/reports/P8-text-surface-inventory.md](docs/reports/P8-text-surface-inventory.md)、[docs/research/text-surface-inventory.md](docs/research/text-surface-inventory.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P8 PASS |
| §27 | 結果摘要與建議的 Phase 分配 |
| §49 | #10 移到 P10（書本掛點時處理）；新增 #20–#22 |

## v2.4 — 2026-10-06（Phase 7 完成後）

依據：[docs/reports/P7-first-complete-conversation.md](docs/reports/P7-first-complete-conversation.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P7 PASS；核心 localization 架構視為已證明 |
| §26 | 結果：Devon 第一次見面全程中文；句型比對（原 P11）提前在 P7 實作（使用者決定） |
| §30 | 句型比對與參數譯文已實作；P11 只剩實際 NPC 的參數譯文驗證與無語音顯示速度 |
| §49 | #7 完成（引擎與工具）；#18 語音仍待有語音的 NPC；新增 #19（抽取工具漏列部分選項） |

## v2.3 — 2026-10-06（Phase 6 完成後）

依據：[docs/reports/P6-askgump-choice-poc.md](docs/reports/P6-askgump-choice-poc.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P6 PASS |
| §25 | 驗收打勾；`AskGump::loadData` 不需要掛點（按鈕是存檔中的子 gump，改為存英文），不需在存檔中記錄 class |
| §49 | #17 完成 |

## v2.2 — 2026-10-06（Phase 5 完成後）

依據：[docs/reports/P5-npc-bark-poc.md](docs/reports/P5-npc-bark-poc.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P5 PASS |
| §24 | 驗收打勾；存檔策略定案：存英文，讀檔後該句以英文顯示；語音實測移到 P7 |
| §49 | #2、#17（bark）完成；#3 有語音的部分完成；新增 #18（有語音的 NPC，P7 驗證） |

## v2.1 — 2026-10-06（Phase 4 完成後）

依據：[docs/reports/P4-localization-manager.md](docs/reports/P4-localization-manager.md)

| 章節 | 修訂內容 |
|---|---|
| §18.1 | P4 PASS |
| §23 | 驗收打勾；正式設定名稱 `localization` / `localization_file`；CJK 字型只在 localization 啟用時載入 |
| §29 / ADR-002 | 執行時的單一編譯檔採用 gettext MO（`u8_<語言>.mo`），編譯工具 `tools/catalog/po_compile.py` |
| §49 | #1、#13 完成；新增 #15–#17 |

---

# 0. Project Mission

本專案的第一目標不是修改原版 Ultima VIII DOS executable，也不是製作新的遊戲引擎。

本專案目標是：

> **以 ScummVM 現有 Ultima8 Engine 為基礎，在不修改原始 Ultima VIII 遊戲資料與 Usecode 的前提下，加入完整的繁體中文顯示與翻譯層。**

最終玩家使用：

```text
Original Ultima VIII game data
        +
ScummVM Ultima8 Engine
        +
Traditional Chinese localization pack
        +
CJK TrueType/OpenType font
```

得到：

```text
完整繁體中文 Ultima VIII
```

同時保留：

- 原始遊戲邏輯
- 原始 Usecode
- 原始遊戲資源
- 原始 save game semantics
- 原始對話選項 identity
- 原始 speech/audio 邏輯
- 原始 quest / trigger / scripting behavior

---

# 1. First Major Success Target

第一個重大里程碑不是完整翻譯。

第一個 POC 必須做到：

```text
Original English Ultima VIII data
        ↓
ScummVM Ultima8
        ↓
一段真實 NPC 對話
        ↓
繁體中文顯示
        ↓
一個玩家對話選項
        ↓
繁體中文顯示
        ↓
點擊中文選項
        ↓
遊戲進入正確的原始對話分支
```

第一個 POC PASS 條件：

- 一段真實 NPC 台詞顯示繁體中文
- 至少一個 `AskGump` 選項顯示繁體中文
- 中文選項可以正常點擊
- 點擊後回傳的是原始 Usecode string identity
- 中文換行正常
- 中文字型正常
- 原英文 Usecode 未修改
- 原遊戲資料未修改
- 關閉 localization 後立即恢復純英文
- save/load 不因翻譯層失效

在此 POC 完成前：

> **禁止大量翻譯遊戲內容。**

---

# 2. Core Architectural Principle

本專案採用：

> **Presentation-Time Localization**

而不是：

> Modify Usecode Strings

即：

```text
Original Usecode
        ↓
Original runtime strings
        ↓
Original game logic
        ↓
Final text presentation
        ↓
Translation Manager
        ↓
Traditional Chinese
        ↓
CJK layout
        ↓
TTF renderer
```

核心原則：

> **遊戲邏輯永遠處理原始英文。**

> **玩家看到的文字才轉換成繁體中文。**

---

# 3. Why Translation Must NOT Modify String Heap First

Ultima VIII Usecode VM 本身存在：

```text
literal strings
string heap
string lists
runtime concatenation
dynamic parameters
conversation answers
speech matching
```

若直接在 Usecode `push string` 時把英文改成中文，可能造成：

- string comparison 改變
- conversation logic 改變
- dynamic concatenation 異常
- speech lookup 異常
- save game 儲存中文 runtime string
- translated string 被重新當作 game logic input
- 不同語言切換困難

因此初版禁止：

```text
Usecode string
→ overwrite with Chinese
```

優先架構：

```text
Usecode
↓
Original English string
↓
Game logic
↓
BarkGump / AskGump / ReadableGump / TextWidget
↓
Localization presentation lookup
↓
Chinese display text
```

---

# 4. Base Game Language vs Display Localization Language

這是本專案的重要架構邊界。

Ultima VIII 原始資料語言：

```text
base_game_language = English
```

繁中顯示語言：

```text
localization_language = zh_TW
```

兩者不得混為一談。

禁止單純新增：

```text
GAMELANG_CHINESE
```

然後讓原本 Ultima8 loader 嘗試載入：

```text
cusecode.flx
```

因為本專案沒有、也不需要中文版 Usecode。

正確模型：

```text
Base Data Language
      English
         │
         ▼
   eusecode.flx
         │
         ▼
 Original Game Logic

Localization Language
       zh_TW
         │
         ▼
 Translation Pack
         │
         ▼
 Presentation Layer
```

建議新設定概念：

```ini
ultima8_localization=zh_TW
```

或其他符合 ScummVM coding conventions 的名稱。

實際名稱必須在 Phase 2 依 ScummVM 現有 config architecture 決定。

不得擅自增加全域語言系統。

---

# 5. Known Ultima8 Text Pipeline

目前已知主要流程：

```text
Usecode
↓
UCMachine
↓
string heap / string lists
↓
game objects / intrinsics
↓
BarkGump
AskGump
ReadableGump
TextWidget
ButtonWidget
↓
Font
↓
TTFont
↓
Unicode rendering
```

其中 Usecode VM 已知有：

```text
opcode 0x0D
```

負責：

```text
push string
```

但：

> `0x0D` 只能作為 semantic source candidate。

禁止在 Phase 1 前直接把它當成正式 Translation Hook。

## 5.1 v2：Phase 1 實證結果

詳見 [docs/research/u8-text-pipeline.md](docs/research/u8-text-pipeline.md)。

**實際流程（Bark）：**

```text
push string (0x0D) → str to ptr (0x6B, 複製字串)
→ calli Item::bark (0x49) → Item::I_bark 以 ARG_STRING 轉成 Common::String
→ Item::bark → BarkGump(_barked) → TextWidget → TTFont → FreeType
```

**實際流程（Ask）：**

```text
push string → mklist/append/union → push slist（copyStringList，複製）
→ calli Item::ask (0x4A) → AskGump（再複製一次）→ ButtonWidget("@ " + 文字)
→ 點擊 → _processResult = string ID → Usecode strcmp(0x26) 比對英文內容 → 分支
```

**關鍵事實：**

- Usecode 以英文字串**內容**決定分支（`strcmp`、slist union/sub 都比對內容，且區分大小寫）。
- 字串送到 Gump 之前會被複製 1–3 次，所以 `0x0D` 的資訊無法自然傳到顯示端。**`0x0D` 不作為 Translation Hook。**
- 會寫進存檔的文字欄位：string heap（`UCSTRINGS`）、`BarkGump::_barked`、`TextWidget::_text`（顯示文字與 byte offset）、`AskGump::_answers`。
- 語音以 `_barked` 的英文前綴比對；顯示時間按 byte 長度比例計算。
- 對話期間主角處於 stasis，原版設計就不能存檔。
- Usecode 的 trace 預設不編譯，需要 `/DDEBUG_USECODE`。

---

# 6. Source + Sink Model

翻譯架構採用：

```text
Semantic Source
        +
Presentation Sink
```

## Source

可能來自：

```text
Usecode class ID
Usecode instruction offset
string ID
literal origin
function context
object context
actor
```

Source 的責任：

> 「這句文字從哪裡來？」

---

## Sink

可能包括：

```text
BarkGump
AskGump
ReadableGump
TextWidget
ButtonWidget
other discovered text surfaces
```

Sink 的責任：

> 「現在玩家實際看到什麼？」

---

# 7. Translation Identity

禁止只使用：

```text
English source string
```

作為唯一 key。

例如：

```text
Yes
No
Leave
Hello
```

可能出現在大量不同 context。

Candidate key：

```text
u8:<class_id>:<opcode_offset>
```

例如：

```text
u8:0134:028F
```

完整 catalog entry 概念：

```json
{
  "id": "u8:0134:028F",
  "surface": "bark",
  "speaker": "Devon",
  "original": "I have been expecting you.",
  "zh_TW": "我一直在等你。"
}
```

但此格式只是 Candidate。

正式 stable ID 必須等 Phase 2 audit 後確認。

## 7.1 v2：已決定的 ID（ADR-001）

上方以 literal offset 為 ID 的候選方案**不採用**。正式 ID：

```text
NPC 台詞   bark  <class>:<Item::bark 的 calli IP>          例：bark 0402:0633
對話選項   ask   <呼叫 ask 的 class> + <英文答案原文>      例：ask 0402 "Who are you? "
參數值     param <class>:<varXX | call_OOOO> + <英文值>    例：param 040A:varF7 "stranger "
```

- bark 的 ID 在 `Item::I_bark` 執行時由 running `UCProcess` 的 `classId:ip` 取得，不需要 provenance sidecar。
- ask 的 ID 用 class + 英文內容，因為遊戲本身就用內容辨識答案。英文比對區分大小寫，並保留結尾空白。
- 實證：多次執行 ID 一致；**離線抽出的 ID 在遊戲中全部命中**；相同英文在不同呼叫點有不同 ID（382 句英文分布在 1,038 個呼叫點）。

catalog entry 範例（PO，見 §29）：

```po
#. 對話：玩家選擇「Who are you?」之後
msgctxt "bark 0402:0964"
msgid "I am Devon, my strange friend. And I am glad to see you are feeling better, {name}."
msgstr "我是 Devon，我的陌生朋友。很高興看到你好多了，{name}。"
```

---

# 8. Dynamic String Problem

Ultima VIII 可能存在：

```text
"Thou hast "
+
number
+
" coins."
```

或：

```text
character name
+
runtime value
+
literal text
```

因此 Translation Manager 必須區分：

```text
Literal Translation
Template Translation
Final-Assembled Translation
UI Translation
```

不得假設所有文字都能由一個 literal string ID 翻譯。

## 8.1 v2：U8 的動態句子

U8 **沒有** U7 那種 `%C` 佔位符號。動態句子由 Usecode 以串接（`0x16`）組成，常見來源：

| 來源 | 次數（全遊戲 concat） | 例子 |
|---|---|---|
| 字串 literal | 278 | |
| `getName()`（玩家名字） | 132 | `"Hello there, " + {name} + "."` |
| string local 變數 | 32 | Orlok：`{varF7}` = 玩家名字或 `"stranger "` |
| 函式回傳值 | 24 | 酒名、`numToStr()` 數字 |

**策略（ADR-001 D3）：**

1. 抽取工具把串接還原成句型，例如 `Greetings again {varF7}. Will ye be havin' another {call_0BCF}?`。
2. 執行時用 bark ID 找到句型，拿完整英文比對固定部分並取出參數。
3. 參數值若有翻譯就替換（`stranger ` → 陌生人、酒名），玩家名字原樣保留。
4. 比對失敗就顯示英文。

全遊戲 bark 4,526 個：固定句子 4,408、自動還原的句型 113、無法自動解析 5（0.1%，需人工處理）。

**v2.8（P11）：** 句子常在分支內分段串接（單複數、物品種類、時段）。抽取工具沿分支列舉每個呼叫點實際可能的句子（追蹤簡單條件排除不可能的路徑），同一 `msgctxt` 可有多個條目（bark 4,761 條）。組合太多的呼叫點（魔杖、時間 focus）以手寫的分段句型描述，片段為 `{partN}` 參數；函式回傳的字串（酒名）成為 `{call_XXXX}` 的參數值。引擎在多個句型都符合時採用固定文字最多者。

Phase 2 必須調查：

- string concatenation opcode
- list copy
- temporary string
- string heap lifetime
- intrinsic string conversion
- final assembled message
- answer list construction

---

# 9. Ultima VIII Special Control Characters

現有 Ultima8 font/layout path 具有特殊 control characters。

已知至少包括：

```text
@
%
~
*
^
```

部分用途涉及：

- conversation bullet
- tab
- line break
- page break
- spacing/control behavior

翻譯工具不得：

```text
盲目翻譯
刪除
重新排序
Unicode normalize 掉
```

這些 token。

Translation Validator 必須檢查 control token preservation。

## 9.1 v2：實際的控制字元

依 `Font::Traits`（`gfx/fonts/font.h`）：

| 字元 | 作用 |
|---|---|
| `~` | 換行 |
| `*` | 換行；在墓碑與牌匾上為分頁 |
| `%` | Tab |
| `^` | 視為空白 |

**`@` 不是排版控制字元。** 它是 `AskGump` 在每個選項前加上的 `"@ "` 前綴，只在 TTFont 中被換成圓點符號。譯文不需要也不應該包含 `@`。

Validator 檢查對象改為 `~ * % ^`，以及句型參數 `{name}`、`{varXX}`、`{call_OOOO}`、`{num}`。

---

# 10. Unicode Strategy

目前 ScummVM Ultima8 已存在：

```text
legacy encoding
→ Unicode
```

以及：

```text
Shift-JIS
→ Unicode
```

以及：

```text
Common::U32String
```

TTF rendering path。

繁中路徑應採：

```text
UTF-8 localization data
        ↓
Unicode codepoints
        ↓
Common::U32String
        ↓
Graphics::Font
        ↓
TTF / FreeType
```

禁止：

```text
Big5-only runtime
custom DOS double-byte encoding
Unicode → fake 8-bit encoding
Chinese bitmap font as primary renderer
```

---

# 11. CJK Layout Requirements

繁中排版至少支援：

- UTF-8 decoding
- Unicode codepoint iteration
- 中文逐字換行
- ASCII word wrapping
- 中英混排
- punctuation rules
- clipping
- alignment
- page break
- conversation bullet
- cursor positioning if relevant

至少處理下列禁則：

行首避免：

```text
， 。 ！ ？ ： ； ） 》 」 』 】 〉
```

行尾避免：

```text
（ 《 「 『 【 〈
```

實際完整 punctuation set 應由 Phase 3 定義與 unit test 固定。

## 11.1 v2：中英混排換行

原本的排版演算法只在空白處斷行。中文沒有空白，所以英文後面接中文時（例如「我是在 Lurker 領域的深處……」），整段中文會被當成一個很長的「單字」，整段被推到下一行，留下大片空白。

**需求：** UTF-8 模式下，每個 CJK 字元都是可斷行點，同時仍遵守標點禁則。Spike 以 `UTF8Traits::endsWord()` 驗證可行；舊有的英文與日文 Traits 行為不變。Phase 3 需以 unit test 固定。

---

# 12. Repository Strategy

建議建立：

```text
Ultima8-ZH-TW/
├── ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md
├── AGENTS.md
├── README.md
├── scummvm-src/
│   └── git submodule → user's ScummVM fork
├── localization/
│   └── zh_TW/
│       ├── dialog/
│       ├── books/
│       ├── ui/
│       ├── items/
│       ├── names/
│       └── glossary/
├── tools/
│   ├── extract/
│   ├── validate/
│   ├── catalog/
│   └── diagnostics/
├── tests/
│   ├── unit/
│   ├── localization/
│   ├── layout/
│   └── integration/
├── docs/
│   ├── architecture/
│   ├── research/
│   ├── reports/
│   ├── decisions/
│   └── translation/
├── private_test/
│   └── .gitignore
└── scratch/
    └── .gitignore
```

---

# 13. Git Strategy

ScummVM fork 建議 branch：

```text
ultima8-zh-tw-dev
```

實驗性 branch：

```text
exp/u8-utf8
exp/u8-localization
exp/u8-cjk-layout
exp/u8-dialog-poc
```

規則：

- 不直接修改 upstream master
- 每 Phase 有獨立 commit
- 不自動 push
- Agent 不自行 rebase upstream
- upstream sync 必須是獨立任務
- translation data 與 engine code 儘量分離

## 13.1 v2：目前狀態

| 項目 | 現況 |
|---|---|
| `scummvm-src/` | upstream clone（blobless），尚未改為指向使用者 fork 的 submodule |
| 基準 | `master` @ `71cb05b1`，working tree clean |
| 實驗分支 | `exp/u8-p2-identity-spike`（commit `2063e25a89`，本機，未 push）：Phase 2 spike，**僅供參考，不直接合併** |
| 開發分支 | `ultima8-zh-tw-dev`：P3–P10，最新 commit `47541ad4bb`（本機，未 push；各 Phase 的 commit 見 `docs/HANDOFF.md`） |
| 建置目錄（gitignored） | `build-scummvm/`（P0 原版）、`build-trace/`（`DEBUG_USECODE`）、`build-spike/`、`build-dev/`（開發分支） |
| 單元測試 | WSL：`~/u8build`，`tools/build/wsl_unit_tests.sh`（481 項，見 P3 報告 Findings 4） |
| 工具 | `tools/diagnostics/`（反組譯、文字統計、shape 檢視）、`tools/extract/u8extract.py`（抽取）、`tools/catalog/`（`u8catalog.py` 抽取合併 / 檢查 / 統計 / 權威檔、`po_compile.py`）、`tools/validate/`（字集、存檔）、`tools/automation/` |
| 翻譯檔 | `localization/zh_TW/`：394 個 class 的 PO、`ui/engine.po`、權威檔 `authority.tsv`；說明見 `localization/README.md` |
| 本機測試 | `private_test/`：啟動檔、設定檔、字型、編譯後的 `u8_zh_TW.mo`、存檔、log（不進版控） |

**待辦：** 建立使用者的 ScummVM fork，並把 `scummvm-src/` 改為 submodule。

---

# 14. Copyright / Distribution Boundary

Repository 禁止提交：

```text
Ultima VIII original game data
eusecode.flx
original shapes
music
speech
save games
commercial fonts
screenshots containing copyrighted data unless intentionally approved
```

使用者自行提供合法 Ultima VIII game data。

字型必須：

```text
open-source
or
redistributable
```

例如可研究：

```text
Noto Sans CJK TC
Noto Serif CJK TC
```

正式選擇前必須記錄 license。

## 14.1 v2：英文原文與字型

- **英文原文可以放進 repo**（使用者決策，比照 U7 中文化專案）：PO 檔的 `msgid` 保留英文原文。禁止提交的仍然是原始遊戲資料**檔案**（`.flx`、`.dat`、音樂、語音、存檔等）。Phase 14 的 `LICENSES.md` 需說明遊戲文字的引用。
- **候選字型（已記錄授權）：**

| 字型 | 授權 | 用途 |
|---|---|---|
| Cubic 11（俐方體 11 號） | SIL OFL 1.1 | **目前首選**，12px 像素字型 |
| Noto Sans TC（Bold / Medium） | SIL OFL 1.1 | 向量字型，供未來 HD 文字層使用 |

---

# 15. Agent Global Rules

所有 Agent 工作固定流程：

```text
Inspect
↓
Understand
↓
Evidence
↓
Minimal Design
↓
Minimal Patch
↓
Build
↓
Test
↓
Report
↓
STOP
```

每個 Phase：

> **只做該 Phase。**

即使提前完成：

> **也不得自行進入下一 Phase。**

---

# 16. Mandatory STOP Conditions

遇到以下任一情況：

```text
STOP
→ report BLOCKED
```

包括：

- ScummVM current source 與本文件描述明顯不符
- Ultima8 engine 無法 build
- 原版 Ultima VIII 無法正常啟動
- baseline 本身不穩定
- 需要修改 original game data
- 需要修改 original Usecode 才能完成目前 Phase
- Translation path 會改變 game logic
- AskGump 中文顯示會改變原 string ID
- save game 必須儲存翻譯後字串
- speech lookup 被中文破壞
- Japanese Ultima8 regression
- English Ultima8 regression
- 其他 ScummVM engine regression
- 需要新增未授權重大 dependency
- stable translation identity 無法證明
- dynamic string behavior 與原設計不同
- upstream architectural conflict
- font license 不明

Agent 不得用 workaround 隱藏 blocker。

v2 新增：

- localization 開啟但 CJK 字型載入失敗，卻仍顯示 UTF-8 譯文（會變成亂碼）
- 譯文用到的字不在所選字型的字集內，且沒有 fallback
- 中文顯示文字被寫進存檔，造成關閉 localization 後讀檔仍出現中文（自言自語 bark 的 `TextWidget::_text`，需在 P4/P5 處理）

---

# 17. Testing Levels

## Unit

測試：

```text
UTF-8
Unicode iteration
CJK wrapping
punctuation
control tokens
translation lookup
fallback
catalog validation
```

---

## Engine Integration

測試：

```text
BarkGump
AskGump
ReadableGump
TextWidget
ButtonWidget
```

---

## Game Regression

測試：

```text
English localization OFF
Traditional Chinese ON
Traditional Chinese OFF again
```

---

## Save Regression

測試：

```text
save English
load Chinese

save Chinese-display mode
load English-display mode
```

遊戲狀態必須一致。

---

## Language Regression

至少：

```text
English
Japanese
Traditional Chinese overlay
```

不得破壞 Japanese Shift-JIS path。

---

# 18. Milestone Overview

```text
P0  Baseline
 ↓
P1  Text Architecture Audit
 ↓
P2  Translation Identity & Provenance
 ↓
P3  UTF-8 / CJK Foundation
 ↓
P4  Localization Manager
 ↓
P5  NPC Bark POC ★
 ↓
P6  AskGump Choice POC ★
 ↓
P7  First Complete Conversation ★
 ↓
P8  Remaining Text Surfaces
 ↓
P9  Engine UI / Static UI
 ↓
P10 Extraction & Catalog Toolchain
 ↓
P11 Dynamic Text / Pagination / Timing
 ↓
P12 Save / Speech / Regression Hardening
 ↓
P13 Translation Campaign
 ↓
P14 Packaging / Release
 ↓
P15 Optional Enhancements
```

## 18.1 v2：進度

| Phase | 狀態 | 報告 |
|---|---|---|
| P0 Baseline | ✅ PASS（2026-10-05） | `docs/reports/P0-baseline.md` |
| P1 Text Architecture Audit | ✅ PASS（2026-10-05） | `docs/reports/P1-text-architecture-audit.md` |
| P2 Translation Identity | ✅ PASS → **GO**（2026-10-06） | `docs/reports/P2-translation-identity.md` |
| P3 UTF-8 / CJK Foundation | ✅ PASS（2026-10-06） | `docs/reports/P3-cjk-foundation.md` |
| P4 Localization Manager | ✅ PASS（2026-10-06） | `docs/reports/P4-localization-manager.md` |
| P5 NPC Bark POC ★ | ✅ PASS（2026-10-06） | `docs/reports/P5-npc-bark-poc.md` |
| P6 AskGump Choice POC ★ | ✅ PASS（2026-10-06） | `docs/reports/P6-askgump-choice-poc.md` |
| P7 First Complete Conversation ★ | ✅ PASS（2026-10-06）— **Core Localization Architecture proven** | `docs/reports/P7-first-complete-conversation.md` |
| P8 Text Surface Inventory | ✅ PASS（2026-10-06） | `docs/reports/P8-text-surface-inventory.md`、`docs/research/text-surface-inventory.md` |
| P9 Engine UI / Static Text | ✅ PASS（2026-10-06） | `docs/reports/P9-engine-ui-static-text.md` |
| P10 Extraction & Toolchain | ✅ PASS（2026-10-06） | `docs/reports/P10-extraction-toolchain.md` |
| P11 Dynamic Strings / Pagination / Timing | ✅ PASS（2026-10-07） | `docs/reports/P11-dynamic-strings-pagination-timing.md` |
| P12 Save / Speech / Regression Hardening | ✅ PASS（2026-10-07） | `docs/reports/P12-save-speech-regression.md` |
| P13 Full Translation Campaign | ✅ PASS（2026-10-09）— 99.8%，6,949 條 | `docs/reports/P13-full-translation.md` |
| P14 Packaging | ✅ PASS（2026-10-09，使用者驗收）— Windows 免安裝包、GPL-3.0、勾選框預設開啟 | `docs/reports/P14-packaging.md` |
| P15 HD Text Layer | ✅ PASS（2026-10-10，使用者驗收）— 高解析中文字預設開啟、jf open 粉圓、屬性頁中文 | `docs/reports/P15-hd-text-layer.md` |
| P16 Quick Action Icons | ✅ PASS（2026-10-10，使用者驗收）— 右下角快捷圖示列（仿 Exult），預設開啟 | `docs/reports/P16-quick-bar.md` |

**注意：** P3–P6 雖然已由 P2 spike 驗證可行性，仍需依各 Phase 的規格重新寫成正式實作（加上 unit test、fallback、存檔處理），不得直接合併 spike。

---

# 19. Phase 0 — Baseline

## Goal

建立完全未修改的 ScummVM Ultima8 baseline。

## Tasks

### P0.1 Repository Audit

記錄：

```text
ScummVM upstream URL
branch
commit hash
working tree status
compiler
Visual Studio version
build configuration
```

---

### P0.2 Build ScummVM

建立：

```text
Debug build
Release build
```

至少確認 Ultima engine 被編入。

---

### P0.3 Launch Ultima VIII

使用合法原版 English Ultima VIII data。

確認：

- game detection
- intro
- new game
- movement
- conversation
- inventory
- save
- load
- audio
- subtitles

---

### P0.4 Font Override Baseline

只測現有 ScummVM font replacement。

不得加入中文功能。

確認：

- existing TTF override works
- anti-alias works
- high-res text path works
- Japanese-specific path location identified

---

### P0.5 Source Map

找到並記錄：

```text
GameData
UCMachine
Font
TTFont
FontManager
BarkGump
AskGump
ReadableGump
TextWidget
ButtonWidget
```

---

## Deliverable

```text
docs/reports/P0-baseline.md
```

內容包括：

```text
repo
commit
build command
runtime command
game version
known data requirements
screens tested
known warnings
```

---

## Acceptance

- [x] Debug build PASS
- [x] Release build PASS
- [x] English Ultima VIII launches
- [x] conversation works
- [x] save/load works
- [x] TTF override confirmed
- [x] source map recorded
- [x] no code modified

> v2：P0 PASS（2026-10-05）。建置環境為 VS 2026（MSVC 14.51）+ vcpkg master（CI 固定的 vcpkg 版本無法辨識 VS 2026）。

**STOP**

---

# 20. Phase 1 — Text Architecture Audit

## Goal

完整追蹤至少一段真實 NPC 對話。

不得修改程式。

---

## Required Trace

建立：

```text
Usecode literal
↓
opcode / string creation
↓
string heap
↓
runtime transformation
↓
game call
↓
BarkGump
↓
TextWidget
↓
Font
↓
TTFont
```

另外追蹤一個對話選項：

```text
Usecode
↓
string list
↓
AskGump
↓
ButtonWidget
↓
click
↓
returned string ID
↓
Usecode branch
```

---

## Research Questions

必須回答：

1. Bark message 在哪個函式從 string ID 變成 `Common::String`？
2. 該位置還能否取得 Usecode class / instruction context？
3. AskGump answer list 的 origin 是否能追到 stable Usecode location？
4. 字串有哪些 concat opcode？
5. 哪些字串會動態組合？
6. string heap 是否進 save state？
7. BarkGump `_barked` 是否進 save state？
8. translation 應放在 BarkGump 前還是 TextWidget 前？
9. AskGump display translation 如何不改 `_processResult`？
10. speech 是否使用原始 `_barked` 比對？

---

## Deliverable

```text
docs/research/u8-text-pipeline.md
```

每個結論標：

```text
OBSERVED
INFERRED
UNKNOWN
```

---

## Acceptance

- [x] one NPC line fully traced
- [x] one AskGump answer fully traced
- [x] string lifetime understood
- [x] save implications documented
- [x] speech implications documented
- [x] candidate translation hook listed
- [x] alternative hook listed
- [x] no implementation

> v2：P1 PASS（2026-10-05）。追蹤對象為 Devon（class `0402`）。另外發現 BookGump、ScrollGump 也是文字 surface。

**STOP**

---

# 21. Phase 2 — Translation Identity & Provenance Design

## Goal

定義穩定 translation ID。

不得實作完整翻譯。

---

## Candidate

優先研究：

```text
Usecode class ID
+
instruction offset
+
surface
```

例如：

```text
u8:0134:028F:bark
```

但必須實際驗證。

---

## Provenance Sidecar

允許研究：

```text
StringID
→ StringProvenance
```

概念：

```cpp
struct StringProvenance {
    uint16 classId;
    uint32 instructionOffset;
    OriginType origin;
};
```

但：

> 不得修改原始 string value。

---

## Dynamic String

若 concat 發生：

```text
String A
+
String B
→ String C
```

需研究是否：

```text
C provenance = composite(A,B)
```

或 final sink 使用其他 context。

---

## Translation Entry

設計至少包含：

```text
id
source
translation
surface
context
speaker optional
notes optional
status
```

---

## Deliverable

```text
docs/architecture/ADR-001-translation-identity.md
```

---

## Acceptance

- [x] same dialog → same ID across two runs
- [x] different dialog with same English text → different ID
- [x] AskGump stable identity
- [x] dynamic text strategy documented
- [x] fallback semantics defined
- [x] no game logic changes

> v2：P2 PASS → GO（2026-10-06）。上方的 provenance sidecar **不採用**，改用 intrinsic 呼叫點（ADR-001）。依使用者要求，P2 同時以 spike 驗證了中文顯示的可行性（實驗分支 `exp/u8-p2-identity-spike`）。

**STOP**

---

# 22. Phase 3 — UTF-8 / CJK Foundation

## Goal

讓 Ultima8 font stack 可以正確處理繁體中文。

尚不接真實遊戲對話翻譯。

---

## Work

實作適合目前 ScummVM architecture 的：

```text
UTF8Traits
```

或等效 Unicode path。

Agent 必須先研究是否已有可直接使用：

```text
Common::String UTF-8 APIs
Common::U32String conversion
Unicode iterators
```

禁止重造 ScummVM 已有 Unicode utilities。

---

## Required Test Strings

```text
繁體中文測試
Ultima VIII：異教徒
你好，Avatar！
生命值 HP：100
「這是一段中文。」 
```

---

## Special Token Tests

```text
@
%
~
*
^
```

必須保持既有 Ultima VIII semantics。

---

## CJK Wrap Tests

至少：

```text
純中文
中文 + English
數字
標點
conversation bullet
page break
very narrow rectangle
```

---

## Deliverable

```text
docs/reports/P3-cjk-foundation.md
```

---

## Acceptance

- [ ] UTF-8 valid input PASS
- [ ] malformed UTF-8 handled safely
- [ ] CJK glyph rendering PASS
- [ ] Chinese wrapping PASS
- [ ] punctuation test PASS
- [ ] original Traits PASS
- [ ] SJISTraits PASS
- [ ] Japanese regression PASS

## v2：P3 工作項目（依 P2 spike 調整）

Spike 已驗證以下做法可行，P3 要重新寫成正式實作：

1. **`UTF8Traits`**：UTF-8 解碼（不合法序列 → U+FFFD，且與 `advance()` 同步）、標點禁則、CJK 逐字斷行（`endsWord`）。
2. **`toUnicode` 修正**：改為逐字附加。原本以會做 UTF-8 解碼的 `U32String(const char*, len)` 預先配置長度，遇到多 byte 文字會觸發斷言。這個修正同時影響英文與日文路徑，需要 regression test。
3. **TTFont UTF-8 模式**：與 `_SJIS` 並列的第三種編碼模式。
4. **字集覆蓋檢查工具**：檢查「譯文用到的字 ⊂ 所選字型的字集」。像素字型的字數有限，這是必要工具。
5. **字型設定**：像素字型 Cubic 11，12px（DPI 0 時 1pt = 1px），關閉反鋸齒。反鋸齒目前是全域設定，需評估是否改為每個 override 個別設定（見 §48）。
6. **Unit test 位置**：先調查 ScummVM 現有的測試框架（`test/`）能否測到 engine 內部的 Traits。

Acceptance 補充：

- [ ] 中英混排換行（英文單字後接中文時不留空白）PASS
- [ ] 字集覆蓋檢查工具 PASS

**STOP**

---

# 23. Phase 4 — Localization Manager

## Goal

建立與 game language 分離的 localization layer。

---

## Concept

```text
Base Language = English
Localization = zh_TW
```

新增：

```text
LocalizationManager
```

或符合 ScummVM architecture 的名稱。

---

## Required API Concept

```text
translate(id, source, context)
```

fallback：

```text
translation found
→ Chinese

translation missing
→ original source
```

不得：

```text
missing translation
→ blank
```

---

## Runtime Toggle

至少支援：

```text
off
zh_TW
```

---

## POC Catalog

只能建立少量測試資料。

例如：

```text
one NPC line
one AskGump choice
```

不得 bulk translation。

---

## Acceptance

- [x] localization OFF → exact original text path
- [x] zh_TW → translated test lookup
- [x] unknown ID → original English
- [x] malformed entry → safe fallback
- [x] no Usecode changes
- [x] no string heap replacement

## v2：P4 工作項目

1. **ID 取得**：bark 在 `Item::I_bark` 由 running `UCProcess` 取得 `classId:ip`；ask 在 `Item::I_ask` 取得 class（ADR-001）。需要 `UCProcess::getIp()` 這類唯讀 accessor。
2. **翻譯表**：讀取由 PO 編譯成的單一檔案（ADR-002）。載入一次並建立 hash map，不得每次繪製都讀檔。
3. **設定名稱**：spike 使用 `u8_l10n`、`u8_l10n_file`、`u8_l10n_font`、`u8_l10n_fontsize`，正式名稱需符合 ScummVM 慣例，並考慮在遊戲選項 GUI 中提供。
4. **字型缺失時 fail open**：CJK 字型載入失敗 → 自動停用翻譯（ADR-001 D5）。
5. **英文比對**：條目同時比對英文原文，不符就顯示英文（SOURCE-MISMATCH）。

Acceptance 補充：

- [x] CJK 字型缺失 → 自動顯示英文，不出現亂碼

**v2.1：P4 結果**（[報告](docs/reports/P4-localization-manager.md)）

- 實作：`TranslationCatalog`（`misc/translation_catalog.*`，只依賴 `common/`）與 `Localization`（`misc/localization.*`）。
- 設定：`localization=off|zh_TW`、`localization_file`（預設 `u8_<語言>.mo`）；`font_cjk_*` 沿用 P3，`font_cjk_file` 預設 `Cubic_11.ttf`。
- 啟用條件：英文版 U8、翻譯檔正確且語言相符、CJK 字型套用到所有 `[fontoverride]` 字型。任何一項不成立就顯示英文並使用原字型。
- 查表 key：`context + "\x04" + 英文原文`。結果分為 HIT / MISS / SOURCE-MISMATCH（只有 bark 呼叫點會回報 SOURCE-MISMATCH）。
- 遊戲內確認：與 Devon 對話，bark ID 與離線抽取一致，`ask 0402 "Goodbye. "` HIT。
- `I_bark` / `I_ask` 只查表並寫 log（debug channel `Localization`），顯示文字在 P5 / P6 才替換。

**STOP**

---

# 24. Phase 5 — First NPC Bark Chinese POC ★

## Goal

讓一段真正 NPC speech 顯示繁體中文。

---

## Choose Target

選擇：

```text
early-game
easy to reproduce
stable
short
non-dynamic
```

的 NPC。

可優先研究 Devon，但 Agent 必須以實際可重現性決定。

---

## Required Flow

```text
Original English source
↓
original game logic
↓
BarkGump
↓
Translation lookup
↓
Traditional Chinese
↓
TextWidget
↓
CJK font
```

---

## Critical Constraint

以下值仍應保持英文/original：

```text
_barked
speech lookup
Usecode string heap
save-game game state
```

如果 translation 必須直接改 `_barked`：

> STOP 並重新設計。

---

## Acceptance

- [x] real NPC Chinese appears
- [x] original English does not visually overlap
- [x] correct actor
- [x] correct position
- [x] wrap correct
- [x] duration reasonable
- [~] speech still works（程式碼層級；Devon 沒有語音檔，實測移到 P7）
- [x] localization OFF restores English
- [x] save/load PASS

## v2：P5 工作項目

1. **掛點**：`BarkGump` 持有不寫入存檔的顯示文字，在 `InitGump` 建立 `TextWidget` 時使用；`_barked` 不變（spike 已驗證）。
2. **存檔**：自言自語的 bark（非 stasis）會把 `TextWidget::_text` 寫進存檔。需決定：讀檔時以 `_barked` 重新查表並重建 TextWidget（建議），或接受存檔中有譯文。
3. **顯示時間**：`calculateTicks()` 以顯示文字的 byte 長度 ÷ `_barked.size()` 計算；中文一個字 3 bytes，會停留過久。完整處理在 P11，P5 先確認不會「過早消失」。

Acceptance 補充：

- [x] 自言自語 bark 顯示中文時存檔 → 關閉 localization 讀檔 → 顯示英文

**v2.2：P5 結果**（[報告](docs/reports/P5-npc-bark-poc.md)）

- `BarkGump::_displayText`（不存檔）交給 TextWidget；`_barked` 不變。字型不能畫 UTF-8 時顯示英文。
- 存檔：`TextWidget::setSaveText()` 讓顯示譯文的 widget 存英文原文（offset 歸零）。存檔格式不變；讀檔後該句以英文顯示剩下的時間。
- 顯示時間：有語音時以實際顯示文字長度分配；無語音的公式不變（中文約每秒 5 字）。
- 測試：`Localization::bark <class>:<ip>`、`tools/validate/save_text_check.py`。

**STOP**

---

# 25. Phase 6 — First AskGump Chinese Choice POC ★

## Goal

繁中化玩家回答選項，但完全保留 Usecode identity。

---

## Flow

```text
Original StringID
↓
Original English answer
↓
display-only translation
↓
Chinese ButtonWidget
↓
player clicks
↓
original StringID returned
↓
original Usecode branch
```

---

## Critical Invariant

中文顯示文字：

> **不得成為 game logic return value。**

---

## Acceptance

建立至少兩個 answer：

```text
Option A
Option B
```

驗證：

- [x] both Chinese
- [x] button dimensions correct
- [x] hitboxes correct
- [x] Option A triggers original A branch
- [x] Option B triggers original B branch
- [x] returned string identity unchanged
- [x] English mode works
- [x] save/load works

## v2：P6 工作項目

1. **掛點**：`AskGump::InitGump` 與 `AskGump::loadData` 組 `"@ " + 文字` 的兩個地方都要替換；`_answers`、`_processResult` 不變（spike 已驗證點擊中文選項會進入原始分支）。
2. **呼叫的 class**：由 `Item::I_ask` 傳入 AskGump。讀檔重建時需要能取得 class，可存入 AskGump 的存檔資料，或由 owner 推得。注意：對話期間不能存檔，所以這是低頻率的情況。
3. **按鈕寬度**：選項以 160px 為寬度換行排列，需確認中文選項的寬度與點擊範圍。

**v2.3：P6 結果**（[報告](docs/reports/P6-askgump-choice-poc.md)）

- `Item::I_ask` 查好譯文傳給 `AskGump::_displayAnswers`（不存檔），只用於按鈕文字；`_answers` 與 `ChildNotify` 未修改。
- `loadData` 不從 string heap 重建按鈕，按鈕本身是存檔中的子 gump → `ButtonWidget::setSaveText()` 存英文即可，不需第二個掛點，也不需記錄 class。
- 按鈕寬度與點擊範圍依實際文字自動計算，中文正常。

**STOP**

---

# 26. Phase 7 — First Complete Conversation ★

## Goal

完成一小段真正的雙向 NPC conversation。

例如：

```text
NPC line
↓
2–3 player answers
↓
NPC response
↓
next choices
↓
conversation exit
```

---

## Must Test

- multiple pages
- repeated text
- same English appearing in different context
- conversation bullet
- click target
- speech
- text timing
- closing Gump
- restarting conversation

---

## Acceptance

> 玩家可以從對話開始到離開，全程使用繁中而不破壞任何 conversation logic。

若 PASS：

> **Core Localization Architecture is considered proven.**

**v2.4：P7 結果**（[報告](docs/reports/P7-first-complete-conversation.md)）：✅ PASS。Devon 第一次見面（新遊戲開場）全程中文；含玩家名字的 4 個句型（`0964`、`3498`、`060F`、`338E`）在遊戲中 HIT。語音無法實測（Devon 沒有語音檔，§49 #18）。

**STOP**

---

# 27. Phase 8 — Remaining Text Surface Inventory

## Goal

找出所有玩家可見文字類型。

---

## Known Candidates

至少調查：

```text
BarkGump
AskGump
ReadableGump
TextWidget
ButtonWidget
books
scrolls
signs
item names
inventory UI
stats
system messages
death text
intro text
game menu
save/load UI
credits
```

---

## Deliverable

```text
docs/research/text-surface-inventory.md
```

格式：

| Surface | Source | Renderer | Dynamic | Translation Method | Status |
|---|---|---|---|---|---|

---

## Rule

不要因為看到新 surface 就立刻實作。

先完整 inventory。

## v2：已知的 surface

P1 已發現的：

| Surface | Intrinsic / 位置 | 全遊戲呼叫點 |
|---|---|---|
| `BookGump` | `Book::read`（0x6E）；使用 `_TL_()` | 86 |
| `ScrollGump` | `Scroll::read`（0x6F） | 22 |
| `ReadableGump`（墓碑） | `Grave::read`（0x70） | 68 |
| `ReadableGump`（牌匾） | `Plaque::read`（0x71） | 63 |
| `MenuGump`、`QuitGump`、`U8SaveGump`、`PaperdollGump` | 使用 `_TL_()` | — |
| `CreditsGump` | 獨立處理 `@`、`~` 等字元 | — |
| `AvatarDeathProcess`、`TargetReticleProcess` | 使用 `_TL_()` | — |

另外，`u8english.ini` 已用 `_TL_()` 以英文全文替換書本內容（修正原版 bug），新翻譯層需要與它並存。

**v2.5：P8 結果**（[報告](docs/reports/P8-text-surface-inventory.md)、[inventory](docs/research/text-surface-inventory.md)）

- 26 類 surface；已完成：台詞、選項。可沿用 bark 機制：查看名稱（574 種）、自言自語、Guardian 嘲諷。
- 書（86，約 111,000 字元）、捲軸（22）、墓碑（68）、牌匾（63）都是「intrinsic + 字串參數」，可沿用「呼叫點 ID + 英文比對」；都是 `ModalGump`，不進存檔。
- CJK 字型只覆蓋字型 0、5–9；墓碑（11）、牌匾（10）、存讀檔（4）、角色狀態（不允許 override）需要額外處理。
- 日文版的做法可借用：墓碑字幕（`%`）、圖片按鈕改文字（`_TL_SHP_`）、engine 字串（`[text]`）。
- 待使用者決定：墓碑 / 牌匾的顯示方式；名單與語錄是否翻譯。

**STOP**

---

# 28. Phase 9 — Engine UI / Static Text

Ultima8 engine 已有內部 translation concept。

研究：

```text
GameData::translate()
language/text
language/gumps
```

---

## Goal

繁中化：

```text
engine-generated labels
stats
system messages
menus
fixed UI strings
```

不要與 Usecode translation 混為同一 identity system。

---

## Static Graphics

對內嵌英文字樣的 Gump：

優先：

```text
translated frame
```

而不是 OCR 或 host text overlay。

---

## Acceptance

- [x] known engine UI strings translated（角色狀態欄除外，放不下）
- [x] original fallback works
- [x] translated Gump mapping works where needed
- [x] no proprietary assets committed

**v2.6：P9 結果**（[報告](docs/reports/P9-engine-ui-static-text.md)）

- engine 字串使用獨立的 `ui` context（以英文辨識），與 Usecode 的 ID 分開。`Localization::uiText()` 在字型不能畫 UTF-8 時退回 `_TL_()`。
- 圖片文字：主選單、離開確認的問句改為文字（**日文版的對應方式，不製作翻譯圖片**；理由見報告）。yes / no、Entry、OK、PAGAN 標題維持原圖。
- 日記「旅程的開端……」用書本字型 9；死亡畫面為英文 + 中文字幕（方案 A）；角色狀態欄維持英文（放不下）。
- 修正 upstream 既有的 `TTFont::renderText` 寫出範圍問題。

**STOP**

---

# 29. Phase 10 — Extraction & Translation Catalog Toolchain

## Goal

自動建立待翻譯 catalog。

---

## Extraction Source

研究：

```text
UsecodeFlex
existing disassembler
ScummVM converter
Pentagram tooling
```

避免重造 Usecode parser。

---

## Extractor Output

至少：

```text
ID
original
class
offset
surface if known
context
control tokens
dynamic/static flag
```

---

## Translation Workflow Format

Phase 10 決定正式格式。

Candidate：

```text
PO
TSV
JSON
```

選擇條件：

- UTF-8
- context
- multiline
- version control friendly
- validation friendly
- translator friendly
- no unnecessary runtime dependency

Runtime 不應為了 JSON 加入大型第三方 parser。

### v2：格式已決定（ADR-002）

- **PO**，依 Usecode class 分檔（約 515 個），例如 `localization/zh_TW/dialog/0402_DEVON.po`。
- 條目依對話流程排列，`#.` 註解放上下文（例如「玩家選擇 Who are you? 之後」、參數說明）。
- `msgctxt` = ADR-001 的 ID；`msgid` = 英文原文或句型（區分大小寫、保留結尾空白）。
- 英文原文放進 repo。
- 建置工具檢查並合併成單一執行檔，引擎不需要 PO parser。
- 重新抽取時依 ID 合併（類似 `msgmerge`），不覆蓋既有譯文。
- Excel / CSV 只作為輸出的報表。

### v2：既有工具

- `tools/diagnostics/u8dis.py`：Usecode 反組譯。已驗證 515 個 class、0 次失去同步、923 個 event 進入點全部對齊。
- `tools/extract/u8extract.py`（示範版）：依對話流程抽取，能自動還原句型。全遊戲 bark 解析率 99.9%。P10 以它為基礎擴充成正式工具（輸出 PO、合併、驗證、覆蓋率）。

U7 的作法（Exult 反組譯成 `.es` → 翻譯 → 重新編譯）不適用於本專案，因為本專案不修改遊戲資料。但保留「依事件分檔、看得到上下文」的翻譯體驗。

---

## Required Tools

```text
extract
validate
coverage
duplicate detector
control-token validator
missing translation report
```

---

## Acceptance

- [x] repeat extraction deterministic
- [x] IDs stable
- [x] no duplicate-ID conflicts
- [x] same-English/different-context handled
- [x] control characters preserved
- [x] zero proprietary binary copied into repo

**v2.7：P10 結果**（[報告](docs/reports/P10-extraction-toolchain.md)、[翻譯檔說明](localization/README.md)）

- `u8catalog.py update`：全部 394 個 class → `localization/zh_TW/dialog/CCCC_NAME.po`（6,552 條，英文約 52 萬字元），合併時保留譯文；`check`（含過時條目、控制字元、權威檔、缺字）；`stats`（進度、重複、不一致）；`terms`（權威檔）。
- 新 context：`book` / `scroll` / `grave` / `plaque CCCC:IIII`；引擎已顯示（墓碑與牌匾為字幕）。
- 權威檔 `localization/zh_TW/authority.tsv`（使用者要求）：人名、地名、物品、魔法、生物、稱號、組織的唯一譯名。
- MO 的英文 key 以 CP437 編碼，與遊戲的 byte 一致。

**STOP**

---

# 30. Phase 11 — Dynamic Strings / Pagination / Timing

## Dynamic Text

支援：

```text
character names
numbers
items
quantities
locations
runtime values
```

優先使用：

```text
translated template
+
runtime parameters
```

避免翻譯完整 final text 的無限組合。

### v2：句型比對設計（ADR-001 D3）

```text
執行時收到： "Greetings again Pman. Will ye be havin' another Blackwine?"
bark ID：     040A:1F16
英文句型：   "Greetings again {varF7}. Will ye be havin' another {call_0BCF}?"
取出參數：   varF7 = "Pman"（玩家名字，不翻譯）、call_0BCF = "Blackwine"
參數翻譯：   param 040A:call_0BCF "Blackwine" → 「黑酒」
輸出：       「又見面了，Pman。要再來一杯黑酒嗎？」
```

- 比對失敗就顯示英文。
- 參數值（例如 `stranger `）可能帶有結尾空白，比對與替換時需正確處理。
- 譯文可以調整參數順序；Validator 需確認譯文與英文句型的參數集合相同。

### v2：顯示時間

`BarkGump::calculateTicks()` 目前以 byte 長度計算，必須改以「顯示字數」（codepoint）計算，並維持與英文語音長度的比例。

**v2.8（P11）完成：** `TranslationCatalog::readingLength()`（CJK 字含全形標點算 3、其他字元算 1）。權重 3 來自譯文長度（1 中文字 ≈ 3.2 英文字母）與閱讀速度比例；中文每字 24 ticks（約 2.5 字/秒，原版日文版約 1.5 字/秒），整句時間與英文相當。英文計時不變。

### v2.8：分頁量測結果

`localization_measure=true` + `tools/catalog/measure.py` 以實際字型量測全部譯文。台詞框 194×55：英文 5 行/頁，中文 3 行/頁（行距 18 px），POC 台詞頁數 +8%；選項、字幕寬度沒有超出。**未證明需要調整，不改字型、版面、分頁。** 正式翻譯後重新量測（§49 #27）。

---

## Pagination

量測所有翻譯：

```text
width
height
page count
```

只有實際證明需要時才：

```text
adjust font size
change pagination
increase dialog area
```

---

## Timing

BarkGump 原始 timing 可能依：

```text
string length
speech duration
talk speed
```

繁中顯示不得直接以 UTF-8 byte count 計算。

必須研究：

```text
codepoint count
displayed page length
speech duration
```

並保持合理體驗。

---

## Acceptance

- [x] runtime numeric string（金幣、試劑：真實 Usecode）
- [x] name substitution（Devon `{name}`、Orlok `{varF7}`）
- [x] item substitution（Orlok 酒名 `{call_0BCF}`、魔杖 `{partN}`）
- [x] multi-page Chinese（Devon 長句 2–4 頁）
- [x] no premature disappearance
- [x] no excessively long stale text

**STOP**

---

# 31. Phase 12 — Save / Speech / Regression Hardening

## Save Matrix

測試：

```text
English mode save → English load
English mode save → Chinese load
Chinese mode save → Chinese load
Chinese mode save → English load
```

Game state 必須一致。

---

## Speech Matrix

測：

```text
speech ON / subtitles ON
speech ON / subtitles OFF
speech OFF / subtitles ON
```

Localization 不得破壞：

```text
speech selection
speech timing
speech completion
```

---

## Regression

至少：

```text
English U8
Japanese U8 if test data legally available
Ultima8 font override OFF
Ultima8 font override ON
localization OFF
localization zh_TW
```

另外執行 ScummVM relevant unit tests。

---

## Acceptance

- [x] save compatibility PASS（`save_matrix.ps1` + `save_compare.py`：4 種組合 × 2 個存檔，邏輯區段與英文基準線逐 byte 相同）
- [x] speech PASS（`Localization::guardianBark`：語音 / 字幕 3 種組合 + 英文對照，使用者確認）
- [x] English regression PASS（`regression_startup.ps1` 情境 A / G / I；非 UTF-8 字型維持原版計時）
- [x] Japanese code path regression PASS（程式檢查 + SJIS 單元測試；無合法日文資料）
- [x] localization toggle PASS（情境 A–I；存檔可在兩種模式間交換）
- [x] missing font fallback defined（情境 F：還原原字型、停用翻譯）

### v2.9（P12）結果

- 中文模式只改變顯示：存檔的 GAME / WORLD / MAPS / CURRENTMAP / UCGLOBALS / UCSTRINGS / UCLISTS 與英文模式相同；KERNEL / OBJECTS 的差異只來自時間，和兩次英文執行之間的差異相同。
- 語音以英文原句選擇與計時；中文字幕依各頁 reading length 分配語音長度。
- P11 計時改動對 Shift-JIS 的潛在誤判已修正（只有 UTF-8 字型使用 reading length）。

**STOP**

---

# 32. Phase 13 — Full Translation Campaign

只有到此 Phase 才大量翻譯。

---

## Suggested Order

```text
1. Core UI
2. Common interaction text
3. Names
4. Items
5. Locations
6. Early game conversation
7. Main NPC dialog
8. Side NPC dialog
9. Books / scrolls
10. System messages
11. Edge cases
12. Credits / misc
```

---

## Translation Status

每條至少：

```text
UNTRANSLATED
DRAFT
REVIEWED
IN_GAME_VERIFIED
FINAL
```

---

## Glossary

建立：

```text
localization/zh_TW/glossary/
```

至少管理：

```text
Avatar
Guardian
Pagan
Titan
Thaumaturgy
Necromancy
Theurgy
Sorcery
Tempestry
places
characters
items
spells
```

正式譯名先 research，再固定。

---

## QA

每章 / 每區域建立：

```text
translation coverage
visual QA
context QA
quest regression
```

禁止一次宣稱整個遊戲完成而沒有區域 acceptance。

---

# 33. Phase 14 — Packaging

玩家安裝目標：

```text
ScummVM
+
legally owned Ultima VIII data
+
zh_TW localization pack
```

禁止要求：

```text
patched eusecode.flx
patched U8.EXE
modified commercial data archive
```

---

## Translation Pack

理想：

```text
localization/ultima8/zh_TW/
```

或符合 ScummVM architecture 的正式位置。

---

## User Configuration

目標 UX：

```text
Game data: English
Localization: Traditional Chinese
Font: bundled/open-source CJK
```

---

## Deliverables

```text
README.zh-TW.md
INSTALL.zh-TW.md
TRANSLATION_CREDITS.md
LICENSES.md
CHANGELOG.md
```

---

# 34. Phase 15 — Optional Enhancements

只有核心中文版穩定後才考慮。

---

## Possible Enhancements

```text
larger high-resolution dialogue
HD font profiles
font size setting
dialog history
better books
HD UI labels
wide conversation panels
Traditional Chinese player-name input
IME support
translation debugging overlay
translation ID inspector
voice replacement
```

這些功能：

> 不屬於第一版中文化必要條件。

v2：其中「larger high-resolution dialogue / HD font profiles」是讓向量中文字型清晰顯示的根本解法（見 §48）。ScummVM 移除了 Pentagram 的 ScalerGump，需要新增一層以視窗解析度繪製文字的機制。第一版以像素字型因應。

v3.0（P15）：已實作 HD 文字層（`hd_text`）。遊戲仍畫在 320×200，每幀放大到視窗解析度，再以 Pentagram 留下的 `PaintCompositing` 把高解析字型的文字畫上去；滑鼠座標換回遊戲座標，存檔不受影響。見 [P15 報告](docs/reports/P15-hd-text-layer.md)。

---

# 35. Player Name / Chinese Input

繁中顯示與繁中輸入必須分開。

V1 可以允許：

```text
English player name
+
Traditional Chinese game text
```

中文名字輸入屬於後續 Enhancement。

不得讓 IME 問題阻擋核心 localization POC。

---

# 36. Performance Requirements

Translation layer 必須：

- lookup deterministic
- avoid expensive config lookup every frame
- cache catalog
- avoid repeated UTF-8 conversion where possible
- avoid per-frame file I/O
- avoid unnecessary heap allocation in hot render loop

翻譯檔應：

```text
load once
→ validate
→ build lookup map
```

不得每次 RenderText 都重新讀檔。

---

# 37. Fallback Rules

任何翻譯錯誤：

```text
must fail open
```

即：

```text
missing translation
→ English

bad translation record
→ English

font glyph missing
→ fallback font or safe replacement

localization pack missing
→ English
```

禁止：

```text
blank dialog
broken conversation
crash
blocked gameplay
```

---

# 38. Logging

Debug build 可提供：

```text
localization ID
surface
source text
translation hit/miss
font
layout size
page count
```

例如：

```text
[U8-L10N]
id=u8:0134:028F
surface=bark
result=HIT
source="I have been expecting you."
translation="我一直在等你。"
```

Release 預設不得大量輸出。

---

# 39. Architecture Invariants

## I1

```text
Original game data is read-only.
```

## I2

```text
Original Usecode remains authoritative.
```

## I3

```text
Localization is presentation-only whenever possible.
```

## I4

```text
Game logic uses original strings and IDs.
```

## I5

```text
Missing translation never blocks gameplay.
```

## I6

```text
Traditional Chinese canonical encoding is UTF-8.
```

## I7

```text
No Big5 runtime requirement.
```

## I8

```text
Japanese support must remain intact.
```

## I9

```text
Base-game language and localization language are separate concepts.
```

## I10

```text
No bulk translation before architecture POC PASS.
```

---

# 40. Definition of Technical Success

第一階段技術成功定義：

> **Using unmodified English Ultima VIII game data, ScummVM's Ultima8 engine displays a real NPC dialogue and player response options in Traditional Chinese through a Unicode/CJK font pipeline, while the original Usecode strings and string identities remain authoritative and gameplay behavior is unchanged.**

---

# 41. Definition of Project Success

完整版成功：

```text
Original Ultima VIII
+
ScummVM Ultima8
+
Traditional Chinese localization
+
CJK TrueType/OpenType
+
complete dialogue
+
UI
+
books
+
items
+
system messages
+
stable save/load
+
original gameplay
```

且：

```text
localization OFF
→ normal English Ultima VIII
```

---

# 42. Phase Report Template

每 Phase 建立：

```text
docs/reports/Px-<name>.md
```

格式：

```markdown
# Phase Px Report

## Result

PASS / FAIL / BLOCKED

## Environment

- Repository:
- Branch:
- Commit:
- Compiler:
- Build:

## Scope Performed

## Evidence

## Files Changed

## Tests

## Findings

### Observed

### Inferred

### Unknown

## Regressions

## Risks

## Blockers

## Recommendation

## Next Phase Readiness

READY / NOT READY

## STOP

Work stopped after Phase Px as required.
```

---

# 43. First Agent Task

將以下內容作為第一個 Codex / VS Code Agent 任務。

```text
Read ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md completely.

Execute PHASE 0 ONLY.

Do not implement Traditional Chinese localization yet.

Goal:
Establish a verified, reproducible baseline for the current ScummVM Ultima8
engine running an unmodified English Ultima VIII installation.

Tasks:

1. Inspect the workspace.
2. Record all repositories, branches, commits and dirty working trees.
3. Identify the exact ScummVM build instructions for Windows.
4. Confirm the Ultima8 engine is included in the selected build configuration.
5. Build an unmodified Debug configuration.
6. Build an unmodified Release configuration.
7. If legally obtained Ultima VIII data is already available locally, launch it.
8. Verify:
   - new game
   - movement
   - one NPC conversation
   - one player response choice
   - inventory
   - save
   - load
   - audio
   - subtitles
9. Inspect but DO NOT MODIFY the current implementations of:
   - GameData
   - UCMachine
   - Font
   - TTFont
   - FontManager
   - BarkGump
   - AskGump
   - ReadableGump
   - TextWidget
   - ButtonWidget
10. Confirm the current TrueType/font-override path.
11. Identify the current Japanese/SJIS text path.
12. Record exact relevant source paths and functions.
13. Produce:

   docs/reports/P0-baseline.md

Important constraints:

- Do NOT modify ScummVM source.
- Do NOT modify Ultima VIII game data.
- Do NOT modify usecode files.
- Do NOT create Chinese translations.
- Do NOT add a Chinese language enum.
- Do NOT add dependencies.
- Do NOT start Phase 1.
- Do NOT push to GitHub.

If the source differs materially from the Master Plan assumptions,
document the difference and STOP with BLOCKED rather than redesigning
the architecture yourself.

Final response must include:

- PASS / FAIL / BLOCKED
- repository commit
- build results
- Ultima VIII launch result
- exact source files relevant to the text pipeline
- known discrepancies
- path to P0-baseline.md

Then STOP.
```

---

# 44. Phase 1 Agent Task Skeleton

**Do not execute until Phase 0 is reviewed.**

```text
Execute PHASE 1 ONLY.

Trace one real NPC line from Usecode literal/string creation all the way to
BarkGump/TextWidget/Font rendering.

Also trace one AskGump answer from creation through button display and back
to the original Usecode branch after clicking.

Do not modify code.

Clearly separate:
OBSERVED
INFERRED
UNKNOWN

Produce docs/research/u8-text-pipeline.md and STOP.
```

---

# 45. Phase 2 Agent Task Skeleton

```text
Execute PHASE 2 ONLY.

Using Phase 1 evidence, design stable translation identity and optional
string-provenance metadata.

Do not implement localization yet.

Prove that:
- the same dialog produces the same identity across runs;
- different contexts can distinguish identical English source text;
- AskGump can retain original StringID while displaying translated text.

Produce ADR-001-translation-identity.md and STOP.
```

---

# 46. Critical Go / No-Go Gate

正式開始 Unicode 與中文程式碼以前：

```text
P0 PASS
+
P1 PASS
+
P2 PASS
```

才允許開始 Phase 3。

如果 Phase 2 無法建立可靠 stable identity：

> **NO-GO。**

不得用：

```text
English text only
```

草率取代 stable ID architecture。

### v2：Gate 結果（2026-10-06）

```text
P0 PASS
+
P1 PASS
+
P2 PASS
= GO → Phase 3
```

stable identity 已建立並以實機驗證（ADR-001），沒有以英文原文取代 ID。

---

# 47. Final Development Order

完整建議順序：

```text
P0
↓
review
↓
P1
↓
review
↓
P2
↓
GO / NO-GO
↓
P3
↓
P4
↓
P5 ★ First Chinese NPC
↓
P6 ★ First Chinese Choice
↓
P7 ★ First Complete Conversation
↓
P8
↓
P9
↓
P10
↓
P11
↓
P12
↓
Architecture Freeze
↓
P13 Full Translation
↓
P14 Release
↓
P15 Optional Enhancements
```

---

# 48. Font & Resolution Strategy（v2 新增）

## 問題

Ultima VIII 以 **320×200** 繪製，再由 ScummVM 放大到視窗（例如 1440×1080，約 4.5 倍）。TTF 文字也畫在 320×200 上，所以一個中文字大約只有 12px。

## 實測（P2）

| 方案 | 結果 |
|---|---|
| Noto Sans TC 可變字重（預設最細） | 加上 1px 黑框後幾乎看不清楚 |
| Noto Sans TC Bold 11pt | 清楚，但放大後筆畫邊緣呈方塊狀 |
| 遊戲高解析度選項（640×400） | 地圖範圍變大、角色變小，改變了原版畫面 → 不採用 |
| **Cubic 11（俐方體 11 號）12px，關閉反鋸齒** | **筆畫銳利，符合像素美術風格 → 採用** |

## 決策

- **第一版：** 像素字型 Cubic 11（SIL OFL），12px，關閉反鋸齒。
- **必要工具：** 字集覆蓋檢查（P3），確認譯文用字都在字型內，並規劃缺字的 fallback 字型。
- **長期（P15）：** 以視窗解析度繪製文字的 HD 文字層，屆時改用向量字型（Noto Sans TC 等）。**v3.0 已實作**（`hd_text` + `font_cjk_hd_*`），預設字型待使用者決定。
- 中文字型的大小與顏色沿用原版 `u8game.ini` `[fontoverride]` 的顏色與黑框設定。

---

# 49. Known Open Items（v2 新增）

| # | 項目 | 處理 Phase |
|---|---|---|
| 1 | ~~CJK 字型載入失敗時自動停用翻譯~~ ✅ 還原原字型並停用 | P4 |
| 2 | ~~自言自語 bark 的 `TextWidget::_text` 寫入存檔~~ ✅ 存英文原文（`setSaveText`） | P5 |
| 3 | ~~顯示時間以 byte 計算~~ ✅ reading length（CJK 字算 3），有語音 / 無語音都適用（P11） | P11 |
| 4 | ~~字集覆蓋檢查工具~~ ✅ `tools/validate/font_coverage.py` | P3 |
| 5 | ~~`font_antialiasing` 為全域設定~~ ✅ `font_cjk_antialiasing` 個別設定 | P3 |
| 6 | ~~`toUnicode` 修正的英文與日文 regression test~~ ✅ 單元測試（日文無實機資料） | P3 |
| 7 | ~~句型比對與參數翻譯~~ ✅ 引擎與編譯工具（P7）；Orlok `040A` 的 `{varF7}`、`{call_0BCF}` 驗證完成（P11） | P7 / P11 |
| 8 | 5 個無法自動解析的 bark（PYROS、SORCERER、METHOD） | P10 |
| 9 | 共用 class（例如 `METHOD 057C`）代為發話時的對話脈絡 | P10 |
| 10 | ~~BookGump 的 `_TL_()` 書本修正與新翻譯層並存~~ ✅ 有譯文時不套用英文修正（P10） | P10 |
| 11 | 建立 ScummVM fork 並改為 submodule | P3 之前或期間 |
| 12 | ~~HD 文字層~~ ✅ `hd_text`（P15 報告） | P15 |
| 13 | ~~是否只在 localization 開啟時載入 CJK 字型~~ ✅ 是（OFF 時與原版完全相同）。開啟時未翻譯的英文仍會以像素字型顯示 | P4 |
| 14 | 原版換行在字元比行寬時無限迴圈 → 已在 P3 修正，可考慮回報 upstream | — |
| 15 | 遊戲選項 GUI 的語言選單（ScummVM game option 只有勾選框，需要自訂 widget） | P9 或之後 |
| 16 | 翻譯檔沒有記錄遊戲資料版本；考慮在檔頭加入 `EUSECODE.FLX` 雜湊 | P10 |
| 17 | ~~掛點確認目標字型是 UTF-8 字型~~ ✅ BarkGump（P5）、AskGump（P6） | P5 / P6 |
| 18 | ~~有語音的 NPC 在 localization 下的語音與字幕~~ ✅ 英文語音 + 中文字幕，語音 / 字幕各組合正常（P12，Guardian 嘲諷） | P12 |
| 19 | ~~抽取工具漏列部分選項~~ ✅ 改為同時收集被比對的答案（P10） | P10 |
| 20 | 墓碑（字型 11）、牌匾（10）、死亡畫面：**先採方案 A（英文雕刻 + 中文字幕，日文版做法）**（使用者決定 2026-10-06）。U7 專案是全部改成中文，之後再評估是否改為方案 B | P9 / P10 |
| 21 | ~~字型 4 與狀態欄字型~~ ✅ P9：日記的中文改用字型 9；狀態欄維持英文（列距 9px 放不下中文）；`SliderGump` 只有數字 | P9 |
| 22 | 製作人員名單（`ECREDITS.DAT`）與開發者語錄（`QUOTES.DAT`）：**都不翻譯**（使用者決定 2026-10-06） | — |
| 23 | `EditWidget` 使用 high-res TTF（CJK）時文字畫到錯誤位置（日記輸入框）。P9 以不替換日記字型避開；使用者：之後再修 | 待定 |
| 24 | `TTFont::renderText` 游標與文字寫出圖片範圍（upstream 既有，P9 已修正），可考慮回報 upstream | — |
| 25 | ~~試劑名稱等動態組合的文字~~ ✅ 依分支列舉句子 + 分段句型 `{partN}`（P11） | P11 |
| 26 | 權威檔（`authority.tsv`）的分類與 711 個待決定的譯名需人工整理 | 翻譯開始前 |
| 27 | ~~台詞框行數~~ ✅ 2026-10-10：設定 `bark_lines`（每頁行數，高解析開啟時預設 4）、`bark_width`（預設 194），上限 300×100 遊戲像素；只影響中文台詞，存檔仍寫入原版 194×55（引擎 `63622f587d`） | — |
| 28 | P11 POC 用到的 14 個譯名（黑酒、黑曜石、血…）：使用者同意先使用（2026-10-07），之後依舊版中文手冊再調整；權威檔維持 proposed | 使用者查手冊後 |
| 29 | 全語音 / 中文語音（使用者的想法，2026-10-07）：語音以 shape 編號選檔、以英文片語比對（`SpeechFlex`），中文語音需要新的語音檔與片語表 | P15（條件成熟時） |
| 30 | upstream：以 `--save-slot` 讀檔時，ScummVM 在讀檔前嘗試自動存檔，新遊戲初始化的 stasis 使它失敗，下一次延後 5 分鐘（不影響遊戲） | — |
| 31 | ~~upstream：跳躍撞牆卡住 / 穿出地圖~~ ✅ 已修正（2026-10-10）：`AnimationTracker::step` 大步移動撞到物件時，`GetInterpolatedCoords(end, start)` 起點終點傳反，主角被放進物件裡；之後每個動作立刻失敗，主角移動控制在同一 tick 無限重跑（被 kernel 保護機制終止而卡死），或落下時掉到 Z < 0。改為 `(start, end)`，使用者確認不再卡住、不再穿牆。官方原版同樣有此 bug；使用者要求回報，已送出 [PR #7979](https://github.com/scummvm/scummvm/pull/7979)（分支 `ultima8-fix-jump-into-wall`，2026-10-10） | — |
| 32 | ~~upstream：字型快取（`FontManager::TTFHash`）以位址當雜湊~~ ✅ 2026-10-10 修正（引擎 `88656e047d`）：套用遊戲選項時可能當掉、字型重複載入。可考慮回報官方（需使用者同意） | — |

---

# END OF MASTER PLAN