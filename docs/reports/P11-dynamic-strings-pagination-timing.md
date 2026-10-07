# Phase P11 Report — Dynamic Strings / Pagination / Timing

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `4ce1d3e434`（本機，未 push；接續 P10 的 `47541ad4bb`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），483 項全部通過（新增 2 項：`test_reading_length`、`test_part_templates`；`test_placeholders` 擴充）
- Game data: GOG Ultima VIII Gold Edition, English（唯讀）
- 遊戲內測試：使用者操作（2026-10-07 12:54，`launch-dev.bat new`，log `private_test/dev-20261007-125420.log`）

## Scope Performed

依 Master Plan §30。

| 項目 | 內容 |
|---|---|
| 抽取：依分支列舉句子 | `u8extract.py` 新增 `site_variants()`：沿 Usecode 的分支（`jne`、`jmp`、`foreach`）走訪，記錄每個 bark / 讀物呼叫點**實際可能組出的每一個句子**。同一指令上字串狀態相同的路徑只走一次；追蹤簡單條件（`local == N`、`not local`、同一函式的回傳值 `== N`，例如時段），排除不可能的路徑；迴圈回到開頭時，上一輪留下的字串視為未知（不列入）。對話流程（`--flow`）的線性走訪保留不變 |
| 抽取：分段句型 `{partN}` | 組合太多的呼叫點（`PART_TEMPLATES`，目前 2 處）以手寫句型描述，抽取時用**全部列舉結果驗證**每個句子都符合某個句型（或屬於明列的不可達分支），符合的片段值成為 `param CCCC:partN` 條目 |
| 抽取：函式回傳值 | `{call_XXXX}` 的可能值（函式回傳的字串）自動成為 `param` 條目（Orlok 的 5 種酒） |
| 引擎：句型 | `{partN}` 佔位符號（N = 1–99）與 `param CCCC:partN`；同一呼叫點有多個句型都符合時，採用**固定文字最多**的句型（`{part1}of {part2}` 與 `{part1}of {part2}with {num} uses remaining`）；整句條目仍優先於句型 |
| 引擎：顯示時間 | `TranslationCatalog::readingLength()`：以「英文字母」計算長度，CJK 字（含全形標點）算 3，其他字元（UTF-8 或遊戲 CP437 的 byte）算 1。`BarkGump::calculateTicks()` 改用它（無語音的時間、有語音時各頁分配的比例）。英文文字每個 byte 仍算 1，**英文的計時完全不變** |
| 引擎：量測 | 設定 `localization_measure=true`：啟動後以實際字型與各種文字框尺寸排版每一條譯文，log 中寫出頁數、寬高、reading length（英文與譯文）；`tools/catalog/measure.py` 彙整 |
| 主控台 | `Localization::say <class>:<ip> <英文>`：以某個呼叫點說出任意英文（測試句型與參數，可用雙引號保留空白） |
| 工具 | `po_compile.py`：接受 `param CCCC:partN` 與 `{partN}` |
| 說明文件 | `localization/README.md`：動態組合的句子、參數值（不帶結尾空白）、`{partN}`、長度與顯示時間、`say` 指令 |
| POC 譯文 | 30 條：金幣、試劑 8 句、Orlok 句型 2 + 參數 6、魔杖句型 3 + 整句 1 + 片段 7、時間 focus 句型 1。譯者註解 `# P11 POC`。翻譯檔合計 105 條 |
| 權威檔 | POC 用到的 14 個詞改為 **proposed**（note「P11 POC」）：Blackwine 黑酒、Tenebraen Ale Tenebrae 麥酒、Hurricane 颶風酒、Breath o' Spirit 靈息酒、Cloven Hoof 魔蹄酒、obsidian 黑曜石、Blood / blood 血、Bone 碎骨、Dirt 泥土、Wood / wood 木頭、Ignite 點燃、Explosion 爆炸。**尚未 approved**，正式翻譯前需使用者確認 |

## 抽取結果的變化

| 項目 | P10 | P11 |
|---|---|---|
| 條目總數（含 ui） | 6,564 | 6,841 |
| bark | 4,528 | 4,761 |
| param | 11 | 54（var 11、call 5、part 38） |
| 有多個句子的呼叫點 | —（分支被串成一句） | 38 |
| 無法解析的 bark | 5 | 5（文字來自呼叫端的參數，§49 #8） |

P10 中把分支串成一句的 **11 條錯誤條目全部消失**，例如：

