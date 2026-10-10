# Handoff — Ultima VIII 繁體中文化專案

**更新日期：** 2026-10-10（P16 快捷圖示列 PASS；P15 高解析文字層 PASS，打包 v0.9.1-beta）
**目前進度：** Phase 0–13 ✅ PASS（P13 報告 `docs/reports/P13-full-translation.md`），Phase 14（打包）✅ PASS（報告 `docs/reports/P14-packaging.md`，產生方式見 §8 末）。**P15 高解析文字層 ✅ PASS**（報告 `docs/reports/P15-hd-text-layer.md`，見 §8 末）。其他待使用者決定：Release 呈現方式（使用者想參考「叛變克朗多」專案的 `dist/release_v100_zh`）、Mac 版（GitHub Actions）、P15 高解析文字層（Master Plan §34、§48）。舊摘要：Phase 0–12 ✅ PASS（**核心 localization 架構已證明**，P7）。**Phase 13（正式翻譯）進行中**：第一批（開場 → 碼頭處決 → 城內衛兵）已完成並經使用者試玩確認。下一步見 §8。

給接手的 Agent：請先完整閱讀本文件，再讀 [Master Plan](../ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md)（目前 v2.9，開頭有修訂紀錄，§18.1 有進度表，§49 是待辦總表）。翻譯檔的格式與流程見 [localization/README.md](../localization/README.md)。

---

## 1. 與使用者合作的規則（重要）

| 規則 | 說明 |
|---|---|
| **一律用正體中文回覆** | 程式碼、檔名、ID 可維持原樣。報告與文件沿用「繁中 + 英文術語」風格 |
| **Phase Gate** | 每個 Phase 做完就 STOP、寫報告（`docs/reports/P<n>-*.md`），**等使用者明確指示才進下一個 Phase**。使用者說「繼續」「開始 Phase N」即為指示 |
| **push** | 主 repo 已公開於 GitHub：https://github.com/pmanyeh/Ultima-8-for-ZH（2026-10-08 起，使用者要求時才 push）。`scummvm-src` 的開發分支推到使用者的 fork：https://github.com/pmanyeh/scummvm（`ultima8-zh-tw-dev`）。**絕不 push 到官方 upstream**：遠端 `upstream` = scummvm/scummvm（push 網址已設成無效），`origin` = 使用者的 fork；也不要從 fork 建立 PR（預設目標是官方）。README 的翻譯進度用 `tools/catalog/progress.py zh_TW` 更新 |
| **commit** | 每個 Phase 完成時 commit：`scummvm-src`（引擎）與主 repo（報告、工具、翻譯檔）分別 commit |
| **計劃可依實證調整** | Master Plan 會依實際情形修訂；有落差時更新計劃並在修訂紀錄中說明 |
| **遊戲內測試由使用者操作** | 使用者偏好自己操作遊戲：給出明確的步驟（啟動檔、主控台指令、要看什麼），測完再由 Agent 讀 log / 存檔驗證。使用者可能同時在用桌面，**不要自行操作遊戲視窗**，除非使用者要求；啟動後立刻關閉的 `startup_check.ps1` 可以用 |
| **權威檔** | 使用者要求：人名、地名、物品、魔法、怪物、專有名詞**一律依 `localization/zh_TW/authority.tsv`**，確保前後一致（見 §6） |
| **不大量翻譯** | Master Plan I10：開發階段只做少量 POC 譯文。正式大量翻譯要等工具與權威檔就緒、使用者同意 |
| 使用者背景 | 做過 U7（Exult）中文化：`D:\git\Exult-for-zh`、`D:\git\Ultima7-zh-TW\BlackGate`。U7 是改寫 Usecode 字串再重新編譯；本專案**不改** Usecode。U7 的墓碑等是全部改中文 |

---

## 2. 專案核心架構（已確定）

**Presentation-time localization：遊戲邏輯永遠使用英文原文，只在建立顯示元件時把文字換成中文。**

理由（P1 實證）：Usecode 以英文字串**內容**決定對話分支（`strcmp`，區分大小寫），語音以英文比對，存檔中存有 string heap。

### 翻譯的 ID（context）

| context | 用途 | 取得方式 |
|---|---|---|
| `bark CCCC:IIII` | NPC 台詞、查看物品 / 人物的名稱 | `Item::I_bark` 執行時 running `UCProcess` 的 `classId:ip`（IP 指向 calli） |
| `ask CCCC` + 英文 | 對話選項 | `Item::I_ask` 時 running process 的 class；同 class 同英文 = 同一選項 |
| `book` / `scroll` / `grave` / `plaque CCCC:IIII` | 書、捲軸、墓碑、牌匾 | 讀物 intrinsic（0x6E–0x71）的呼叫點 |
| `param CCCC:varXX` / `call_XXXX` / `partN` | 句型參數的值 | 同 class 的參數譯文 |
| `ui` + 英文 | 引擎介面文字（主選單、離開確認、日記、死亡墓碑） | `Localization::uiText(英文, 字型)` |

