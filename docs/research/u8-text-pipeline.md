# Ultima VIII Text Pipeline — Phase 1 Research

**Phase:** P1 — Text Architecture Audit  
**日期：** 2026-10-05  
**ScummVM：** upstream `master` @ `71cb05b1c03aa6bdcd34f78c20cef12c10067ba5`（未修改）  
**遊戲資料：** GOG Ultima VIII Gold Edition, English（`EUSECODE.FLX` detection MD5 `c61f1dac…`）  
**追蹤對象：** Devon（Usecode class `0x0402`），開局第一段對話

所有原始碼路徑相對於 `scummvm-src/engines/ultima/ultima8/`。每個結論都標註：

- **OBSERVED**：直接由原始碼、執行期 trace 或存檔內容證實
- **INFERRED**：由觀察合理推論，尚未直接驗證
- **UNKNOWN**：目前沒有足夠證據

---

## 0. 方法與證據來源

| 證據 | 內容 | 位置 |
|---|---|---|
| 原始碼閱讀 | UCMachine、intrinsics、Gump、Widget、Font、Audio | `scummvm-src/` |
| 靜態 Usecode 反組譯 | 自寫唯讀工具，opcode 運算元長度取自 `UCMachine::execProcess`。驗證：**515 個 class 全部解碼、0 次失去同步；923 個 event 進入點全部對齊指令邊界** | `tools/diagnostics/u8dis.py` |
| 執行期 Usecode trace | Debug build 加上編譯參數 `/DDEBUG_USECODE`（原始碼未修改，獨立目錄 `build-trace/`），主控台 `UCMachine::traceClass 0x402`，使用者實際與 Devon 對話 | `private_test/trace-20261005-220938.log`（本機，不進版控） |
| 存檔分析 | 對話結束後的存檔 `p1-after`，gzip 解壓後依 `saveStrings` 格式解析 | `private_test/saves/ultima8.001`（本機） |
| 全遊戲普查 | 用反組譯工具統計所有 class 的 bark/ask/concat/strcmp 用法 | 本文件 §6 |

執行期 trace 的位址格式 `CLASS:IP`（例如 `0402:0633`）與反組譯工具輸出的 offset 一致，兩者可以直接對照。

---

## 1. 追蹤一：NPC 台詞（Bark）

### 1.1 純 literal 台詞 — `"Hello there. "`

**OBSERVED**（靜態反組譯與執行期 trace 一致）：

```text
0402:061E  push pid
0402:061F  push string "Hello there. "        ← UCMachine opcode 0x0D → assignString() 產生 string ID
0402:0630  str to ptr                          ← opcode 0x6B：duplicateString()，產生「新的」string ID
0402:0631  push dword [BP+06h]                 ← this（Devon item）
0402:0633  calli 0049h  Item::bark(char* str)  ← intrinsic 呼叫
0402:0637  free string [SP+04h]
...
0402:063B  push retval（BarkGump process id）
0402:063C  implies → suspend                   ← Usecode 等 BarkGump 結束才繼續
```

C++ 端：

```text
UCMachine::execProcess  case 0x0F (uc_machine.cpp:350)
  → Item::I_bark (world/item.cpp:3053)
       ARG_STRING(str)                         ← string ID → Common::String（usecode/intrinsics.h:81-83）
  → Item::bark(const Common::String &msg) (world/item.cpp:2033)
  → new BarkGump(objId, msg, shapenum)         ← _barked = msg（gumps/bark_gump.cpp:49）
  → BarkGump::InitGump (bark_gump.cpp:78)
       new TextWidget(0, 0, _barked, true, fontnum, 194, 55)   ← :90
       AudioProcess::playSpeech(_barked, …)                    ← :99
       _counter = calculateTicks()                              ← :113
  → TextWidget::InitGump → setupNextText (gumps/widgets/text_widget.cpp:105)
       font->getTextSize(_text.substr(_currentStart), …, u8specials=true, paging)
       _currentEnd = _currentStart + remaining   ← byte offset
  → TextWidget::renderText (:145)
       font->renderText(_text.substr(_currentStart, _currentEnd-_currentStart), …)
  → TTFont::renderText (gfx/fonts/tt_font.cpp:195)
       typesetText<Traits>  → 斷行、分頁（byte iterator）
       toUnicode<Traits>    → encoding[] 單 byte 對應 Unicode；'@' → bullet glyph
       Graphics::Font（FreeType）繪製
```

