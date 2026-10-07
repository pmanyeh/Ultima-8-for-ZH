# Phase P12 Report — Save / Speech / Regression Hardening

## Result

**PASS**

## Environment

- Repository: `scummvm-src/`
- Branch: `ultima8-zh-tw-dev`（commit 見 HANDOFF；本機，未 push；接續 P11 的 `4ce1d3e434`）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC 14.51）：成功，0 warning
- Unit test: WSL Ubuntu（g++），483 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（唯讀）
- 自動化測試：2026-10-07 16:25–16:50（`save_matrix.ps1`、`regression_startup.ps1`，只開關自己啟動的 process）
- 遊戲內測試：使用者操作（2026-10-07 21:21–21:25，語音矩陣 4 種設定）

## Scope Performed

依 Master Plan §31。

| 項目 | 內容 |
|---|---|
| 存讀檔矩陣（自動） | `tools/automation/save_matrix.ps1`：把存檔複本放進獨立的存檔資料夾，以英文 / 中文模式讀檔，由 ScummVM 自動存檔（slot 0）後關閉；再把結果以另一種模式讀入並存檔。每階段的執行同時進行 |
| 存檔比較 | `tools/validate/save_compare.py`：解析存檔容器（`8UMV` + 11 個區段），逐區段比較；UCGLOBALS 不同的 byte、UCSTRINGS 的字串差異；以第二次英文執行為基準線（時間造成的差異）；只在**遊戲資料區段**檢查中文 |
| 啟動回歸（自動） | `tools/automation/regression_startup.ps1`：重建 P4 的 A–G 情境，加上 H（`font_override=false`）、I（英文設定檔） |
| 語音矩陣（使用者） | 新主控台指令 `Localization::guardianBark <1-23>`：執行主角的 `guardianBark` Usecode 事件（Guardian 的嘲諷，語音 `E666.FLX`）；`launch-dev.bat [slot] nosub|mute` 產生關字幕 / 關語音的設定 |
| 日文版程式路徑 | 檢查 P11 的計時改動：Shift-JIS 的 byte 序列可能剛好是合法 UTF-8，`readingLength()` 會誤算。**修正**：只有 UTF-8 字型（顯示譯文）才用 reading length，英文與日文維持原版的 byte 計算 |
| POC 譯文 | Guardian 嘲諷 3 句（`0401:3C96`、`3F7C`、`410E`）。翻譯檔合計 108 條 |
| 權威檔 | Pagan、Britannia、Guardian → proposed（暫保留英文，待舊版中文手冊）。Lord British 不在權威檔（候選詞收集漏列，§49 #26 整理時補上） |

## Evidence

### 存讀檔矩陣（`save_matrix.ps1` + `save_compare.py`）

來源存檔：slot 1（一般狀態）、slot 2（P5：主角說話中存檔，含 `BarkGump` / `TextWidget`）。

| 組合 | slot 1 | slot 2 |
|---|---|---|
| 英文存 → 英文讀（en1 / en2，基準線） | ✅ | ✅ |
| 英文存 → 中文讀（en1 → en_to_zh） | ✅ | ✅ |
| 中文存 → 中文讀（source → zh1） | ✅ | ✅ |
| 中文存 → 英文讀（zh1 → zh_to_en） | ✅（重跑，見下） | ✅ |

- 邏輯區段（GAME、WORLD、UCGLOBALS、UCSTRINGS、UCLISTS）：所有組合與英文基準線**完全相同**（0 byte 差異）；MAPS、CURRENTMAP 也相同。
- 時間相關區段（KERNEL 127 byte、OBJECTS / INFO / APP 各 1 byte）：中英文之間的差異與兩次英文執行之間的差異**相同**。
- 遊戲資料區段中沒有中文（全部存檔）。
- ScummVM 的中繼資料（存檔描述）會以 ScummVM 介面語言寫入，例如英文設定檔的自動存檔描述是「自动保存」。這不是遊戲文字，`save_compare.py` 另外列出、不算失敗（`save_text_check.py` 會把它算進去，以 `save_compare.py` 為準）。
- slot 1 的 zh_to_en 第一次執行時，遊戲在讀檔 15 秒後正常結束（log 為正常關閉，不是當掉），推測是視窗被手動關閉；以 `-Source` 重跑同一個中文存檔 → OK。

### 啟動回歸（`regression_startup.ps1`）