- 查表 key = `context + "\x04" + 英文原文`（gettext 慣例）。英文必須**完全相同**（含結尾空白）。
- **句型**：msgid 含 `{name}` `{num}` `{varXX}` `{call_XXXX}` `{partN}`，比對時取出參數，填入譯文（P7）。同一呼叫點可有多個條目（依分支組出的不同句子，P11）；多個句型都符合時採用固定文字最多者。
- **Fallback**（ADR-001 D5）：查不到、英文不符、格式錯誤、找不到翻譯檔、字型不能畫 UTF-8 → 一律顯示英文。CJK 字型載入失敗 → 停用翻譯。
- **存檔只有英文**：`TextWidget::setSaveText()`、`ButtonWidget::setSaveText()`。讀檔後，存檔當下正在顯示的那一句 / 那組選項會是英文（使用者已同意）。

### 翻譯檔

- **PO**，每個 Usecode class 一檔：`localization/zh_TW/dialog/CCCC_NAME.po`（394 檔、6,829 條），依對話流程排列；`ui/engine.po`（12 條）。**英文原文放進 repo**（使用者決策，ADR-002）。
- 執行時讀編譯後的單一檔 `u8_zh_TW.mo`（gettext MO；英文 key 以 CP437 編碼，與遊戲的 byte 一致）。
- 設定（game domain）：`localization=off|zh_TW`、`localization_file`（預設 `u8_<語言>.mo`）、`font_cjk_file`（預設 `Cubic_11.ttf`）、`font_cjk_size`（12）、`font_cjk_antialiasing`（false）、`font_cjk_letter_spacing` / `font_cjk_latin_spacing`（中文與英數之間）/ `font_cjk_line_spacing`（額外像素，預設 0；引擎 2026-10-09 加入）。**CJK 字型只在 localization 啟用時載入**；只替換 `[fontoverride]` 中的字型 0、5–9。

### 引擎程式（`scummvm-src/engines/ultima/ultima8/`）

| 檔案 | 內容 |
|---|---|
| `misc/translation_catalog.*` | 讀 MO、查表、句型比對、`readingLength()`（計時用，CJK 字算 3）（只依賴 `common/`，可做單元測試） |
| `misc/localization.*` | 設定、啟用條件、`translateBark` / `translateAnswer` / `translateCallSite` / `translateUI` / `uiText`、`measureCatalog()`（P11） |
| `world/item.cpp` | `I_bark`、`I_ask` 掛點 |
| `gumps/bark_gump.*`、`ask_gump.*` | `_displayText`、`_displayAnswers`（不存檔）；台詞顯示時間依 reading length（P11） |
| `gumps/book_gump.*`、`scroll_gump.cpp`、`readable_gump.*` | 讀物掛點；墓碑 / 牌匾為英文 + 中文字幕 |
| `gumps/menu_gump.cpp`、`quit_gump.cpp`、`u8_save_gump.cpp`、`world/actors/avatar_death_process.*` | 介面文字（P9） |
| `gfx/fonts/font.*`、`tt_font.*`、`font_manager.*`、`games/game_data.*` | UTF-8 / CJK 字型（P3）、`isUTF8()`、CJK override |
| `misc/debugger.*` | 主控台指令（§4） |

---

## 3. 目錄與 Repo

```text
D:\git\Ultima 8 for ZH\                  ← 主 repo（git, branch main，最新 commit 見 git log）
├── ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md   ← v2.9
├── docs/
│   ├── HANDOFF.md                        ← 本文件
│   ├── reports/P0..P12-*.md              ← 各 Phase 報告
│   ├── research/u8-text-pipeline.md      ← P1 文字流程研究
│   ├── research/text-surface-inventory.md ← P8 全部文字 surface 盤點（26 類）與 Phase 分配
│   └── architecture/ADR-001（ID）, ADR-002（格式、工具鏈、權威檔）
├── localization/
│   ├── README.md                         ← 翻譯檔格式、要保留的符號、流程（給譯者）
│   └── zh_TW/
│       ├── dialog/CCCC_NAME.po           ← 394 個 class（自動產生 + 合併）
│       ├── ui/engine.po                  ← 介面文字
│       └── authority.tsv                 ← 權威檔
├── tools/
│   ├── catalog/u8catalog.py              ← update（抽取 + 合併）/ check / stats / terms
│   ├── catalog/po_compile.py             ← PO → MO
│   ├── catalog/measure.py                ← 譯文頁數 / 寬度量測報表（P11）
│   ├── extract/u8extract.py              ← 依對話流程抽取；依分支列舉句子、PART_TEMPLATES（P11）
│   ├── diagnostics/u8dis.py              ← Usecode 反組譯（515 class，0 desync）
│   ├── diagnostics/text_survey.py        ← 各類文字的呼叫點與字數統計
│   ├── diagnostics/u8shapes.py           ← shape 檔 → PNG（只在本機看，圖片不進 repo）
│   ├── validate/font_coverage.py         ← 字集覆蓋檢查
│   ├── validate/save_text_check.py       ← 存檔中有 CJK 文字就失敗
│   ├── validate/save_compare.py          ← 存檔逐區段比較（P12，只檢查遊戲資料區段的中文）
│   ├── build/                            ← 建置與測試腳本（§4）
│   └── automation/scummvm_window.ps1、startup_check.ps1、save_matrix.ps1、regression_startup.ps1（P12）
├── Ultima 8/          （gitignored）GOG 遊戲資料，唯讀；英文版在 Ultima 8\ENGLISH\
├── private_test/      （gitignored）啟動檔、設定檔、字型、u8_zh_TW.mo、存檔、log
└── scummvm-src/       （gitignored，獨立 git repo）ScummVM upstream clone
```