### 1.2 動態台詞 — `"I am Devon, … " + getName() + "."`

**OBSERVED**（執行期 trace）：

```text
0402:08ED  push string "I am Devon, my strange friend. And I am glad to see you are feeling better, "
0402:0949  calli 00BCh getName()
0402:094E  concat  = "I am Devon, my strange friend. And I am glad to see you are feeling better, Pman"
0402:0955  push string "."
0402:095A  concat  = "…feeling better, Pman."
0402:0960  str to ptr [BP-1Fh]           ← opcode 0x69：字串來自 local 變數
0402:0964  calli 0049h Item::bark
```

到了 `Item::bark()`，收到的只是一個組合完成的 `Common::String`，**它由哪些 literal 組成的資訊已經消失**。

### 1.3 這次對話實際出現的全部 bark

| Bark 呼叫點 | 來源 | 類型 | 內容（節錄） |
|---|---|---|---|
| `0402:0633` | literal `0402:061F` | 靜態 | "Hello there. " |
| `0402:0964` | concat | 動態（玩家名） | "I am Devon, … feeling better, Pman." |
| `0402:0A84` | literal `0402:0A43` | 靜態 | "Why, on the shore, friend, safe now and thankfully alive. " |
| `0402:1A04` | literal `0402:1930` | 靜態 | "I am unsure, my friend. All I know is that I found your water-logged body…" |
| `0402:1B1D` | literal `0402:1AA8` | 靜態 | "Aye, 'tis what we sometimes call the sea. …" |
| `0402:3498` | concat | 動態（玩家名） | "Farewell, friend Pman, and good luck. …" |
| `0402:34FD` | literal `0402:34BF` | 靜態 | "I can already see a crowd gathering there on the docks." |
| `0402:352D` | literal `0402:350B` | 靜態 | "That can mean only trouble." |

---

## 2. 追蹤二：玩家回答選項（Ask）

### 2.1 建立選項清單

**OBSERVED**（執行期 trace，第一輪）：

```text
0402:083A  push slist [BP-1Dh]
0402:083C  push string "Who are you? "           ← literal
0402:084D  create list 01 (02)
0402:0850  append                                ← opcode 0x17
0402:0855  push slist [BP-1Dh]
0402:0857  push string "Goodbye. "
0402:0867  append
...
0402:0890  push string "Goodbye. " → remove slist (0x1A)   ← 依「內容」移除
0402:08A8  push string "Goodbye. " → append                ← 重新加到最後
0402:08BD  push pid
0402:08BE  push slist [BP-1Dh]                   ← opcode 0x43：copyStringList()，複製清單「與其中所有字串」
0402:08C0  push dword [BP+06h]
0402:08C2  calli 004Ah  Item::ask(uword slist)   ← Devon 所有輪次都用這「同一個」呼叫點
0402:08CA  push retval → implies → suspend
```

選項在之後的輪次以 `slist_union`（0x19，依內容去除重複）新增，以 `slist_sub`（0x1A，依內容移除）刪除。

### 2.2 AskGump 顯示與點擊

**OBSERVED**（原始碼）：

```text
Item::I_ask (world/item.cpp:3149)
  ARG_LIST(answers)
  new AskGump(1, answers)
    _answers = new UCList(2); _answers->copyStringList(*answers)   ← 第三次複製（gumps/ask_gump.cpp:41）
AskGump::InitGump (ask_gump.cpp:50)
  for each i:
    str_answer = "@ " + UCMachine::getString(_answers->getStringIndex(i))   ← '@' 就是在這裡加上的
    new ButtonWidget(px, py, str_answer, true, fontnum); child->SetIndex(i)
AskGump::ChildNotify (ask_gump.cpp:90)
  s = _answers->getStringIndex(child->GetIndex())   ← 以按鈕 index 取回 string ID，與按鈕文字無關
  _processResult = s
  _answers->removeString(s, true)                   ← 保留被選的字串不被釋放
```

