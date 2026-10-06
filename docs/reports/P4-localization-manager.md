# Phase P4 Report — Localization Manager

## Result

**PASS**（遊戲內實際對話查表一項待確認，見 Evidence「遊戲內對話」）

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`
- Commit: `b0efb70a44`（本機，未 push；接續 P3 的 `96bfc46318`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test build: WSL Ubuntu（g++），`make test`（`tools/build/wsl_unit_tests.sh`）
- Game data: GOG Ultima VIII Gold Edition, English（未修改）

## Scope Performed

依 Master Plan §23 與「v2：P4 工作項目」，在開發分支實作正式的 localization layer。spike（`l10n_spike.*`）只作參考，重新設計。**本 Phase 只做查表，不改變任何顯示**；把譯文交給 BarkGump / AskGump 是 P5 / P6 的範圍。

| 項目 | 內容 |
|---|---|
| `TranslationCatalog`（`misc/translation_catalog.*`） | 讀取編譯後的翻譯檔，建立 hash map。只依賴 `common/`，可單獨做單元測試 |
| `Localization`（`misc/localization.*`） | 讀設定、載入 catalog、管理啟用狀態；`translate(context, source)`、`translateBark()`、`translateAnswer()` |
| ID 取得 | `UCProcess::getIp()`（唯讀）；`Item::I_bark` 用 running process 的 `classId:ip`，`Item::I_ask` 用 running process 的 class（ADR-001） |
| 掛點 | `I_bark`、`I_ask` 只在啟用時查表並寫 log，**不改 `str`、answer list、BarkGump、AskGump** |
| 字型 | CJK 字型只在 localization 啟用時載入；任何一個字型載入失敗 → 還原原本的字型並停用翻譯 |
| Debug channel | 新增 `Localization`（`--debugflags=Localization`），log 前綴 `[U8-L10N]` |
| 除錯指令 | `Localization::info`：顯示語言、翻譯檔、條目數、字型狀態 |
| 編譯工具 | `tools/catalog/po_compile.py`：PO → MO，含格式檢查 |
| POC 翻譯 | `localization/zh_TW/dialog/0402_DEVON.po`：Devon 第一段對話 17 條（P2 已有的譯文，無新增翻譯） |
| 單元測試 | `test/engines/ultima/ultima8/misc/translation_catalog.h`（10 項） |
| 啟動檢查工具 | `tools/automation/startup_check.ps1`：用指定設定檔啟動、等遊戲初始化完成、關閉，列出 log |

## 設計決定

### 1. 設定名稱

```ini
localization=zh_TW            ; off（預設）或語言代碼
localization_file=            ; 選填，預設 u8_<語言>.mo
font_cjk_file=Cubic_11.ttf    ; 選填，預設 Cubic_11.ttf
font_cjk_size=12              ; 選填，預設 12
font_cjk_antialiasing=false   ; 選填，預設 false
```

- 放在遊戲設定（game domain），與 `font_override` 等既有選項同一層。
- spike 的 `u8_l10n*` 改名。`font_cjk_*` 沿用 P3 的名稱。
- 遊戲選項 GUI 尚未加入：ScummVM 的 game option 只支援勾選框，語言選單需要自訂 widget。列為待辦（§49 新增 #15）。

### 2. 只在 localization 啟用時載入 CJK 字型（§49 #13）

P3 只要設定 `font_cjk_file` 就會換字型。P4 改為：**只有 localization 啟用、翻譯檔載入成功時才換字型**。因此 `localization=off` 時，字型與文字都和原版完全相同。這是驗收「OFF → exact original text path」的必要條件。

### 3. 翻譯檔格式：gettext MO（ADR-002 補充）

ADR-002 決定「執行時讀單一編譯檔」，但沒有決定格式。採用 **gettext MO**：

- 是 PO 的標準編譯格式，`msgfmt`、Poedit 都能產生，Python 的 `gettext` 模組可以直接讀取驗證。
- key 為 `msgctxt + "\x04" + msgid`，與 gettext 處理 context 的方式相同。
- 引擎端只需要約 100 行的讀取程式，不需要 PO parser。
- 所有 offset 與長度都先檢查範圍，結構有任何錯誤就整個檔案不使用。

查表 key 是「context + 英文原文」，所以：

| 情況 | 結果 |
|---|---|
| context 與英文都相符 | HIT，回傳譯文 |
| context 存在，但英文不同 | SOURCE-MISMATCH，顯示英文（log 記錄） |
| context 不存在 | MISS，顯示英文 |

同一個 bark 呼叫點可以有多個英文版本（ADR-001 風險 2 的對策），各自有譯文。

### 4. 啟用條件

以下全部成立才會啟用，否則一律顯示英文：

1. `localization` 不是 `off`
2. 英文版 Ultima VIII（日文、德文、法文、西班牙文版與 Crusader 都不啟用）
3. 翻譯檔存在、結構正確，且檔頭 `Language` 與設定相符
4. CJK 字型成功套用到 `[fontoverride]` 中的**每一個**字型

設定在遊戲中變更時（ScummVM 選單），會重新判斷；語言改變時先還原原本的字型再重新設定。

## Evidence

### 單元測試

```text
Running cxxtest tests (476 tests)....OK!
```

466 → 476，新增 10 項全部通過，原有測試全部通過：

| 測試 | 內容 |
|---|---|
| `test_context_format` | `bark 0402:0633`、`ask 0402` 的格式 |
| `test_canonical_context` | 大小寫不同的 hex 會被正規化；格式錯誤（缺 IP、超過 4 位、非 hex、`param`、空字串）會被拒絕 |
| `test_utf8_validation` | 合法 UTF-8、ASCII 通過；CP437 文字、截斷序列不通過 |
| `test_hit` | bark 與 ask 查表成功；檔頭 Language 讀取 |
| `test_miss_and_mismatch` | 未知呼叫點、未知 class → MISS；英文不同、大小寫不同、少了結尾空白 → SOURCE-MISMATCH |
| `test_several_sources_per_bark` | 同一個呼叫點有兩個英文版本，各自 HIT |
| `test_lowercase_hex_in_file` | 檔案中的小寫 hex 也能查到 |
| `test_malformed_entries_skipped` | 無 context、未知種類、錯誤 hex、未翻譯、空英文、非 UTF-8 譯文、複數形式、重複條目 → 共 8 條略過，其餘照常使用；重複時保留第一條 |
| `test_big_endian_file` | big-endian 的 MO 也能讀 |
| `test_corrupt_files_rejected` | 非 MO 檔、太短、截斷、條目數過大、offset 超出範圍 → 整個檔案不使用；之後再載入正確檔案仍正常 |

### 編譯工具

```text
private_test/extra/u8_zh_TW.mo: 17 entries from 1 files, 2016 bytes (skipped: 0 untranslated, 0 fuzzy, 0 obsolete)
```

- 以 Python 標準函式庫 `gettext.GNUTranslations.pgettext()` 讀回：`("bark 0402:0633", "Hello there. ")` → 「你好啊。」；少了結尾空白的 `"Who are you?"` 查不到。
- 錯誤檔測試：檔頭語言不符、缺 `msgctxt`、`bark 0402`（缺 IP）、跨行重複、複數條目 → 全部列出並中止，不產生輸出檔。
- 略過檔測試：fuzzy、未翻譯、`#~` 過時條目被略過；多行字串與 `\"`、`\n` 跳脫正確；`zh-TW` 視為 `zh_TW`。
- 同一個 PO 指定兩次 → 17 條全部報告重複。

