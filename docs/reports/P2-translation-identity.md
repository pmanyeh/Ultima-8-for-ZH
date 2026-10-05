# Phase P2 Report — Translation Identity & Provenance

## Result

**PASS**：建議 **GO** 進入 Phase 3。

- 設計：[ADR-001 Translation Identity](../architecture/ADR-001-translation-identity.md)
- 格式：[ADR-002 Translation Catalog Format](../architecture/ADR-002-translation-catalog-format.md)

## Environment

- Repository: `scummvm-src/`，upstream `71cb05b1c03aa6bdcd34f78c20cef12c10067ba5`
- Branch: `exp/u8-p2-identity-spike`（**尚未 commit**）
- Build: `build-spike/`（Debug x64，VS 2026 / MSVC 14.51）
- Game data: GOG Ultima VIII Gold Edition, English（未修改）

## Scope Performed

1. 定義 bark、ask、動態句型的翻譯 ID（ADR-001）。
2. 實作最小 spike，以實機驗證 ID 穩定性，並且**依使用者要求提前驗證中文顯示的可行性**（嚴格說屬於 Phase 3–6 的範圍，見 Deviations）。
3. 依對話流程的抽取示範工具，以及全遊戲的普查。
4. 字型與解析度實驗。
5. 確定翻譯檔格式（ADR-002，使用者決策）。

## Spike 內容（`exp/u8-p2-identity-spike`）

所有改動都標註 `L10N SPIKE`，共約 220 行：

| 檔案 | 內容 |
|---|---|
| `usecode/uc_process.h` | 新增唯讀的 `getIp()` |
| `gfx/fonts/font.h` / `font.cpp` | `UTF8Traits`：UTF-8 解碼（不合法的序列 → U+FFFD）、中文標點禁則、中文逐字換行（`endsWord`）；`typesetText<UTF8Traits>` 實例化 |
| `gfx/fonts/tt_font.*` | UTF-8 模式；`toUnicode` 改為逐字附加（修正多 byte 文字造成的斷言失敗） |
| `gfx/fonts/font_manager.*` | `addTTFOverride(..., utf8)` |
| `misc/l10n_spike.*`（新增） | 讀取 TSV 翻譯表、bark/ask 查表、`[U8-L10N]` log、CJK 字型 override |
| `world/item.*` | `I_bark` 傳入顯示文字；`I_ask` 傳入呼叫的 class |
| `gumps/bark_gump.*` | `_displayText`（不寫入存檔）交給 TextWidget；`_barked` 不變 |
| `gumps/ask_gump.*` | 按鈕文字查表替換；`_answers` 與 `_processResult` 不變 |
| `games/game_data.cpp` | 呼叫 `L10nSpike::setupFonts()` |
| `engines/ultima/module.mk` | 加入 `l10n_spike.o` |

設定（遊戲設定檔）：`u8_l10n=zh_TW`、`u8_l10n_file`、`u8_l10n_font`、`u8_l10n_fontsize`。

## Evidence

### 實機測試（使用者遊玩，以及 Agent 截圖與自動點擊）

- Devon 的開場白 `0402:0633` → 「你好啊。」（HIT）。
- 選項「你是誰？」「再見。」等中文顯示正常，中英混排正常（`• Hello, Devon.  • 再見。`）。
- **點擊中文「再見。」→ 進入原始的 Goodbye 分支**，Devon 說出原本的道別台詞（`0402:338E`）。
- 長句分成多行、標點不出現在行首，中英混排換行正常（修正後由使用者確認）。
- 沒有翻譯的台詞與選項顯示英文（MISS），對話照常進行。
- 含玩家名字的句子（`0402:060F`、`0402:0964`）目前顯示英文，屬於預期行為（句型要到 Phase 11）。

### ID 驗證

詳見 ADR-001 §驗證。要點：多次執行的 ID 一致；**由反組譯工具離線算出的 ID，在遊戲中全部命中**。