### `scummvm-src` 分支

| 分支 | Commit | 用途 |
|---|---|---|
| `master` | `71cb05b1c0` | upstream 基準（2026-10-05） |
| `exp/u8-p2-identity-spike` | `2063e25a89` | P2 spike，**只供參考，不合併** |
| `ultima8-zh-tw-dev` | `1882ba7ba5` | **正式開發分支**（目前 checkout）。P3 `96bfc46318`、P4 `b0efb70a44` `d6192426af`、P5 `a1a2282aae`、P6 `b04657abfb`、P7 `5a8b1e7e5b`、P9 `cb69291575`、P10 `47541ad4bb`、P11 `4ce1d3e434`、P12 `91c8b8598a`、名稱加註 `e674111a51`、P13 選項句型 `1882ba7ba5`（P8 只有研究，無引擎修改） |

建置目錄（`scummvm-src/` 內，gitignored）：`build-scummvm/`（原版）、`build-trace/`（Usecode trace）、`build-spike/`、**`build-dev/`（開發分支，Debug x64）**。

---

## 4. 建置、測試與執行

### Windows（MSVC）

- VS 2026 Community（MSVC 14.51）、vcpkg 在 `D:\vcpkg`（master）、相依套件在 `D:\vcpkg\installed_scummvm`。只啟用 ultima 引擎。
- `tools\build\build_dev.bat`：重新產生專案並建置開發分支（增量約 1–3 分鐘）。Agent 以 PowerShell 執行：
  `& cmd /c "`"D:\git\Ultima 8 for ZH\tools\build\build_dev.bat`" > <log> 2>&1"`
- **遊戲執行中無法建置**（`LNK1168`：scummvm.exe 被鎖住）。請使用者先關閉遊戲，不要自行結束使用者的程序。
- 其他：`build_baseline.bat Debug|Release`（原版）、`build_trace.bat`。

### 單元測試（WSL Ubuntu）

MSVC 的 `--tests` 模式會停用所有引擎，所以在 WSL 跑（**用 PowerShell 工具執行**；Git Bash 會改寫 `/mnt/...` 路徑）：

```powershell
wsl -d Ubuntu -- bash "/mnt/d/git/Ultima 8 for ZH/tools/build/wsl_unit_tests.sh"
```

- 目前 **483 項全部 OK**。本專案的測試：`test/engines/ultima/ultima8/gfx/font_utf8.h`（P3）、`misc/translation_catalog.h`（P4–P10）。
- **MSVC 與 g++ 都要建置**：MSVC 把 C4701（可能未初始化）當錯誤。
- **單元測試只能用不依賴 `Kernel` 的物件檔**，否則靜態函式庫會拉進整個引擎與 GUI 而無法連結。gump / widget 只能在遊戲中測。

### 執行遊戲（`private_test/`）

| 啟動檔 | 內容 |
|---|---|
| `launch-dev.bat [slot\|new] [en\|nosub\|mute]` | **開發分支**，`--debugflags=Localization`。`new` = 新遊戲（一開始就進入與 Devon 的第一次見面）；`en` = localization off（`scummvm-dev-en.ini`，共用存檔）；`nosub` = 關字幕、`mute` = 關語音（P12） |
| `launch-p0.bat`、`launch-trace.bat`、`launch-spike.bat` | 原版、Usecode trace、P2 spike |

- 設定檔：`scummvm-dev.ini`（`localization=zh_TW`、`font_cjk_file=Cubic_11.ttf`、`originalsaveload=true`）。ScummVM 會自動改寫 ini，屬正常。
- `--extrapath=private_test\extra`：Cubic_11.ttf、`ultima8.dat` 複本、**`u8_zh_TW.mo`**（改了 PO 要重新編譯，見 §6）。
- 每次執行產生 `private_test/dev-YYYYMMDD-HHMMSS.log`；`[U8-L10N]` 行顯示每次查表（HIT / MISS / SOURCE-MISMATCH）。
- 存檔：`saves/ultima8.001`（p1-after，已認識 Devon）、`.002`（P5：主角說話中存檔）、`.003`（P6）、`.004`（P9 日記測試）；`.000` 是 ScummVM 自動存檔。
- `startup_check.ps1 -Config <ini>`：啟動、等初始化、關閉、列出 log（不操作視窗）。
- **存讀檔矩陣**：`save_matrix.ps1 [-Slot n]`（自動存檔需約 5 分鐘 × 2 階段，會開遊戲視窗，**先告知使用者**），結果用 `save_compare.py A B --baseline C` 比較。
- **啟動回歸**：`regression_startup.ps1`（9 種設定情境，各約 8 秒）。
- **分頁量測**：複製 `scummvm-dev.ini`，在 `[ultima8]` 加 `localization_measure=true`，用 `startup_check.ps1 -Config <該 ini> -Seconds 40 -Log measure.log` 執行，再 `python tools/catalog/measure.py measure.log`（說明在檔頭）。P4 的 7 種情境設定在舊 session 的 scratchpad，需要時重建（off / zh / 缺翻譯檔 / 損壞 / 語言不符 / 缺字型 / 未設定）。