### 遊戲啟動（Windows build，`startup_check.ps1`）

7 種設定，各自啟動到 `-- Game Initialized --` 後關閉：

| 情境 | 設定 | log | 結果 |
|---|---|---|---|
| A. OFF | `localization=off` | 沒有任何 `[U8-L10N]` 訊息 | ✅ 原版路徑 |
| G. 未設定 | 沒有 `localization` | 沒有任何 `[U8-L10N]` 訊息（`font_cjk_file` 有設定，但不載入） | ✅ 原版路徑 |
| B. zh_TW | `localization=zh_TW` | `17 entries loaded, 0 skipped, language "zh_TW"`、`localization zh_TW active` | ✅ 啟用 |
| C. 缺翻譯檔 | `localization_file=p4test_missing.mo` | `translation catalog ... not found, showing English text` | ✅ 英文 |
| D. 翻譯檔損壞 | 截斷 40 bytes | `string 16 is out of bounds`、`... is invalid, showing English text` | ✅ 英文 |
| E. 語言不符 | 檔頭 `Language: ja_JP` | `is a ja_JP catalog, not zh_TW; showing English text` | ✅ 英文 |
| F. 缺字型 | `font_cjk_file=p4test_missing.ttf` | `Failed to open TTF`、`CJK font could not be loaded, localization disabled` | ✅ 英文、原字型 |

### 遊戲內對話（待確認）

`I_bark` / `I_ask` 的 ID 取得與查表，需要實際和 Devon 對話才能在 log 中看到 HIT / MISS。這需要操作遊戲視窗，依合作規則先向使用者確認，**尚未執行**。

- 已有的證據：ID 取得的方式（`classId` + calli 的 IP、ask 的 class）與 P2 spike 相同，spike 在遊戲中已多次 HIT（`0402:0633`、`0402:1B1D`、`ask 0402 "Goodbye. "` 等）；查表本身由單元測試覆蓋。
- 預期 log（`launch-dev.bat 1`，和 Devon 對話）：