### 2.3 回到 Usecode 分支

**OBSERVED**（執行期 trace，你選 "Who are you?" 那一輪）：

```text
0402:08D0  push dword process result         ← AskGump 回傳的 string ID
0402:08D8  push string "Who are you? "        ← 另一個獨立的 literal
0402:08E9  strcmp                             ← opcode 0x26：比對「字串內容」
0402:08EA  jne → (not taken)                  ← 相等 → 進入 "Who are you" 分支
0402:08ED  …"I am Devon…" bark
```

其餘輪次的比對結果：

| 玩家點選 | 比對成立的 literal | 備註 |
|---|---|---|
| Who are you? | `0402:08D8` "Who are you? " | |
| Where am I? | `0402:0A0F` "Where am I? " | 同一個分支也接受 `0402:0A22` "Where did you find me? "（OR 條件） |
| What happened to me? | `0402:1900` "What happened to me? " | 同一個分支也接受 `0402:191C` "Found me? " |
| The Lurker's domain? | `0402:1A8A` "The Lurker's domain? " | |
| Goodbye. | `0402:333E` "Goodbye. " | |

回答的分派是一條很長的 if / else-if `strcmp` 鏈。例如 "Goodbye." 那一輪共執行了 30 次 `strcmp` 才命中。

**結論（OBSERVED）：Usecode 用英文字串「內容」決定分支，string ID 本身沒有語意。** 同一句英文在同一個 class 裡會出現在多個 offset，例如 "The Lurker's domain? " 出現在 `0402:1A58`（加入清單）、`1A8A`（比對）、`1B56`（移除）。

---

## 3. 字串生命週期與複製

**OBSERVED**（`usecode/uc_machine.cpp`）：

| Opcode | 動作 | 對 string ID 的影響 |
|---|---|---|
| `0x0D` push string | `assignString(literal)` | **新 ID** |
| `0x16` concat | `_stringHeap[b] += getString(a)`；`freeString(a)` | 沿用 b 的 ID，內容改變 |
| `0x41` push string local | `duplicateString` | **新 ID** |
| `0x43` push slist local | `copyStringList` | 清單內每個字串都得到**新 ID** |
| `0x6B` str to ptr | `duplicateString` | **新 ID** |
| `0x69` push string var as ptr | 不複製 | 同 ID |
| `0x19` / `0x1A` slist union/sub | `stringInList` / `removeString` 依**內容**比對 | — |
| `0x26` strcmp | 依**內容**比對，之後 free 兩者 | — |
| `0x62` / `0x63` / `0x65` / `0x67` | free string / slist | — |
| `AskGump` ctor | `copyStringList` | 每個字串都得到**新 ID** |

**INFERRED：** 文字從 literal 到 Gump 的途中至少被複製 1～3 次。若採用「在 `0x0D` 記錄 provenance」的方案，`duplicateString`、`copyStringList` 和 concat 都必須同步傳遞 provenance。

---

## 4. 存檔、Stasis 與 Speech

### 4.1 對話期間不能存檔

**OBSERVED：**

- 使用者在 AskGump 開啟時按 `Ctrl+F5`，出現「此時無法保存遊戲」。
- 原因：對話開始時，Devon 會 spawn `METHOD`（class `0x057C`）的 `0BCF` 函式，該函式在 `057C:0C3E` 呼叫 intrinsic `0x00D0 setAvatarInStasis`。`Ultima8Engine::canSaveGameStateCurrently()` 在 stasis 期間回傳 false（`ultima8.cpp:1164`）。

**INFERRED：** 一般 NPC 對話（AskGump 與對話中的 BarkGump）不會出現在存檔裡。但 NPC 平常的自言自語 bark 不在 stasis 中，仍可能被存進存檔。

