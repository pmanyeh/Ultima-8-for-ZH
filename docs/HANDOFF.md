# Handoff — Ultima VIII 繁體中文化專案

**更新日期：** 2026-10-06
**目前進度：** Phase 0–4 ✅ PASS，**下一步：Phase 5（First NPC Bark Chinese POC），需等使用者明確指示才開始**

給接手的 Agent：請先完整閱讀本文件，再讀 [Master Plan](../ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md)（v2，開頭有修訂紀錄與進度表）。

---

## 1. 與使用者合作的規則（重要）

| 規則 | 說明 |
|---|---|
| **一律用正體中文回覆** | 程式碼、檔名、ID 可維持原樣。報告與文件沿用「繁中 + 英文術語」風格 |
| **Phase Gate** | 每個 Phase 做完就 STOP、寫報告，**等使用者明確指示才進下一個 Phase** |
| **不 push** | 兩個 repo 都只在本機 commit。目前尚未建立使用者的 GitHub fork |
| **commit** | 使用者已同意每個 Phase 完成時 commit（主 repo 與 `scummvm-src` 分別 commit） |
| **計劃可依實證調整** | 使用者明確表示 Master Plan 會依實際情形修訂；有落差時更新計劃並在修訂紀錄中說明 |
| 使用者背景 | 做過 U7（Exult）中文化：`D:\git\Exult-for-zh`、`D:\git\Ultima7-zh-TW\BlackGate`。U7 的做法是改寫 Usecode 字串（`.es` 腳本 → 重新編譯）；本專案**不改** Usecode |
| 使用者會同時操作遊戲 | 自動操作遊戲視窗前先確認，避免互相干擾 |

---

## 2. 專案核心架構（已確定）

**Presentation-time localization：遊戲邏輯永遠使用英文原文，只在顯示時把文字換成中文。**

理由（Phase 1 實證）：Usecode 以英文字串**內容**決定對話分支（`strcmp`，區分大小寫），語音以英文前綴比對，存檔中存有 string heap。

| 項目 | 決定 | 文件 |
|---|---|---|
| NPC 台詞 ID | `bark <class>:<Item::bark 的 calli IP>`，例如 `bark 0402:0633`。在 `Item::I_bark` 由 running `UCProcess` 的 `classId:ip` 取得 | ADR-001 |
| 對話選項 ID | `ask <呼叫 ask 的 class>` + 英文原文（含結尾空白），例如 `ask 0402 "Who are you? "` | ADR-001 |
| 動態句子 | 句型 + 參數：`{name}`、`{num}`、`{varXX}`、`{call_OOOO}`；參數值另有翻譯 `param <class>:<var>` | ADR-001 D3 |
| Fallback | 一律顯示英文（MISS、英文不符、格式錯誤、找不到表）；**字型載入失敗必須停用翻譯** | ADR-001 D5 |
| 翻譯檔 | **PO**，依 Usecode class 分檔，依對話流程排列；**英文原文放進 repo**（使用者決策）；執行時讀編譯後的單一檔案 | ADR-002 |
| 字型 | **Cubic 11（俐方體 11 號，OFL）12px，關閉反鋸齒**。U8 以 320×200 繪製，向量字型放大後模糊；HD 文字層留到 P15 | Master Plan §48 |

---

## 3. 目錄與 Repo

