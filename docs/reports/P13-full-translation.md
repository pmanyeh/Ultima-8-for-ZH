# Phase P13 Report — Full Translation Campaign

## Result

**PASS**（全遊戲翻譯完成，99.8%；試玩中未發現漏翻。區域性的完整試玩驗收持續進行，見 Risks）

## Environment

- Repository: 主 repo `main`（`f0b7e11` → `75a631c`，22 個 commit，已 push 到 `origin/main`）
- Engine: `scummvm-src/` 分支 `ultima8-zh-tw-dev`（`1882ba7ba5` → `f9433ae9d2`，已 push 到使用者的 fork）
- Windows build: `build-dev/`（Debug x64，VS 2026 / MSVC）：成功
- Unit test: WSL Ubuntu，485 項全部通過
- Game data: GOG Ultima VIII Gold Edition, English（唯讀）
- 期間：2026-10-08（第一批）～2026-10-09（第二～八批、片頭字幕、字距設定）

## Scope Performed

| 批次 | 內容 | 條目 |
|---|---|---|
| 1 | 開場 → 碼頭處決 → 城門與城內衛兵（使用者錄影宣告用） | 1,003 |
| 2 | 泰尼伯瑞主要角色：班提克、歐洛克、珍娜、薩金德、達里恩、科里克、奇蘭卓、阿拉米娜 | 1,240 |
| 3 | 貝倫、米斯蘭、維維多斯 | 792 |
| 4 | 平民 / 小孩 / 乞丐、托溫、阿卡迪昂、白銀之岩（史泰洛斯、席勒斯、薩維爾）＋ 抽取工具補抓的 51 個選項 | 約 950 |
| 5 | 威廉與柯林斯、巫師聚落（貝恩、瓦爾迪恩、戈格隆德、馬爾奇爾、門徒）、四泰坦、派羅斯召喚、惡魔場景 | 約 1,300 |
| 6 | 物品名稱、作弊選單、地下墓穴的古代死靈法師、戴文的審判、其餘 300 個小 class | 約 1,100 |
| 7 | 墓碑、牌匾（字幕） | 128 |
| 8 | 全部的書與捲軸（約 12 萬英文字元） | 約 140 |
| — | 片頭動畫字幕（`EINTRO.SKF`，新增 `ui/movies.po`） | 5 |

結果（`u8catalog.py stats`）：7,000 條中 6,949 條已翻，以英文字元計 **99.8%**。刻意不翻的 51 條：作弊選單的亂碼密碼與座標資訊、數字選項（0–9）、`.`、名字缺漏的兩句（見 Findings）。

### 翻譯原則（沿用並擴充第一批）

- 專有名詞一律依權威檔（`authority.tsv`）；引擎自動加註英文。
- 角色口吻：歐洛克的海盜腔、薩金德居高臨下的「咱們」、城門衛兵的「俺」、巨魔的文雅書面語等。
- 聆聽真言法術顯示的括號「真心話」照原意譯出。
- 雙關改寫：「What's yer poison?」→「想來點什麼毒藥？」；murder/mother →「謀殺／模範」；Daemion / Daemient →「戴蒙／戴蒙癡」。
- 咒語（In Flam! 等）保留原文，驚嘆號改全形。
- 墓碑與牌匾是字幕，不必照雕刻的 `*` 換行。
- 同一句英文在不同語境刻意譯法不同的共 11 組（例如 yes / no 依前面的問題譯為「見過／覺得／好／是」），已逐一確認。

## Evidence

### 試玩 log（使用者操作，2026-10-08～10-09）

`private_test/dev-*.log` 的 HIT / MISS 紀錄，以目前的翻譯檔重新比對（`$TEMP/claude/misscheck.py`）：

- 所有曾經 MISS 的條目現在都有譯文，除了：
  - 床鋪「休息幾個時段」的選項 `0`–`5`（只顯示數字，不需翻譯）；
  - 2026-10-07 P11 測試用的 `Something else`（測試字串，非遊戲內容）。
- 10-09 晚上的試玩（片頭字幕、字距設定）：各 log 的 HIT 194～264 筆，MISS 0、SOURCE-MISMATCH 0。
- 使用者回饋：「文本文意順暢」；片頭字幕已顯示中文；換字型並調整字距後「效果很好」。

### 工具檢查