### 4.2 會被序列化的文字欄位

**OBSERVED**（原始碼）：

| 欄位 | 寫入位置 | 內容 |
|---|---|---|
| `UCMachine::_stringHeap` | `saveStrings`（`uc_machine.cpp:2292`）→ 存檔區段 `UCSTRINGS` | 所有現存字串 |
| `BarkGump::_barked` | `BarkGump::saveData`（`bark_gump.cpp:212-213`） | 原文 |
| `TextWidget::_text`、`_currentStart`、`_currentEnd` | `TextWidget::saveData`（`text_widget.cpp:209-215`） | **實際顯示的文字**與 byte offset |
| `AskGump::_answers` | `AskGump::saveData`（string ID 清單）；`loadData` 從 heap 重建按鈕 | string ID |

### 4.3 對話結束後的實際存檔

**OBSERVED**（`p1-after`）：

- 存檔格式：gzip → `8UMV` 容器，區段包括 `KERNEL`、`OBJECTS`、`WORLD`、`MAPS`、`CURRENTMAP`、`UCSTRINGS`、`UCGLOBALS`、`UCLISTS`、`APP`。
- `UCSTRINGS` 區段**沒有任何字串**（只有 ID 管理資料）。
- 整份存檔找不到任何對話文字，也沒有 BarkGump、AskGump、TextWidget 物件。

### 4.4 Speech

**OBSERVED**（`audio/speech_flex.cpp:67-92`）：`SpeechFlex::getIndexForPhrase()` 用 `hasPrefixIgnoreCase` 拿**英文 `_barked` 內容**比對語音片語表。`playSpeech`、`getSpeechLength`、`isSpeechPlaying`、`stopSpeech` 都以 `_barked` 為 key。

### 4.5 顯示時間

**OBSERVED**（`bark_gump.cpp:142-159`）：

```text
有語音：ticks = (目前頁面的 byte 長度 × speech 長度) ÷ (_barked.size() × MILLIS_PER_TICK)
無語音：ticks = (目前頁面的 byte 長度 × NO_SPEECH_LENGTH) ÷ talkSpeed
```

「目前頁面的長度」來自 TextWidget（實際顯示的文字），`_barked.size()` 則是原文長度。

---

## 5. 研究問題解答（Master Plan §20）