### 主控台指令（遊戲中 `Ctrl+Alt+D`）

| 指令 | 用途 |
|---|---|
| `Localization::info` | 翻譯狀態（語言、翻譯檔、條目數、字型） |
| `Localization::bark <class>:<ip>` | 主角以 localization 路徑說出翻譯檔中的一句台詞 |
| `Localization::say <class>:<ip> <英文>` | 主角以該呼叫點說出任意英文（測試句型與參數；用雙引號保留空白） |
| `Cheat::toggle`、`Cheat::items` | 背包放入金幣、試劑等（查看即走真實 Usecode，P11 用來測 `{num}`） |
| `Localization::read book\|scroll\|grave\|plaque <class>:<ip>` | 直接開啟讀物（不必走到物品旁） |
| `Localization::gravestone` | 只顯示死亡墓碑（主角不會死） |
| `Localization::guardianBark <1-23>` | Guardian 的嘲諷（有語音 `E666.FLX`），測語音 / 字幕；3 / 12 / 16 有 POC 譯文 |
| `Ultima8Engine::barkTestFile p3_test_strings.txt <n>` | 字型繪製測試 |

---

## 5. 已知陷阱

1. **Shell 會破壞反斜線**：Bash heredoc、`sed`、`printf` 處理 `\n`、`\x`、`\\` 時常出錯；Python 一般字串中的 `\u` 也會被當成跳脫。**P11 再次發生：即使是 `<<'EOF'` 的 heredoc，裡面的 `\\n`、`\\x` 也被變成真正的換行 / 字元。** 修改原始碼請用 Edit / Write 工具，或把 Python 腳本用 Write 寫成檔案再執行（腳本放 scratchpad）。
2. **`_UTF8` 是 Windows 系統標頭的巨集**：變數命名避開（用 `_utf8`）。
3. **原版英文含 CP437 字元**（4 句德文 / 法文）：字型以 CP437 逐 byte 解碼不合法的 UTF-8；PO 以 UTF-8 存放，編譯時 key 轉回 CP437。
4. **對話中無法存檔**（`setAvatarInStasis`），原版設計。
5. **ScummVM 預設用自己的存讀檔畫面**：要 `originalsaveload=true` 才會用 U8 原版日記。ScummVM **沒有繁中介面翻譯**（`po/zh_Hant.po` 是空的），ScummVM 自己的選單是簡中或英文，不在本專案範圍。
6. **`EditWidget` 用 high-res CJK 字型時文字畫到錯誤位置**（§49 #23，使用者：之後再修）。目前日記字型（4）不替換。
7. **`TTFont::renderText` 原本會寫出圖片範圍**（游標在行尾），P9 已修正。
8. Git 全域 `core.autocrlf=true`：主 repo 用 `.gitattributes`（`eol=lf`，`.bat` 為 crlf）；`scummvm-src` 的部分檔案是 CRLF，修改腳本要保留原本的換行。
9. 主控台輸出中文會變亂碼（cp950），驗證時用 `ascii()` 或寫檔比對。
10. **增量連結可能沒把新程式連進 `scummvm.exe`**（2026-10-10 發生：改了圖示的圖框，畫面一直不變；obj 與 `ultima.lib` 是新的，exe 是舊的）。畫面或行為不符合預期時，先刪掉 `build-dev/Debugx64/ultima.lib` 和 `scummvm.exe` 再建置。

---

## 6. 翻譯檔流程與權威檔

```bash
python tools/catalog/u8catalog.py update zh_TW        # 抽取 + 合併（保留譯文；--tm 帶入相同英文的譯文為 fuzzy）
python tools/catalog/u8catalog.py terms zh_TW         # 更新權威檔候選詞（保留手動欄位）
python tools/catalog/u8catalog.py check zh_TW --font private_test/extra/Cubic_11.ttf
python tools/catalog/u8catalog.py stats zh_TW         # 進度、重複、不一致（--csv 報表）
python tools/catalog/po_compile.py zh_TW localization/zh_TW -o private_test/extra/u8_zh_TW.mo
python tools/catalog/batch.py dump zh_TW <class>...    # 依對話流程列出未翻條目（P13）
python tools/catalog/batch.py apply zh_TW <file> --comment "P13 batch N"   # 套用譯文（檢查控制字元、佔位符號）
python tools/catalog/progress.py zh_TW               # 更新 README / README_EN 的翻譯進度
```

