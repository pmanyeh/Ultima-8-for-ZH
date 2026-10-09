# Phase P15 Report — HD Text Layer（高解析文字層）

## Result

**實作完成，待使用者試玩**（2026-10-09）。**預設開啟**（使用者 2026-10-10 決定）；取消勾選時與 P14 完全相同。

## Environment

- Engine: `scummvm-src/` 分支 `ultima8-zh-tw-dev`：`bd1abf27e8`
- 測試：Windows 11、OpenGL、視窗 1440×1080、`aspect_ratio` 開啟（高解析畫面 1440×1080）

## 目標

Master Plan §34 / §48：U8 以 320×200 繪製，中文字只有約 12 px，再被放大 4–5 倍。P15 讓中文字以**視窗解析度**繪製，可以使用一般的向量字型（Noto Sans TC 等），同時**不改變原版畫面**（地圖範圍、角色大小不變；P2 已確認 640×400 模式會改變畫面，不採用）。

## 做法

Pentagram 原本有 `ScalerGump`（遊戲畫在低解析、文字以螢幕解析度合成），ScummVM 移除了 ScalerGump，但合成的骨架（`Gump::PaintCompositing` / `PaintComposited`、`Font::isHighRes`、`TextWidget` 的 high-res 分支）都還在。P15 把縮放層接回來：

```text
遊戲（世界、gump、像素字型）→ 320×200 的 _screen（與原本完全相同）
        │ 最近鄰放大（每幀，Debug 版 2–5 ms）
        ▼
_hdScreen（視窗解析度，例如 1440×1080）
        │ PaintCompositing：高解析字型的 TextWidget、片頭字幕
        ▼
ScummVM 輸出（1:1，不再由 backend 縮放）
```

| 部分 | 內容 |
|---|---|
| 畫面大小 | 預設為「符合目前視窗、維持遊戲畫面比例」的最大尺寸（`aspect_ratio` 開啟時 4:3，否則 16:10）；可用 `hd_text_size=寬x高` 指定。小於遊戲解析度 2 倍時不啟用 |
| 座標 | 遊戲邏輯全部維持 320×200：滑鼠座標在輸入端換算回遊戲座標；游標圖同比例放大 |
| 字型 | `FontManager` 另存一組 high-res override（`_hdOverrides`），只有 `TextWidget` 與片頭字幕使用；其他地方（製作人員名單、狀態欄、日記輸入框等）仍用原本的 12 px 字型，畫在遊戲層 |
| `TextWidget` | 字型量測以視窗像素、widget 尺寸與存檔欄位以遊戲像素（`textToGameX/Y`、`textTargetWidth/Height`）。**存檔內容不變**（`_targetWidth/_targetHeight` 仍存遊戲像素） |
| 片頭字幕 | `SKFPlayer::paintComposited`，由 `MovieGump::PaintComposited` 呼叫 |
| 屬性頁標籤 | P9 因 9 px 列距放不下中文而維持英文；高解析層下改用 8 遊戲像素的小字（`FontManager::HD_SMALL_CJK_FONT`）畫「力量／智力／敏捷／護甲／生命／魔力／負重」（`ui/engine.po`），數字維持原本字型。未開高解析時仍是英文 |
| 圖層（遮擋） | 高解析文字在整個遊戲畫完後才畫。有高解析文字的 gump 在遊戲層畫完自己時記下該區域的畫面（`saveHDOcclusion`）；畫完文字後，比對出被後來的 gump 改掉的像素，從遊戲畫面蓋回去（`restoreHDOcclusion`）。所以背包、選單等視窗能正確蓋住文字，部分重疊時露出的部分照常顯示。最初版本只在 modal 視窗下隱藏文字，使用者發現屬性頁的標籤浮在背包上，改為此做法 |
| 合成順序 | 修正 Pentagram 原本由上往下的走訪順序，改為與繪製相同的順序（自己先、子 gump 後） |

## 設定（game domain）