```text
[U8-L10N] ask 0402 HIT src="Goodbye. "
[U8-L10N] bark 0402:060F MISS src="Hello there, <玩家名字>."   ← 動態句子，P11
```

## Acceptance（Master Plan §23）

| 項目 | 結果 | 證據 |
|---|---|---|
| localization OFF → exact original text path | ✅ | 情境 A / G：不載入翻譯檔、不換字型、不查表（`isActive()` 為 false 時 `I_bark` / `I_ask` 不做任何事） |
| zh_TW → translated test lookup | ✅（遊戲內對話待確認） | 單元測試 `test_hit`；情境 B 載入 17 條 |
| unknown ID → original English | ✅ | `test_miss_and_mismatch`；`translate()` 在 MISS / SOURCE-MISMATCH 回傳原文 |
| malformed entry → safe fallback | ✅ | `test_malformed_entries_skipped`、`test_corrupt_files_rejected`；情境 C / D / E |
| no Usecode changes | ✅ | 只加了唯讀的 `UCProcess::getIp()`；UCMachine 未修改 |
| no string heap replacement | ✅ | `I_bark` 的 `str`、`I_ask` 的 answer list 都不變；譯文目前不使用 |
| CJK 字型缺失 → 顯示英文，不出現亂碼（v2） | ✅ | 情境 F：還原原字型、停用翻譯 |

## Findings

### Observed

1. **MSVC 把 C4701（可能未初始化的變數）當作錯誤**，g++ 不會。WSL 編譯通過不代表 Windows 編譯會過，兩邊都要建置。
2. **Ultima 引擎的靜態函式庫連結有連鎖效應**：單元測試只要用到依賴 `Kernel` 的物件檔，就會連帶需要整個引擎與 GUI，測試無法連結。因此把不依賴引擎的 `TranslationCatalog` 獨立成檔案。
3. `applyGameSettings()` 在啟動與每次變更選項時都會呼叫 `setupFontOverrides()`。原本只在 `font_override` / `font_antialiasing` 改變時重設字型；現在 localization 語言改變時也會重設，否則關閉翻譯後 CJK 字型會殘留。

### Inferred

- P3 的「設定 `font_cjk_file` 就換字型」行為已改變：現在必須同時設定 `localization`。P3 的 `barkTestFile` 測試需要 `localization=zh_TW`（`scummvm-dev.ini` 已更新）。

### Unknown

- 遊戲內 `I_bark` / `I_ask` 的實際 log（見上）。
- 日文版、Crusader：程式碼層級不會啟用（語言與遊戲類型檢查），沒有實機資料。

## Files Changed

- `scummvm-src`（`ultima8-zh-tw-dev`，commit `b0efb70a44`）：17 個檔案，+1002 / −13
  - 新增 `misc/translation_catalog.{h,cpp}`、`misc/localization.{h,cpp}`、`test/.../misc/translation_catalog.h`
  - 修改 `ultima8.{h,cpp}`、`games/game_data.{h,cpp}`、`gfx/fonts/font_manager.h`（`removeOverride`）、`usecode/uc_process.h`（`getIp`）、`world/item.cpp`（`I_bark`、`I_ask`）、`misc/debugger.{h,cpp}`、`ultima/ultima.h` 與 `detection.cpp`（debug channel）、`module.mk`
- 主 repo：`tools/catalog/po_compile.py`、`tools/automation/startup_check.ps1`、`localization/zh_TW/dialog/0402_DEVON.po`、本報告、ADR-002 補充、Master Plan 與 HANDOFF 更新
- 本機：`private_test/launch-dev.bat`（`--debugflags=Localization`）、`scummvm-dev.ini`（`localization=zh_TW`）、`extra/u8_zh_TW.mo`

## Regressions

- 全部 476 項單元測試通過（含 P3 的字型測試）。
- `localization` 未設定或 `off`：只多了一次設定讀取與字串比較；字型、文字、Usecode 路徑與原版相同。
- 日文：`setupJPOverrides` 未修改；localization 對非英文版不啟用。

## Risks

1. 翻譯檔沒有記錄對應的遊戲資料版本。若用在不同版本的英文 Usecode，IP 可能不同；英文比對（SOURCE-MISMATCH）可以防止顯示錯誤的譯文，但會變成大量 MISS。P10 可考慮在檔頭加入 `EUSECODE.FLX` 的雜湊。
2. 字型是否就緒是全域判斷（所有 `[fontoverride]` 字型都換成功）。若某個 gump 使用不在 `[fontoverride]` 中的字型，譯文仍會畫成亂碼。P5 / P6 的掛點應再檢查目標字型是否為 UTF-8 字型。

## Blockers

無。

## Next Phase Readiness

**READY**：Phase 5（First NPC Bark Chinese POC）。建議先完成上面「遊戲內對話」的確認。等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 4 as required. Phase 5 was not started.