- **權威檔** `localization/zh_TW/authority.tsv`：欄位 category / english / translation / status / count / example / note。status：`keep`（保留英文）、`approved`、`proposed`、`todo`。`check` 依 keep / approved 檢查譯文。
- 目前（2026-10-08）：756 詞，**使用者已翻譯全部譯名**：approved 17、proposed 720、ignore 19（不是專有名詞）。審閱修正：Lithos = 利索斯（潛伏者是 Hydros）、巫師 / 巫術、魔法書用法術全名等。使用者還在找舊版中文手冊，可能再調整。新欄位 `annotate`。
- 譯名已全部決定（proposed）；正式翻譯時譯文一律用權威檔的中文名稱，不自己加英文（引擎會自動加註）。
- 翻譯進度（2026-10-08）：6,944 條（含 ui），**已翻 1,003 條**（以英文字元計 11.2%）。README 的進度用 `python tools/catalog/progress.py zh_TW` 更新。
- 權威檔 758 詞（P13 加 Nystul 尼斯圖、Pellgun 佩爾岡）。

---

## 7. 已完成的 Phase（摘要）

| Phase | 結果 | 報告 |
|---|---|---|
| P0 Baseline | 建置、執行原版 | [P0](reports/P0-baseline.md) |
| P1 Text Architecture Audit | 文字流程、存檔、語音研究 | [P1](reports/P1-text-architecture-audit.md) |
| P2 Translation Identity | ID 設計（ADR-001）、格式（ADR-002）、spike → GO | [P2](reports/P2-translation-identity.md) |
| P3 UTF-8 / CJK Foundation | UTF-8 字型、中文換行與禁則、Cubic 11 | [P3](reports/P3-cjk-foundation.md) |
| P4 Localization Manager | 翻譯檔（MO）、查表、fallback、字型條件 | [P4](reports/P4-localization-manager.md) |
| P5 NPC Bark POC ★ | 台詞中文；存檔只存英文 | [P5](reports/P5-npc-bark-poc.md) |
| P6 AskGump Choice POC ★ | 選項中文；點中文選項進入原本分支 | [P6](reports/P6-askgump-choice-poc.md) |
| P7 First Complete Conversation ★ | Devon 第一次見面全程中文；句型（`{name}`）提前實作；**核心架構已證明** | [P7](reports/P7-first-complete-conversation.md) |
| P8 Text Surface Inventory | 26 類 surface | [P8](reports/P8-text-surface-inventory.md) |
| P9 Engine UI / Static Text | `ui` context；主選單 / 離開確認改文字（日文版做法）；死亡墓碑字幕 | [P9](reports/P9-engine-ui-static-text.md) |
| P10 Extraction & Toolchain | 全遊戲翻譯檔、合併 / 檢查 / 統計、權威檔、讀物 | [P10](reports/P10-extraction-toolchain.md) |
| P11 Dynamic Strings / Pagination / Timing | 依分支列舉句子、`{partN}`、酒名等參數；顯示時間改為 reading length；分頁量測（不調整版面） | [P11](reports/P11-dynamic-strings-pagination-timing.md) |
| P12 Save / Speech / Regression | 存讀檔矩陣（中英互換，邏輯區段一致）、語音矩陣、啟動回歸 9 情境；日文計時修正 | [P12](reports/P12-save-speech-regression.md) |

### 使用者已做的決定

- 翻譯檔用 PO、英文原文放進 repo（ADR-002）。
- **專有名詞改用中文**（2026-10-08，使用者翻譯了整份權威檔）：不再保留英文（原本的 keep 已改為中文譯名）。
- **名稱自動加註**（2026-10-08）：同一次對話中第一次出現的名稱顯示「中文(English)」，之後只顯示中文；書 / 捲軸每次打開重新計算；**對話選項不加註**（使用者決定）；半形括號。由權威檔的 `annotate` 欄決定（空白 = person / place / faction 加註），`po_compile.py` 編成 `term` 條目，設定 `localization_annotate`。
- 字型 Cubic 11（12px、關閉反鋸齒）。
- 讀檔後正在顯示的那一句 / 選項以英文顯示：可接受。
- 含玩家名字的句子：P7 一併處理（已完成）。
- 墓碑 / 牌匾 / 死亡畫面：**先採方案 A**（英文雕刻 + 中文字幕），之後再評估全中文（使用者的 U7 是全中文）。
- 製作人員名單、開發者語錄：**都不翻譯**。
- 角色狀態欄（STR / INT…）維持英文（放不下中文）。
- 主選單、離開確認：改為中文文字按鈕（日文版做法），不製作中文圖片。
- `EditWidget` 的 high-res 問題：之後再修。
- **維護權威檔**。
- P11：分頁增加約 8%，不調整版面（測試通過）；顯示時間 CJK 字算 3 個英文字母。
- #27：目前不調整；之後可縮小行距或只在中文時加大台詞框。#28：14 個 proposed 譯名先使用，使用者會依舊版中文手冊再調整。
- P12：語音四種情境都自然。「全語音 / 中文語音」是使用者之後的想法（§49 #29，條件成熟再說）。

---

## 8. Phase 13（正式翻譯）進行中

### 已完成：第一批（使用者要錄影向同好宣告專案）