```text
D:\git\Ultima 8 for ZH\                  ← 主 repo（git, branch main）
├── ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md   ← v2
├── docs/
│   ├── HANDOFF.md                        ← 本文件
│   ├── reports/P0..P4-*.md               ← 各 Phase 報告
│   ├── research/u8-text-pipeline.md      ← P1 文字流程研究（最重要的背景資料）
│   └── architecture/ADR-001, ADR-002
├── localization/zh_TW/dialog/*.po       ← 翻譯原始檔（ADR-002）；目前只有 Devon 的 POC
├── tools/
│   ├── catalog/po_compile.py             ← PO → MO 編譯（引擎讀的單一翻譯檔）
│   ├── diagnostics/u8dis.py              ← Usecode 反組譯（515 class，0 desync）
│   ├── extract/u8extract.py              ← 依對話流程抽取（示範版，P10 擴充）
│   ├── validate/font_coverage.py         ← 字集覆蓋檢查
│   ├── build/                            ← 建置與測試腳本（見 §4）
│   └── automation/
│       ├── scummvm_window.ps1            ← 遊戲視窗截圖、點擊、按鍵
│       └── startup_check.ps1             ← 用指定設定檔啟動、等初始化完成、關閉、列出 log
├── Ultima 8/          （gitignored）GOG 遊戲資料，唯讀；英文版在 Ultima 8\ENGLISH\
├── private_test/      （gitignored）本機測試：啟動檔、設定檔、字型、存檔、log
└── scummvm-src/       （gitignored，獨立 git repo）ScummVM upstream clone
```

### `scummvm-src` 分支

| 分支 | Commit | 用途 |
|---|---|---|
| `master` | `71cb05b1c0` | upstream 基準（2026-10-05） |
| `exp/u8-p2-identity-spike` | `2063e25a89` | P2 spike（含翻譯查表的完整實驗），**只供參考，不合併** |
| `ultima8-zh-tw-dev` | `b0efb70a44` | **正式開發分支**，P3（`96bfc46318`）、P4 已 commit。目前 checkout 的分支 |

### 建置目錄（在 `scummvm-src/` 內，gitignored）

| 目錄 | 內容 |
|---|---|
| `build-scummvm/` | P0 原版（master），Debug 與 Release |
| `build-trace/` | master + `/DDEBUG_USECODE`（Usecode trace） |
| `build-spike/` | spike 分支 |
| `build-dev/` | **開發分支**（Debug x64） |

---

## 4. 建置與測試

### Windows（MSVC）

- 工具：VS 2026 Community（MSVC 14.51）、vcpkg 在 `D:\vcpkg`（master；CI 固定版本無法辨識 VS 2026）、相依套件裝在 `D:\vcpkg\installed_scummvm`。
- 只啟用 ultima 引擎：`create_project .. --msvc --vcpkg --disable-all-engines --enable-engine=ultima,ultima8`。
- 沒有執行 `vcpkg integrate install`，改以 msbuild 參數 `ForceImportAfterCppTargets` 匯入。

```bat
tools\build\build_dev.bat           ← 重新產生專案並建置開發分支（約 5–10 分鐘）
tools\build\build_baseline.bat Debug|Release   ← 原版 build-scummvm
tools\build\build_trace.bat         ← DEBUG_USECODE 版
```

（`gen_msvc_project.bat`、`install_vcpkg_deps.bat` 是第一次環境建立用的。）

### 單元測試（WSL Ubuntu）

MSVC 的 `--tests` 模式會停用所有引擎，所以 Ultima8 測試要在 WSL 跑：

```bash
# 一次性：~/u8src -> scummvm-src 的 symlink（路徑有空白，make 不能直接用）
#         ~/u8build 已 configure：--backend=null --disable-all-engines
#         --enable-engine=ultima,ultima8 --disable-freetype2 --disable-mt32emu --disable-detection-full
wsl -d Ubuntu -- bash "/mnt/d/git/Ultima 8 for ZH/tools/build/wsl_unit_tests.sh"
```

腳本內的三個繞道：`VER_REV=wsltest`（避免 `git describe` 掃描 Windows 檔案系統而卡住）、以 `python3` 執行 `cxxtestgen`（CRLF + `python` shebang）、`make -o test/runner.cpp`。
目前結果：**476 項全部 OK**。本專案新增的測試：`test/engines/ultima/ultima8/gfx/font_utf8.h`（P3）、`test/engines/ultima/ultima8/misc/translation_catalog.h`（P4）。