### 全遊戲抽取普查（`tools/extract/u8extract.py`）

| 項目 | 數量 |
|---|---|
| bark 呼叫點 | 4,526 |
| 固定句子 | 4,408 |
| 自動還原的句型 | 113 |
| 無法自動解析 | 5（0.1%） |
| 對話選項（class + 英文） | 969 |

示範輸出：`private_test/extract-demo/`（Devon、Orlok），依對話流程排列，含佔位參數（`{name}`、`{varF7}` = `"stranger "` 或玩家名字、`{call_0BCF}` = 酒名）。

### 字型與解析度

| 方案 | 結果 |
|---|---|
| Noto Sans TC（向量字型，可變字重） | 預設字重太細，加上 1px 黑框後幾乎看不清楚 |
| Noto Sans TC Bold 11pt | 清楚，但放大後筆畫邊緣呈方塊狀（使用者評估：有改進空間） |
| 遊戲高解析度選項（640×400） | 地圖可見範圍變大、角色變小，改變了原版畫面 → 不採用 |
| **Cubic 11（俐方體 11 號，OFL）12px，關閉反鋸齒** | **筆畫銳利，與像素美術風格一致 → 使用者接受** |

**根本原因：** U8 以 320×200 繪製後再放大約 4.5 倍，一個中文字大約只有 12px。徹底的解法是讓文字以視窗解析度繪製（Phase 15「HD 對話」）。

## Files Changed

- `scummvm-src/`（實驗分支，未 commit）：見上表
- 新增 `docs/architecture/ADR-001-translation-identity.md`
- 新增 `docs/architecture/ADR-002-translation-catalog-format.md`
- 新增 `docs/reports/P2-translation-identity.md`
- 新增 `tools/extract/u8extract.py`
- 本機（不進版控）：`private_test/launch-spike.bat`、`scummvm-spike.ini`、`extra/`（字型、翻譯表、`ultima8.dat` 複本）、`extract-demo/`

## Deviations

1. **提前進行中文顯示 spike：** Master Plan §46 規定 P2 GO 之前不寫中文程式碼。使用者明確要求先確認「ScummVM 能否顯示中文」，因此在實驗分支做了最小 spike。spike 不會直接合併，Phase 3–6 需依計劃重新整理成正式實作。
2. **翻譯檔格式提前決定：** 原本屬於 Phase 10，提前為 ADR-002。

## Regressions

- 未做完整回歸測試。spike 改動了 `toUnicode`（所有 TTF 路徑共用）與 `findWordEnd`（新增 `endsWord`；舊有 Traits 永遠回傳 false）。理論上英文與日文的行為不變，但 Phase 3 必須以 unit test 證明。
- localization 關閉時（`u8_l10n` 不是 `zh_TW`），bark/ask 只多記一行 debug log，顯示文字與原版相同。

## Risks

1. CJK 字型載入失敗時尚未自動停用翻譯（ADR-001 D5，Phase 4 必要項目）。
2. 自言自語 bark 的顯示文字會寫進存檔（ADR-001 後果 4）。
3. 顯示時間按 byte 數計算，中文（3 bytes/字）會停留比較久（Phase 11）。
4. 像素字型的字數有限，需要「譯文用字 ⊂ 字型字集」的檢查工具（Phase 3/10）。
5. 全域的 `font_antialiasing` 會同時影響其他 TTF 字型。

## Recommendation

1. **GO**：進入 Phase 3（UTF-8 / CJK foundation），以 spike 為參考，重新寫成正式實作並加上 unit test。
2. 決定 spike 分支的處理方式：commit 保存（建議，作為參考），或丟棄。
3. Master Plan 需要更新的地方：§5、§7（ID 來源）、§9（`@`）、§20（新增的 Gump 種類）、§29（PO 已決定）、字型策略（像素字型）。

## Next Phase Readiness

**READY**：等待使用者審閱並明確指示。

## STOP

Work stopped after Phase 2 as required. Phase 3 was not started.