範圍：新遊戲開場 → 走到泰尼伯瑞城門 → 碼頭處決 → 進城。使用者試玩兩次，log 確認路線上全部 HIT。

| class | 內容 |
|---|---|
| 0402 戴文（全部）、0483 處決過場、0061 托蘭、0407 莫爾迪亞、0404 城門衛兵、0408 塔娜、0413 夏娜、0412 芮安 | 560 條 |
| 04C3 碼頭審問、METHOD 057C 中處決 / 衛兵日誌的句子、Guardian 嘲諷全部 23 句（0401 event 15）、魚 / 籃子 / 絞盤等物品、含名字的選項 | 64 條 |
| 泰尼伯瑞城內衛兵 GUARD2–10、GUARDMAN、GUARD_EW | 271 條 |

### 已完成：第二～六批（2026-10-09，尚未試玩）

所有對話角色與物品文字已翻完（進度 76.1%，6,692 / 6,995 條）：泰尼伯瑞主要角色（班提克、歐洛克、珍娜、薩金德、達里恩、科里克、奇蘭卓、阿拉米娜）、平民 / 小孩 / 乞丐、米斯蘭、維維多斯與地下墓穴的古代死靈法師、托溫、白銀之岩（史泰洛斯、席勒斯、薩維爾、神術師）、牧民夫婦威廉與柯林斯、巫師聚落（貝倫、貝恩、瓦爾迪恩、戈格隆德、馬爾奇爾、阿卡迪昂、門徒）、四泰坦、派羅斯召喚、戴文的審判、物品名稱、作弊選單。譯者註解 `# P13 batch 2`～`6`。

- 風格：歐洛克海盜腔、括號裡的「真心話」是聆聽真言法術的效果；薩金德用「咱們」的居高臨下語氣；貝恩給主角取的真名「戴蒙」意為「天空之火」，罵人的「戴蒙癡」= 腦中之火；咒語（In Flam! 等）保留原文、驚嘆號改全形。
- 文字雙關改寫：歐洛克「What's yer poison?」→「想來點什麼毒藥？」；阿拉米娜 murder→mother 改成「謀殺／模範」。
- 新出現的人名（未加入權威檔，只出現一兩次）：瑟卡（Cekar）、艾蓮娜（Elaina）、艾莉安娜（Arianna）、卡佩斯（Karpese）、班托斯（Bentos）、雪比／波諾（托拉克斯獸）、門徒名 卡達斯／戴摩斯／柯修斯／門塔／塔隆／艾姆里柯；船名（黑夫人號等）；週日名（守護日、大地日…）、月名（石痕月…）。
- **第七、八批**（同日）：墓碑、牌匾（字幕不必照雕刻的 `*` 換行，batch.py 已比照 check 放寬）、全部的書與捲軸。進度 **99.8%（6,944 / 6,995）**。剩下 51 條是刻意不翻的：作弊選單的亂碼密碼與座標資訊、數字選項 0–9、`.`、0575 / 058A 名字缺漏的兩句。
- **片頭動畫字幕**（EINTRO.SKF，守護者的 5 句）存在動畫檔裡，原本沒抽到也沒查表：引擎 `skf_player.cpp` 改用 `Localization::uiText`，譯文在 `localization/zh_TW/ui/movies.po`（ENDGAME.SKF 沒有字幕）。
- 字型 Cubic 11 缺「愫」「懨」，已改用其他字；之後新增譯文請看 check 的 font 警告。
- 書中新名字（未加入權威檔）：伊拉丹、納戴爾、諾蘭德魯、溫特羅斯、托戴姆、崔克斯特、史拉戴克、布羅格丹、格林修士、傑利（Jelly，人名，非權威檔的肉凍）、維泰克中尉、德洛卡、特雷卡斯特、羅賓．達德利等。

### 第二～六批發現的抽取問題

- **已修正**：清單一次放入多個選項時只抽到最後一個（薩維爾的智慧考驗選項、五芒星陣與死靈法師之鑰的咒語、貝倫的魔鬼之口等，新增 51 條）。`site_variants()` 現在也沿分支列舉選項清單（貝恩的「Please forgive me」+「, kind lady.」/「, Bane.」）。
- **未修正**：巫師門徒（0575 SORCERER）用清單隨機取名（Cardas…），名字存在 local 裡，抽取工具沒把它當參數，`My name is {名字}. And you are?`、`{名字}, the late Sorcerer` 會顯示英文；058A 的 `He calls himself, .` 同樣原因（名字缺）。需要讓抽取工具把「從清單取值的 local」當成參數。
- 0575 的 Cardas 等名字被當成選項抽出（其實是取名清單），無害。

翻譯工具：`tools/catalog/table.py`（prefill / view / fill，用法見檔頭）——對照表方式一批可處理數百條。

譯文附譯者註解 `# P13 batch 1`。翻譯風格：莫爾迪亞傲慢、城門衛兵粗俗口語（俺）、芮安的 `-sob-` → （啜泣）、`-sniff-` → （抽噎）、`-強調-` 改用「」或語氣；貨幣 stones / blacks → 黑曜石幣；選項「Goodbye.」→「再見。」。英文原文誤打的 tab 在譯文中省略（check 會有 tab 警告，可忽略）。