**MSVC 與 g++ 都要建置**：MSVC 把 C4701（可能未初始化）當錯誤，g++ 不會。
**單元測試只能用不依賴 `Kernel` 的物件檔**：否則靜態函式庫會連帶拉進整個引擎與 GUI，測試無法連結（所以 `TranslationCatalog` 獨立成檔）。

### 執行遊戲（`private_test/`）

| 啟動檔 | 版本 | 設定檔 |
|---|---|---|
| `launch-p0.bat [debug\|launcher]` | 原版 | `scummvm-p0.ini` |
| `launch-trace.bat [slot]` | Usecode trace | `scummvm-p0.ini` |
| `launch-spike.bat [slot]` | P2 spike（含中文翻譯 POC） | `scummvm-spike.ini`（`u8_l10n=zh_TW`） |
| `launch-dev.bat [slot]` | **開發分支**（`--debugflags=Localization`） | `scummvm-dev.ini`（`localization=zh_TW`、`font_cjk_file=Cubic_11.ttf`） |

- 每次執行都會產生帶時間戳的 log；全部使用獨立設定檔，不動使用者的全域 ScummVM 設定。
- `--extrapath=private_test\extra`：字型、`ultima8.dat` 複本、**編譯後的翻譯檔 `u8_zh_TW.mo`**、spike 用的 `u8_l10n_zh_TW.tsv`、`p3_test_strings.txt`。
- 更新翻譯檔：`python tools/catalog/po_compile.py zh_TW localization/zh_TW -o private_test/extra/u8_zh_TW.mo`
- Localization 設定（遊戲設定）：`localization=off|zh_TW`、`localization_file`（預設 `u8_<語言>.mo`）、`font_cjk_file`（預設 `Cubic_11.ttf`）、`font_cjk_size`（12）、`font_cjk_antialiasing`（false）。**CJK 字型只在 localization 啟用時載入**。
- log 中的 `[U8-L10N]` 訊息需要 `--debugflags=Localization`；主控台 `Localization::info` 顯示目前狀態。
- 存檔：`private_test/saves/ultima8.001`（`p1-after`，在 Devon 附近，已和 Devon 對話過）。
- 遊戲內字型測試：`Ctrl+Alt+D` → `Ultima8Engine::barkTestFile p3_test_strings.txt <n>`（需要 `localization=zh_TW` 才會載入 CJK 字型）。

### 自動操作遊戲視窗

`tools/automation/scummvm_window.ps1`（DPI aware）：

```powershell
scummvm_window.ps1 shot out.png        # 截圖 client 區域（1440x1080）
scummvm_window.ps1 click x y           # 單擊；dclick 為雙擊
scummvm_window.ps1 key "text"          # SendKeys，只適合輸入文字
scummvm_window.ps1 vk "13"             # 帶 scan code 的按鍵：Enter=13、Esc=27
scummvm_window.ps1 vk "17,18,68"       # Ctrl+Alt+D（開主控台）
```

SDL 只認帶 scan code 的特殊鍵（Enter、組合鍵），所以要用 `vk`。

---

## 5. 已知陷阱

1. **Bash heredoc 會破壞反斜線跳脫**：`\\x`、`\\n` 寫進 Python/C++ 原始碼時被轉換，曾造成 C++ 字串斷行與測試字串變成實際字元。需要反斜線時，改寫成 Python 檔案並用 `chr(92)` 產生，或用 Edit/Write 工具。
2. **`_UTF8` 是 Windows 系統標頭的巨集**：變數命名避開（已改為 `_utf8`）。
3. **原版英文文字含 CP437 字元**（4 句德文/法文，例如 `hei\xE1e`）：UTF-8 解碼遇到不合法序列時，以 CP437 逐 byte 解碼（已實作並有測試）。
4. **對話中無法存檔**：原版設計（`setAvatarInStasis`），不是 bug。
5. **`--save-slot=N` 讀不到存檔時**，會跳出「數據讀取失敗」對話框。
6. ScummVM 執行時會自動改寫 `--config` 指定的 ini（重新排序並加上欄位），屬正常現象。
7. Git 全域設定 `core.autocrlf=true`：主 repo 用 `.gitattributes`（`eol=lf`，`.bat` 為 crlf）。