| 呼叫點 | P10（錯誤） | P11 |
|---|---|---|
| `018B:0300` 試劑 | `{num} vial vials of blood pile piles of bone shards …` | 17 句：`{num} vial of blood`、`{num} vials of blood`、`{num} pile of wood` … |
| `00E3:0282` HOURGLAS | （未列出） | 7 句：`The time is now Bloodwatch.` … `This clock is broken ` |
| `058A:0750` DAEMSCEN | — | `How may I serve you, master? ` / `… mistress? ` |
| `041F:14DC` GORGROND | `Hello again, {varFA}. What do you want?What do you want of me now, …` | 9 句（依好感度） |
| `018D:0462` 魔杖等 | `symbol of ignite extinguish flash … with {num} use uses remaining` | 句型 3 + 整句 5（未鑑定時只顯示種類）；片段 part1 5 種、part2 12 種 |
| `0596:0B87` 時間 focus | `… Bloodwatch,  Firstebb,  Daytide, …` | 句型 1；part1 時辰 7、part2 星期 7、part3 月份 7 |
| `0596:082E` 位置 focus | 31 個地點串成一句 | 27 句 |

上限設定與驗證：每個指令最多 64 種字串狀態、每個呼叫點最多 64 句。以 1,024 / 2,000 的上限重跑，除了兩個 `PART_TEMPLATES` 呼叫點（239 與 343 句）以外，**全部結果與 64 相同**；全遊戲抽取約 4 秒。超過上限的新呼叫點會印出警告，提示加入 `PART_TEMPLATES`。

`018D:0462` 的 `skip`：沒有物品種類或沒有法術的路徑（程式的 else 分支，實際物品都有種類與法術），明列略過。

## 分頁量測（`measure.py`，105 條）

| 種類 | 條目 | 英文頁數 | 中文頁數 | 頁數增加 | reading length 中 / 英 |
|---|---|---|---|---|---|
| bark | 48 | 66 | 71 | 5 條 | 0.93 |
| ask | 26 | — | — | — | 1.10 |
| book | 1 | 2 | 2 | 0 | 0.91 |
| scroll | 1 | 1 | 2 | 1 條 | 0.93 |
| grave / plaque | 4 | （字幕） | — | — | — |

- 台詞框 194×55：英文（像素字型）一頁 5 行；中文（Cubic 11 12px，行距 18px）一頁 3 行、每行約 16 字。中文頁數多約 8%（Devon 的長句 1→2、2→3、3→4 頁）。
- 選項寬度沒有超過 160 px；墓碑、牌匾字幕沒有超過 320 px。
- 捲軸「購物清單」（每行都是 `~` 換行的短詞）1→2 頁：行距較大，換行多的捲軸 / 書會多頁。
- **結論**：增加幅度小，依 §30「只有實際證明需要時才調整」，**不改字型、版面或分頁**。若正式翻譯後頁數增加明顯，可考慮的做法是縮小 CJK 行距（行距 ≤ 13px 時台詞框可放 4 行）。

## 顯示時間

| | 每字 ticks（talkspeed 60） | 速度 |
|---|---|---|
| 英文 | 8 / 字母 | 約 7.5 字母 / 秒 |
| 中文（P11） | 24 / 字 | 約 2.5 字 / 秒 |
| 原版日文版（talkspeed 24、SJIS 2 bytes） | 40 / 字 | 約 1.5 字 / 秒 |

- 權重 3 的依據：現有譯文中 1 個中文字對應約 3.2 個英文字母（台詞），而閱讀速度的比例（英文約 20 字母/秒、中文約 6 字/秒）也約 3。整句的顯示時間與英文原句相當（0.93 倍）。
- 改用 reading length 之前，中文以 UTF-8 byte 計算剛好也是每字 3，結果近似，但那是編碼的巧合；現在與編碼無關，且全形標點、CP437 字元都有明確規則。
- 有語音時（§49 #18）：語音長度依各頁 reading length 的比例分配，讀取原本的英文語音。

## Evidence

### 遊戲內（使用者操作，2026-10-07）

| 測試 | 結果 | log |
|---|---|---|
| Devon 第一次見面（新遊戲）全程中文，多頁台詞自動翻頁 | 使用者確認 OK（`0402:3311` 中文 4 頁、`1D55` 2 頁、`22CF`、`1A04`、`21C9` 等） | 全部 HIT |
| `Cheat::items` 後查看黑曜石幣 | 「500 枚黑曜石幣」 | `bark 008F:00D5 HIT src="500 obsidian coins"` |
| 查看試劑（真實 Usecode，數量 + 單複數 + 種類） | 「50 瓶血」「50 堆碎骨」「50 堆木頭」「50 堆泥土」 | `bark 018B:0300 HIT` ×4 |
| 未翻譯的試劑 | 英文（fallback） | `SOURCE-MISMATCH src="50 piles of blackmoor"`、`"50 executioner's hoods"` |
| `say 040A:1F16`（stranger / 黑酒） | 「又見面了，陌生人。要再來一杯黑酒嗎？」 | HIT |
| `say 040A:1F16`（玩家名字 / 魔蹄酒） | 「又見面了，Pman。要再來一杯魔蹄酒嗎？」 | HIT |
| `say 018D:0462 wand of ignite with 3 uses remaining` | 「點燃魔杖（剩 3 次）」（選中最具體的句型） | HIT |
| `say 018D:0462 "rod of armor of flames "` | 「armor of flames 權杖」（未翻譯的片段保留英文） | HIT |
| `say 0596:0B87`（3 個片段 + 數字） | 「上面還顯示：現在的時辰是 Bloodwatch，今天是 Guarday，Stonemark 月第 3 天。」 | HIT |
| `say 040A:1F16 Something else` | 英文 | `SOURCE-MISMATCH` |