| 鍵 | 預設 | 說明 |
|---|---|---|
| `hd_text` | `true` | 高解析中文字（遊戲選項勾選框「High-resolution Chinese text（高解析中文字）」）；啟動遊戲時生效 |
| `hd_text_size` | （自動） | 高解析畫面大小，例如 `1920x1440` |
| `font_cjk_hd_file` | `jf-openhuninn-2.1.ttf` | 高解析用的字型檔（使用者選定 jf open 粉圓，打包附上） |
| `font_cjk_hd_size` | 同 `font_cjk_size` | 字級 |
| `font_cjk_hd_antialiasing` | `true` | 反鋸齒 |
| `font_cjk_hd_border` | 原本黑框的一半 | 黑框粗細 |
| `font_cjk_hd_letter_spacing` / `_latin_spacing` / `_line_spacing` | 同一般設定 | 間距 |

`font_cjk_hd_*` 的數值以**遊戲像素**為單位（可以有小數，例如 `0.3`），所以與視窗大小無關；引擎依縮放比例換算成視窗像素。

## Verification

| 項目 | 結果 |
|---|---|
| 建置（MSVC Debug x64） | 成功，無警告 |
| 單元測試（WSL） | 485 / 485 |
| 啟動回歸（`regression_startup.ps1`，9 情境，`hd_text` 未設定） | 與 P14 相同 |
| 片頭動畫字幕 | 高解析顯示（Noto Sans TC） |
| 名字輸入（書本） | 「請報上你的名字：」高解析；輸入框維持原本字型 |
| 戴文第一次見面 | 台詞（多行、名稱加註「戴文(Devon)」、玩家名字）與選項皆高解析；點選選項正確進入分支 |
| 主選單（存檔 1 讀檔後按 Esc） | 中文按鈕與玩家名字高解析 |
| 屬性頁上開背包（z 然後 i） | 背包蓋住標籤，露出的數字正常 |
| 屬性頁（存檔 1，按 z） | 中文標籤高解析；中文字會低於英文字母的基線，標籤上移 1 遊戲像素後與數字對齊（使用者指出） |
| 效能（Debug 版，1440×1080） | 遊戲層 1.7–2.5 ms、高解析層 2–5 ms／幀 |

測試方式：自動化腳本啟動遊戲，以 PostMessage 對該視窗送按鍵 / 點擊（不搶焦點），用 ScummVM 的截圖熱鍵（Alt+S）存出實際輸出畫面（`PrintWindow` 對 OpenGL 視窗會拿到過時畫面，不可用）。

## 字型比較（同一句戴文台詞，1440×1080）

| 字型 | 檔案大小 | 授權 | 觀察 |
|---|---|---|---|
| Noto Sans TC Medium | 5.4 MB | OFL | 清楚、粗細適中；一行字數與原本相同 |
| Noto Sans TC Bold | 5.6 MB | OFL | 最醒目，但字寬較大，同一句多換一行（多一頁） |
| jf open 粉圓 2.1 | 4.7 MB | OFL | 圓體、較柔和，筆畫稍細 |
| 細明體（`chinese.ttf`） | 26 MB | 不可散布 | 明體筆畫細，黑框下仍可讀；只能玩家自行設定 |
| Cubic 11（像素字型放大 4.5 倍） | 2.6 MB | OFL | 非整數倍放大 + 反鋸齒，邊緣模糊不均，不建議用於高解析 |

## 尚待使用者確認

1. ~~預設附哪個高解析字型~~：**jf open 粉圓**（使用者 2026-10-09 選定；打包附字型與 OFL 授權檔）。打包版**預設開啟**（2026-10-10）。
2. 試玩：書、捲軸、墓碑 / 牌匾字幕、日記、死亡畫面、選項的滑鼠移過變色、多個 NPC 同時說話、世界翻轉（Inverter）時的台詞位置、全螢幕。

## Known Limitations

- 視窗大小在遊戲中改變時，高解析畫面維持啟動時的大小，由 ScummVM 縮放（重新啟動遊戲即可重新配合）。
- 製作人員名單、日記輸入框、`[fontoverride]` 以外的字型維持原本解析度。