| # | 問題 | 答案 | 等級 |
|---|---|---|---|
| 1 | Bark 在哪裡從 string ID 變成 `Common::String`？ | `Item::I_bark` 的 `ARG_STRING(str)`（`world/item.cpp:3055`，macro 在 `usecode/intrinsics.h:81-83`）。之後一路以 `Common::String` 傳遞。 | OBSERVED |
| 2 | 該位置還能取得 Usecode class / 指令位置嗎？ | **可以。** intrinsic 執行時，`Kernel::getRunningProcess()` 是呼叫它的 `UCProcess`，而 `_ip` 要到該指令執行完才寫回（`uc_machine.cpp:1994-1996`），所以 `_classId:_ip` 正好是 `calli` 指令的位置，例如 `0402:0633`。trace 也以同一個 `p->_ip` 標示每條指令。 | OBSERVED（原始碼）；runtime 讀值待 Phase 2 驗證 |
| 3 | AskGump 的答案能追到穩定的 Usecode 位置嗎？ | 每個答案字串源自建立清單時的 `push string`（例如 "Who are you? " = `0402:083C`），但經過 2～3 次複製後，到了 AskGump 只剩新的 string ID 和內容。`ask` 的呼叫點是共用的（Devon 所有輪次都是 `0402:08C2`），**不能**作為答案的 ID。 | OBSERVED |
| 4 | 有哪些串接 opcode？ | 字串：`0x16`（concat）。清單：`0x17`（append）、`0x19`（union，依內容去重）、`0x1A`（依內容移除）、`0x1B`。 | OBSERVED |
| 5 | 哪些字串會動態組合？ | 玩家名字（`getName` 0xBC，全遊戲 151 處）、數字（`numToStr` 0xB9，28 處）、函式回傳值。全遊戲 4,526 個 bark 呼叫點：**4,377（96.7%）是單一 literal**，149（3.3%）是動態組合（concat 後直接 bark 88、經由變數 58、函式回傳值 2、其他 1）。 | OBSERVED（靜態普查） |
| 6 | string heap 會進存檔嗎？ | 會，`UCSTRINGS` 區段。但對話結束後是空的。 | OBSERVED |
| 7 | `_barked` 會進存檔嗎？ | 會（`BarkGump::saveData`）。但對話中的 bark 處於 stasis，無法存檔；只有一般 NPC 的自言自語 bark 可能被存進去。 | OBSERVED（程式碼）/ INFERRED（實際頻率） |
| 8 | 翻譯該放在 BarkGump 之前還是 TextWidget 之前？ | **BarkGump 之後、TextWidget 建立時**（`bark_gump.cpp:90`）。`_barked` 必須保持英文（語音與時間計算），而 TextWidget 的分頁以 `_text` 的 byte offset 計算，所以 TextWidget 必須拿到實際顯示的文字。 | INFERRED（設計推論，有 OBSERVED 依據） |
| 9 | AskGump 如何翻譯顯示而不改 `_processResult`？ | `ChildNotify` 以按鈕 index 取回 `_answers` 的 string ID，完全不讀按鈕文字。只要在 `InitGump`（以及 `loadData` 重建按鈕處）組 `str_answer` 時換成譯文，`_processResult` 與 Usecode 的 `strcmp` 都不受影響。 | OBSERVED |
| 10 | speech 是否用原始 `_barked` 比對？ | 是，以英文前綴比對語音片語表。 | OBSERVED |

---

## 6. 全遊戲 Usecode 普查

**OBSERVED**（英文 Gold Edition `EUSECODE.FLX`）：

| 項目 | 數量 |
|---|---|
| Usecode class | 515 |
| `push string` literal | 11,238 |
| 不重複的英文文字 | 5,980 |
| 出現 2 次以上的文字 | 1,913 |
| `Item::bark` 呼叫點 | 4,526 |
| `Item::ask` 呼叫點 | 159 |
| `Book::read` / `Scroll::read` / `Grave::read` / `Plaque::read` | 86 / 22 / 68 / 63 |
| `getName` / `numToStr` | 151 / 28 |
| `concat`（0x16） | 475 |
| `strcmp`（0x26） | 2,020 |

最常重複的文字："Farewell. "（131）、"bye "（125）、"Goodbye. "（100）、"."（94）、""（76）、"Who are you? "（58）、"What do you do? "（52）。**證實 Master Plan §7：只用英文原文當 key 不足以區分語境。**

---

## 7. 候選翻譯掛點

### 7.1 Bark — 建議方案

```text
Item::I_bark / Item::bark
  └─ 由 Kernel::getRunningProcess() 取得 UCProcess 的 classId:ip（calli 位置）作為 translation ID
BarkGump
  ├─ _barked = 英文原文（不變；speech、存檔都用它）
  ├─ 另外持有：translation ID 與顯示文字（不寫入存檔；讀檔時重新查表）
  └─ InitGump：new TextWidget(…, 顯示文字, …)
```

- **ID 形式（候選）：** `u8:<class>:<calli offset>:bark`，例如 `u8:0402:0633:bark`。
- **優點：** 純 literal 的 bark（96.7%），呼叫點和 literal 是一對一（`push string → 0x6B → calli` 的固定模式）。動態 bark 的呼叫點對應的是「一個句型」，正好適合 template 翻譯。
- **待 Phase 2 解決：**
  1. `TextWidget::_text` 和 byte offset 會被存檔（自言自語 bark 的情況）。需要決定：存檔中允許顯示文字，或讀檔時從 `_barked` 重建 TextWidget。
  2. 顯示時間公式混用顯示文字的長度與英文原文的長度（Phase 11）。
  3. 經由變數（`0x69`）的 58 個呼叫點，同一個呼叫點可能 bark 不同的字串。
  4. 由別的 class 代替 NPC 說話的情況，例如 `METHOD 057C` 裡的 bark。