### P13 中修正的工具與引擎

- **選項句型**：含玩家名字的選項（`I am {name}.`，全遊戲 36 個）→ `ask` context 也支援句型（引擎 `1882ba7ba5`、抽取工具、po_compile / check）。
- **代為發話**：字串當參數傳給別的 class 的函式說出（`METHOD 057C:087D` 說出參數 → `bark 057C:088A`）。抽取工具以 `passed_strings()` / `param_bark_sites()` 追蹤，**新增 79 句過去完全沒抽到的台詞**（處決群眾、派羅斯召喚場景、法術咒語等），條目放在被呼叫的 class 檔（註解 `said for <caller>`）。
- 翻譯小工具：`tools/catalog/batch.py`（dump / apply）；大量重複句子可用「英文 ||| 中文」對照表產生 blocks（本 session 用 scratchpad 腳本 `distinct.py`，需要時重寫）。

### 下一步（使用者已授權由 Agent 決定翻譯順序）

1. **請使用者試玩**（泰尼伯瑞全城、高原、墓地、白銀之岩、巫師聚落、書），讀 log 補 MISS；修抽取工具的「清單取名」缺口（見上）。之後可做全文校潤、權威檔補新人名、P14 打包。
2. 每批：`batch.py dump` → 閱讀上下文翻譯 → `apply` → `check` → `po_compile` → `progress.py` → commit；請使用者試玩，讀 log 補 MISS。
3. 使用者要求時才 push（兩個 repo：主 repo `origin/main`，引擎 `origin/ultima8-zh-tw-dev`）。目前本機有尚未 push 的 commit。
4. 其他待討論：是否貢獻 upstream（使用者目前**不要**送到官方）。

### P14 打包（2026-10-09）

- 使用者決定：Windows 免安裝包、全專案 GPL-3.0（根目錄 `LICENSE`）、ScummVM 遊戲選項勾選框 `localization_zh_tw` / `localization_annotate`（預設開啟；未設定任何語言鍵時也預設 zh_TW）。
- 產生：`tools\build\build_release.bat`（Release x64）→ `tools\package\make_package.ps1 [-Version 0.9.0-beta] [-Test]` → `dist\Ultima8-zhTW-<版本>\` 與 zip。玩家文件原稿在 `package/`。
- 套件只附 Cubic 11；使用者自用的細明體（`chinese.ttf`）不可散布。
- 2026-10-10：套件另附 jf open 粉圓（高解析用）。可攜設定改由 `package/scummvm.ini` 複製（UTF-8、每個設定一行中文 `#` 註解；ScummVM 改寫時保留註解但重排順序，所以註解要自成一句，可選設定列在 `[scummvm]` 之前的區段說明）。玩家設定說明 `package/SETTINGS.zh-TW.md`。最新包：**v0.9.2-beta**（`dist/`，未上傳）。
- 使用者已驗收（2026-10-09：運作良好，中文顯示正常）。待決定：發布管道（GitHub Releases 等，需使用者同意才上傳）。

### P15 高解析文字層（2026-10-10 PASS）

- 遊戲照舊畫在 320×200，每幀最近鄰放大到視窗大小的 `_hdScreen`，再由 `PaintCompositing` 畫高解析字型的 `TextWidget` 與片頭字幕。滑鼠座標在 `handleEvent` 換回遊戲座標；游標圖放大。
- 設定：`hd_text`（勾選框，**預設開啟**）、`hd_text_size`、`font_cjk_hd_file` / `_size` / `_antialiasing` / `_border` / `_letter_spacing` / `_latin_spacing` / `_line_spacing`（**單位是遊戲像素，可有小數**）。細節見 P15 報告。
- `FontManager::_hdOverrides`：只有 `TextWidget`（`getGameFont(n, true, true)`）與 `SKFPlayer` 用；其他地方仍用 12 px 字型。HD 開啟時一般字型的 `isHighRes()` 為 false。
- 自動測試：scratchpad 的 `hdshot.ps1`（需要時重寫）：啟動 → 等 log 出現某行 → PostMessage 按鍵 / 點擊 → Alt+S 截圖（`[scummvm] screenshotpath`）。**`PrintWindow` 對 OpenGL 視窗會拿到過時畫面**。
- 使用者選定高解析字型 **jf open 粉圓**（引擎預設、打包附上，授權檔 `private_test/extra/jf-openhuninn-OFL.txt`）。屬性頁標籤在高解析層下翻成中文（使用者要求）。打包版預設開啟（使用者 2026-10-10）。

### P16 快捷圖示列（2026-10-10 PASS）