---

## 6. 下一步：Phase 5（First NPC Bark Chinese POC）

### P4 已完成的部分（[報告](reports/P4-localization-manager.md)）

- `TranslationCatalog`（`misc/translation_catalog.*`）：讀 MO，key = `context + "\x04" + 英文原文`，結果 HIT / MISS / SOURCE-MISMATCH。
- `Localization`（`misc/localization.*`）：singleton，由 `Ultima8Engine` 建立；`applyGameSettings()` 呼叫 `configure()`，`GameData::setupFontOverrides()` 回報字型狀態。`isActive()` 為 true 才查表。
- 掛點：`Item::I_bark` 呼叫 `translateBark(str)`、`Item::I_ask` 對每個答案呼叫 `translateAnswer(class, text)`。**目前只查表寫 log，回傳值沒有使用**。
- **待確認**：遊戲內實際和 Devon 對話，看 log 中的 HIT / MISS（需要操作遊戲視窗，先問使用者）。

### P5 要做的事

規格見 Master Plan §24 與「v2：P5 工作項目」：

1. 把 `translateBark()` 的結果交給 BarkGump 顯示（spike 的做法：`BarkGump::_displayText`，不存檔；`_barked` 保持英文）。
2. 自言自語 bark 的 `TextWidget::_text` 會寫進存檔（§49 #2）：讀檔時要用 `_barked` 重建顯示文字，或改成不存譯文。**中文不得進入存檔**（STOP 條件）。
3. 顯示時間以 byte 計算，中文會停留過久（§49 #3）。
4. 掛點前確認目標字型是 UTF-8 字型（§49 #17）。
5. 之後：P6 AskGump（`InitGump` 與 `loadData` 兩處掛點）、P7 完整對話驗收。

### Master Plan §49 尚未完成的待辦

| # | 項目 | Phase |
|---|---|---|
| 2 | 自言自語 bark 的 `TextWidget::_text` 寫入存檔 | P5 |
| 3 | 顯示時間以 byte 計算 | P5 / P11 |
| 7 | 句型比對與參數翻譯 | P11 |
| 8–9 | 5 個無法自動解析的 bark、共用 class 的對話脈絡 | P10 |
| 10 | BookGump 的 `_TL_()` 書本修正與新翻譯層並存 | P8 |
| 11 | 建立 ScummVM fork 並改為 submodule | 待使用者決定 |
| 12 | HD 文字層 | P15 |
| 14 | 原版換行無限迴圈的修正可考慮回報 upstream | — |
| 15 | 遊戲選項 GUI 的語言選單 | P9 或之後 |
| 16 | 翻譯檔加入遊戲資料版本（`EUSECODE.FLX` 雜湊） | P10 |
| 17 | BarkGump / AskGump 掛點確認目標字型是 UTF-8 字型 | P5 / P6 |

---

## 7. 重要數據（快速參考）

| 項目 | 數值 |
|---|---|
| Usecode class | 515 |
| `push string` literal / 不重複文字 | 11,238 / 5,980 |
| bark 呼叫點 | 4,526（固定句子 4,408、句型 113、無法解析 5） |
| ask 選項（class + 英文） | 969 |
| 相同英文出現在多個呼叫點 | 382 句、1,038 個呼叫點 |
| Devon | class `0402`；開場 `0402:0633`「Hello there. 」；ask 呼叫點 `0402:08C2` |
| Orlok（佔位符號範例） | class `040A`；`{varF7}` = 玩家名字或 `"stranger "`；`{call_0BCF}` = 酒名 |
| Cubic 11 字數 | 10,268 |
| intrinsic | bark `0x49`、ask `0x4A`、getName `0xBC`、numToStr `0xB9`、setAvatarInStasis `0xD0` |