- `u8catalog.py check zh_TW --font Cubic_11.ttf`：0 errors；警告只剩英文原文誤打的 tab。字型缺字（「愫」「懨」）已改字。
- `po_compile.py`：6,949 entries（227 個句型）、657 個名稱（146 個加註）。
- `startup_check.ps1`：遊戲載入 6,949 條，localization active。

## Files Changed

### 主 repo

- `localization/zh_TW/dialog/*.po`：全部 class 的譯文
- `localization/zh_TW/ui/movies.po`（新）：片頭字幕
- `tools/extract/u8extract.py`：選項清單抽取修正（見 Findings）
- `tools/catalog/batch.py`：只差空格的條目以完整英文區分；墓碑 / 牌匾不檢查 `*`
- `tools/catalog/table.py`（新）：prefill / view / fill，用「英文 ||| 中文」對照表批次翻譯
- `docs/HANDOFF.md`、`README.md`、`README_EN.md`（進度）

### 引擎（`ultima8-zh-tw-dev`）

- `gfx/skf_player.cpp`：動畫字幕以 `Localization::uiText` 查表（`07ed69ba3a`）
- `gfx/fonts/tt_font.{h,cpp}`、`gfx/fonts/font_manager.{h,cpp}`、`games/game_data.cpp`、`misc/localization.h`：中文字型的字距設定（`f9433ae9d2`）
  - `font_cjk_letter_spacing`：所有字元之間
  - `font_cjk_latin_spacing`：中日韓文字與英文字母 / 數字之間
  - `font_cjk_line_spacing`：行距
  - 預設皆 0（版面與先前相同）；有設定時逐字繪製，字寬與 kerning 與 `Graphics::Font` 相同，換行、分頁、輸入游標都依新間距計算。

## Tests

| 測試 | 結果 |
|---|---|
| WSL 單元測試 | 485 / 485 OK |
| `u8catalog.py check` | 0 errors |
| `startup_check.ps1`（預設與加上間距設定各一次） | 載入 6,949 條，active |
| 使用者試玩 | 片頭、開場、泰尼伯瑞、字距設定：OK |

## Findings

### Observed

1. **選項清單只抽到最後一個答案**：Usecode 一次把多個答案放進清單（`0x0E` 的元素數 > 1）時，抽取工具只記錄最後一個字串。修正後補回 51 個選項（薩維爾的智慧考驗、五芒星陣與死靈法師之鑰的咒語、貝倫的惡魔之口等），沒有刪除任何既有條目。`site_variants()` 也沿分支列舉選項（貝恩的「Please forgive me」+「, kind lady.」/「, Bane.」）。
2. **動畫字幕不在 Usecode 裡**：片頭守護者的 5 句存在 `STATIC/EINTRO.SKF`，引擎播放時沒有查表。`ENDGAME.SKF` 沒有字幕。
3. **從清單隨機取名的句子仍是英文**：巫師門徒（0575 SORCERER）從清單（Cardas、Daemos…）取名存進 local，抽取工具沒有把它當參數，`My name is ○○. And you are?`、`○○, the late Sorcerer` 以及 058A 的 `He calls himself, ○○.` 會顯示英文。Cardas 等名字被當成選項抽出（無害）。
4. 字型 Cubic 11 缺少少數罕用字，`check --font` 能列出。

### Inferred

- 以對話流程（`batch.py dump` 的「after …」註解）翻譯，語境大多正確；只有極短的答案（yes / no）需要逐一看前面的問題。

### Unknown

- 長篇的書在 3 行 / 頁的台詞框以外（書本 UI）分頁是否都自然，尚未逐本試讀。
- 後期區域（白銀之岩之後）的對話尚未完整試玩。

## Regressions

無。字距設定預設 0，程式路徑與先前相同；英文模式不受影響。

## Risks

- **區域驗收**（Master Plan §32 要求每區域 acceptance）：目前完整試玩的是開場到泰尼伯瑞；其餘區域只有 log 抽查，建議在 P14 期間或發布前繼續試玩，以 log 的 MISS 補漏。
- Findings 3 的兩處英文句子。

## Blockers

無。

## Recommendation

1. 進入 P14（打包）。
2. 持續試玩其餘區域；修正 Findings 3（讓抽取工具把「從清單取值的 local」當參數）可排在 P14 期間。
3. 權威檔補入書中新出現的人名（見 HANDOFF §8），待使用者確認舊版中文手冊後一併調整。

## Next Phase Readiness

**READY**

## STOP

Work stopped after Phase P13 as required.（使用者已指示進入 P14）