### 7.2 Bark — 備案

- **Provenance sidecar**（Master Plan §21）：在 `0x0D` 記錄 `stringID → (class, literal offset)`，並在 `duplicateString`、`copyStringList`、concat 時一併傳遞。比較精確，但要修改 UCMachine 的多個熱點路徑，也要處理 provenance 的存讀檔。
- **英文全文 key**（現有 `GameData::translate()` 機制）：最簡單，但 1,913 個重複文字無法區分語境，只適合當 fallback。

### 7.3 Ask — 建議方案

- **ID 形式（候選）：** `u8:<呼叫 ask 的 class>:<英文答案文字>:ask`，例如 `u8:0402:"Who are you? ":ask`。
- **理由（INFERRED，有強證據）：** Usecode 本來就依內容處理答案（加入、去重、移除、比對全部依內容），所以**在同一個 class 裡，英文相同的答案在遊戲邏輯上就是同一個選項**。用「class + 英文內容」當 key，不會比遊戲本身的區分更粗。
- **掛點：** `AskGump::InitGump` 與 `AskGump::loadData` 組 `str_answer` 的地方，保留 `"@ "` 前綴。`_answers`、`_processResult`、string heap 全都不變。
- **呼叫 class 的取得方式：** 在 `Item::I_ask` 執行時讀取 running process 的 `_classId`。

### 7.4 Ask — 備案

以 provenance sidecar 追到建立清單時的 `push string` offset。代價同 7.2，而且同一個答案會有多個 offset（加入、去重），反而需要再合併。

---

## 8. 與 Master Plan 的差異

| 項目 | Master Plan 描述 | 實際情況 | 建議 |
|---|---|---|---|
| §5 opcode `0x0D` 作為來源 | 候選 hook | 字串在送到 Gump 前會被複製 1～3 次，`0x0D` 的資訊不會自然傳到 sink | 以「intrinsic 呼叫點」為 bark 的 ID 優先候選 |
| §7 ID `u8:<class>:<opcode offset>` | literal offset | bark 適合用 calli offset；ask 適合用 class + 英文內容 | Phase 2 ADR 定案 |
| §9 控制字元 `@` | 與 `% ~ * ^` 同類 | `@` 是 AskGump 自己加的 `"@ "` 前綴，只在 TTFont 被換成圓點，不是斷行或分頁字元 | 修正 §9 |
| §16 「save game 必須儲存翻譯後字串 → STOP」 | — | 對話中不能存檔；自言自語 bark 的 `TextWidget::_text` 會被存檔 | Phase 2 設計必須處理後者 |
| §20 文字 surface | BarkGump / AskGump / ReadableGump | 另有 BookGump、ScrollGump（以及 `Grave::read`、`Plaque::read`，經 ReadableGump） | Phase 8 inventory |
| `DEBUG_USECODE` | — | Usecode trace 預設不編譯 | 研究時用獨立的 `build-trace/` |

---

## 9. 未解問題（UNKNOWN）

1. 經由變數 bark 的 58 個呼叫點裡，同一個呼叫點是否會 bark 多種不同的字串？需要逐一靜態分析。
2. `Kernel::getRunningProcess()` 在 `I_bark` / `I_ask` 中的實際值：程式碼推論為 calli 位置，但要以 Phase 2 的最小實驗確認。
3. 自言自語 bark 實際被存進存檔的頻率，以及讀檔後 TextWidget 的行為。
4. 書本、捲軸、墓碑、牌匾的文字流程（BookGump / ScrollGump / ReadableGump）：本 Phase 未追蹤。
5. `BookGump` 使用 `_TL_()` 以英文全文替換內容（`u8english.ini` 的書本修正），新翻譯層要如何與它並存。
6. 日文版（SJIS）的對應路徑：本機沒有資料，只做了 code-path 層級的確認。