- 報告 `docs/reports/P16-quick-bar.md`。右下角 5×2 圖示（背包、屬性、戰鬥、地圖、選單、鑰匙圈、召回石、睡袋、存檔、讀檔），呼叫與按鍵相同的 `handleActionDown`；滑鼠移到右下角才出現；中文提示；不存檔。設定 `quick_bar`（預設開）、`quick_bar_autohide`。
- 自動化測試限制：PostMessage 送的滑鼠移動不會真的移動遊戲游標（點擊有時有效），懸停相關的行為要請使用者試玩。測試時用 `quick_bar_autohide=false` 讓圖示常駐；截圖後要多等幾秒再關遊戲，否則截圖與 log 尾端會沒寫完（`.tmp`）。
- 作弊圖示組（左下角，`cheat=true` 時才出現）：同一個 `QuickBarGump`，種類 `CHEATS`；屬性全滿、體力恢復、無敵、hackMover。穿牆（clipping）只對 ScummVM 的快速移動模式有效、一般走路無效，所以沒放。

### Master Plan §49 尚未完成的待辦

| # | 項目 | 處理時機 |
|---|---|---|
| 8–9 | 5 個無法自動解析的 bark（PYROS、SORCERER ×2、METHOD ×2，文字來自呼叫端參數）、共用 class 的對話脈絡 | 翻譯時 |
| 11 | 建立 ScummVM fork 並改為 submodule | 待使用者決定 |
| 12 | HD 文字層 | ✅ P15 PASS |
| 14 | 原版換行無限迴圈的修正可回報 upstream | — |
| 15 | 遊戲選項 GUI 的語言選單 | 之後 |
| 16 | 翻譯檔加入遊戲資料版本（`EUSECODE.FLX` 雜湊） | 待定 |
| 20 | 墓碑、牌匾、死亡畫面：方案 A，之後評估全中文 | 待使用者評估 |
| 23 | `EditWidget` 用 high-res CJK 字型時位置錯誤 | 之後再修 |
| 24 | `TTFont::renderText` 越界修正可回報 upstream | — |
| 26 | 權威檔分類與 697 個待決定譯名需人工整理 | 正式翻譯前 |
| 27 | ~~台詞框行數~~ ✅ 2026-10-10：設定 `bark_lines`（每頁行數，高解析開啟時預設 4）、`bark_width`（預設 194），上限 300×100 遊戲像素；只影響中文台詞，存檔仍寫入原版 194×55（引擎 `63622f587d`） | — |
| 28 | P11 POC 的 14 個 proposed 譯名：使用者同意先使用，之後依舊版中文手冊調整 | 使用者查手冊後 |
| 29 | 全語音 / 中文語音（使用者的想法） | P15，條件成熟時 |
| 30 | upstream：`--save-slot` 讀檔前的自動存檔嘗試失敗後延後 5 分鐘（不影響遊戲） | — |
| 31 | ~~upstream：跳躍撞牆卡住 / 穿出地圖~~ ✅ 已修正（2026-10-10）：`AnimationTracker::step` 大步移動撞到物件時，`GetInterpolatedCoords(end, start)` 起點終點傳反，主角被放進物件裡；之後每個動作立刻失敗，主角移動控制在同一 tick 無限重跑（被 kernel 保護機制終止而卡死），或落下時掉到 Z < 0。改為 `(start, end)`，使用者確認不再卡住、不再穿牆。官方原版同樣有此 bug；使用者要求回報，已送出 [PR #7979](https://github.com/scummvm/scummvm/pull/7979)（分支 `ultima8-fix-jump-into-wall`，2026-10-10） | — |
| 32 | ~~upstream：字型快取（`FontManager::TTFHash`）以位址當雜湊~~ ✅ 2026-10-10 修正（引擎 `88656e047d`）：套用遊戲選項時可能當掉、字型重複載入。可考慮回報官方（需使用者同意） | — |

---

## 9. 重要數據（快速參考）

| 項目 | 數值 |
|---|---|
| Usecode class | 515（有文字的 394） |
| 翻譯條目 | 6,841：bark 4,761（38 個呼叫點有多個句子）、ask 1,775、param 54（var 11、call 5、part 38）、book 87、scroll 22、grave 67、plaque 63、ui 12 |
| 英文字元 | 約 539,000（台詞約 374,000、書約 117,000、選項約 35,000） |
| 顯示 | 台詞框 194×55：英文 5 行 / 頁、中文 3 行 / 頁（約 16 字 / 行）；中文每字 24 ticks（talkspeed 60） |
| 無法解析的 bark | 5 |
| 相同英文出現在多個 context | 506 句、1,433 個條目 |
| Devon | class `0402`；第一次見面 `0402:0633`「Hello there. 」；認識後 `060F`「Hello there, {name}.」 |
| Orlok（參數範例） | class `040A`；`{varF7}` = 玩家名字或 `stranger `；`{call_0BCF}` = 酒名 |
| 字型 | Cubic 11，10,268 字；目前譯文用到的字全部涵蓋 |
| intrinsic | bark `0x49`、ask `0x4A`、Book::read `0x6E`、Scroll::read `0x6F`、Grave::read `0x70`、Plaque::read `0x71`、getName `0xBC`、numToStr `0xB9`、setAvatarInStasis `0xD0` |
| 語音檔 | 只有 9 個（`SOUND/E44.FLX` 等，依角色 shape 編號），Devon 沒有 |