使用者未能在畫面上找到「Sea of Rains?」選項：該選項以中文「雨之海？」顯示，且只在選擇「什麼的岸邊？」之後出現；多頁與計時已由其他長句驗證。

### 單元測試

- `test_part_templates`：多個句型符合時選固定文字最多者；片段翻譯 / 未翻譯保留英文；整句條目優先。
- `test_reading_length`：ASCII、CJK、全形標點、其他 UTF-8、CP437 byte、部分範圍。
- `test_placeholders`：`partN` 的合法 / 不合法名稱（`part0`、`part01`、`part123`）、`param 18d:part2` 正規化。

### 工具

- `u8catalog.py update`：既有譯文全部保留（kept 63 → 93 含 POC），0 fuzzy、0 obsolete。
- `u8catalog.py check`：0 errors、0 warnings。
- `po_compile.py`：105 entries（20 templates），0 skipped。

## Acceptance（Master Plan §30）

| 項目 | 結果 |
|---|---|
| runtime numeric string | ✅ 金幣、試劑的 `{num}`（真實 Usecode）；時間 focus、魔杖（`say`） |
| name substitution | ✅ Devon `{name}`（P7）；Orlok `{varF7}` = 玩家名字 / 「陌生人」 |
| item substitution | ✅ Orlok `{call_0BCF}` 酒名；魔杖 `{part1}` / `{part2}`；試劑種類（依分支的整句） |
| multi-page Chinese | ✅ Devon 的長句（中文 2–4 頁），自動翻頁正常 |
| no premature disappearance | ✅ 使用者確認；中文每字 24 ticks，整句時間與英文相當 |
| no excessively long stale text | ✅ 使用者確認；比原版日文版的速度快 |

## Findings

### Observed

- U8 的動態句子幾乎都是「分支內串接字串常值」，少數是獨立片段的組合；依分支列舉 + 少量手寫的分段句型即可涵蓋，不需要翻譯最終組合的無限可能。
- 不少分支是互斥的條件（`if hour == 0 … if hour == 1 …`），不追蹤條件會產生大量不可能的組合（HOURGLAS 64+ → 7）。
- 中文行距 18 px 是台詞頁數增加的主因（每頁 3 行 vs 英文 5 行），而不是字寬。
- 原版日文版也把顯示速度調得比英文慢（`talkspeed` 24）。

### Inferred

- 正式翻譯時，同一呼叫點的單複數條目可以用翻譯記憶（`--tm` 只對相同英文有效）以外的方式加速，例如在 stats 中標示「同 context 的兄弟條目」；目前不急。
- 5 個無法解析的 bark 的文字來自呼叫端傳入的參數（§49 #8），需要跨函式的追蹤或人工處理。

## Files Changed

- `scummvm-src`（`4ce1d3e434`）：`misc/translation_catalog.*`、`misc/localization.*`、`misc/debugger.*`、`gumps/bark_gump.cpp`、`ultima8.cpp`、`test/engines/ultima/ultima8/misc/translation_catalog.h`
- 主 repo：`tools/extract/u8extract.py`、`tools/catalog/po_compile.py`、`tools/catalog/measure.py`（新）、`localization/README.md`、`localization/zh_TW/dialog/*.po`（17 個 class 重新產生 + POC）、`localization/zh_TW/authority.tsv`、本報告、Master Plan v2.8、HANDOFF

## Regressions

- 英文：`readingLength()` 對非 UTF-8 文字每 byte 算 1，與原本的 byte 長度相同 → 英文顯示時間不變。
- localization off：量測只在 `localization_measure=true` 且 localization 啟用時執行；其他路徑不變。
- 句型比對：既有的 P7 句型（Devon `{name}`）照常 HIT。

## Risks

- `PART_TEMPLATES` 是手寫的；遊戲資料不同版本時，抽取會以「句子不符合句型」的方式顯示（不符合的句子列為整句條目），不會靜默遺漏。
- 路徑列舉的上限（64）下，若未來發現遺漏的句子，可提高上限重跑比對（本次已驗證與 1,024 相同）。
- 權威檔中 14 個 proposed 詞是 POC 用，尚未經使用者核可。

## Blockers

無。

## Next Phase Readiness

Phase 12（Save / Speech / Regression Hardening）可以開始：存檔只存英文（P5–P7 已有工具 `save_text_check.py`）、有語音的 NPC（§49 #18）、全面回歸。

## STOP

等待使用者指示。