| 情境 | 結果 |
|---|---|
| A `localization=off` | ✅ 沒有任何 `[U8-L10N]` 訊息 |
| B `zh_TW` | ✅ 108 entries loaded，active |
| C 缺翻譯檔 | ✅ `not found, showing English text` |
| D 翻譯檔截斷 40 bytes | ✅ `string 107 is out of bounds`、`is invalid, showing English text` |
| E 檔頭 `ja_JP` | ✅ `is a ja_JP catalog, not zh_TW; showing English text` |
| F 缺 CJK 字型 | ✅ `Failed to open TTF`、`CJK font could not be loaded, localization disabled` |
| G 未設定 | ✅ 沒有任何 `[U8-L10N]` 訊息 |
| H `font_override=false` + zh_TW | ✅ 照常啟用（CJK 字型與 `font_override` 無關） |
| I 英文設定檔 | ✅ 沒有任何 `[U8-L10N]` 訊息 |

### 語音矩陣（使用者操作）

`Localization::guardianBark 3 / 12 / 16`（短句、中句、長句：中文 2 頁以上、語音多段）：

| 設定 | 結果 | log |
|---|---|---|
| 語音開 / 字幕開（`launch-dev.bat 1`） | ✅ 英文語音 + 中文字幕，頁面隨語音翻頁 | 3 句 HIT |
| 語音開 / 字幕關（`nosub`） | ✅ 只有語音，完整播完 | 3 句 HIT |
| 語音關 / 字幕開（`mute`） | ✅ 中文字幕以一般速度翻頁 | 3 句 HIT |
| 英文對照（`en`） | ✅ 原版行為 | 沒有 L10N 訊息 |

使用者評語：四種情境都很自然。

### 單元測試

483 項全部通過（P12 沒有新增測試：修正位於 `BarkGump`，依賴 Kernel / 字型，只能在遊戲中測）。

## Acceptance（Master Plan §31）

| 項目 | 結果 |
|---|---|
| save compatibility PASS | ✅ 4 種組合 × 2 個存檔，邏輯區段一致、沒有中文 |
| speech PASS | ✅ 3 種語音 / 字幕組合 + 英文對照 |
| English regression PASS | ✅ 情境 A / G / I；英文計時不變（非 UTF-8 字型維持 byte 計算） |
| Japanese code path regression PASS | ✅（程式檢查，沒有合法的日文資料）：localization 只在英文版啟用；計時對 Shift-JIS 維持原版；P3 的 SJIS 單元測試通過 |
| localization toggle PASS | ✅ 情境 A–I；存檔可在兩種模式間交換 |
| missing font fallback defined | ✅ 情境 F：還原原字型、停用翻譯、顯示英文（P4 定義） |

## Findings

### Observed

- 中文模式只改變顯示，不改變遊戲狀態：存檔的邏輯區段與英文模式逐 byte 相同。
- 語音以英文原句選擇與計時，中文字幕依各頁的 reading length 分配語音長度，翻頁與語音同步自然。
- upstream 既有行為：以啟動參數（`--save-slot`）讀檔時，ScummVM 會在讀檔前先嘗試自動存檔；那時新遊戲的初始化讓主角處於 stasis，嘗試失敗，下一次自動存檔延後 5 分鐘。不影響遊戲，只影響自動化測試的等待時間。
- U8 的語音只有 9 個角色（泰坦、雕像、Ironman、Guardian），其他 NPC 沒有語音。

### Inferred

- 使用者提出的「全語音 / 中文語音」：技術上語音以 shape 編號選檔、以英文片語比對（`SpeechFlex`），中文語音需要新的語音檔與片語表（以中文或 bark ID 比對），屬於 P15 的額外增強（§49 #29）。

## Files Changed

- `scummvm-src`：`misc/debugger.*`（`Localization::guardianBark`）、`gumps/bark_gump.cpp`（只有 UTF-8 字型用 reading length）
- 主 repo：`tools/automation/save_matrix.ps1`（新）、`tools/automation/regression_startup.ps1`（新）、`tools/validate/save_compare.py`（新）、`localization/zh_TW/dialog/0401_AVATAR.po`、`localization/zh_TW/authority.tsv`、`localization/README.md`、本報告、Master Plan v2.9、HANDOFF
- `private_test/launch-dev.bat`（不進 repo）：`nosub` / `mute`

## Regressions

- 無。P11 的計時改動對日文的潛在影響已在本 Phase 修正。

## Risks

- 自動化測試會在桌面上開啟遊戲視窗（每次約 5 分鐘）；執行前應先告知使用者。
- 日文版沒有實際資料測試，只能以程式路徑與單元測試確認。

## Blockers

無。

## Next Phase Readiness

Phase 13（Full Translation Campaign）的技術前提都已具備：抽取 / 合併 / 檢查 / 量測工具、存檔與語音安全、fallback。開始前需要：權威檔整理（§49 #26、#28，使用者正在找舊版中文手冊）、翻譯方式與順序的決定。

## STOP

等待使用者指示。
