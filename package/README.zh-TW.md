# 創世紀 VIII：佩根（Ultima VIII: Pagan）繁體中文版

這是 Ultima VIII: Pagan 的繁體中文化。遊戲本身不做任何修改：使用你自己的**英文版**遊戲資料，由本包附的 ScummVM（加入中文化功能的版本）在畫面上顯示中文。

- 對話、選項、物品名稱、書與捲軸、墓碑與牌匾、片頭字幕都已中文化（約 7,000 條，99.8%）。
- 人名、地名等專有名詞第一次出現時會附上英文，例如「戴文(Devon)」，方便對照原文與攻略。
- 存檔與英文版完全相容：可以隨時切換中英文，存檔不受影響。
- 語音維持原版英文。

**本包不含遊戲資料。** 你需要擁有正版的 Ultima VIII（例如 GOG 的 *Ultima 8 Gold Edition*）。

## 快速開始

1. 把壓縮檔解壓到任一資料夾（路徑可以有中文或空格）。
2. 執行 `啟動 Ultima 8.bat`（或直接執行 `scummvm.exe`）。
3. 按「Add Game…」（新增遊戲），選擇遊戲的**英文版資料夾**（GOG 版是安裝資料夾裡的 `ENGLISH`，裡面有 `U8.EXE` 和 `STATIC` 資料夾）。
4. 選好遊戲後按「Start」（開始）。

詳細步驟與疑難排解見 [INSTALL.zh-TW.md](INSTALL.zh-TW.md)。

## 設定

在 ScummVM 選取遊戲，按「Game Options…」（遊戲選項）→「Game」分頁：

| 選項 | 說明 |
|---|---|
| Traditional Chinese translation (繁體中文) | 中文化開關（預設開啟）。取消勾選就是原版英文。 |
| Show the English after names (名稱加註英文) | 專有名詞第一次出現時附上英文（預設開啟）。 |
| Quick action icons (快捷圖示列) | 滑鼠移到畫面右下角時出現的快捷圖示：背包、屬性、戰鬥、地圖、選單、鑰匙圈、召回石、睡袋、存檔、讀檔（預設開啟）。在 `scummvm.ini` 加上 `quick_bar_autohide=false` 可讓它常駐顯示。 |
| High-resolution Chinese text (高解析中文字) | 中文字以視窗解析度繪製（字型 jf open 粉圓），畫面其他部分不變（預設開啟）。重新啟動遊戲後生效。 |

字型、字級、字距、行距、台詞框的行數與寬度、快捷圖示列是否常駐等細部調整，寫在本資料夾的 `scummvm.ini`（每個設定都有中文註解）。完整說明與調整範例見 [SETTINGS.zh-TW.md](SETTINGS.zh-TW.md)。

## 已知問題

- 巫師聚落的一般門徒自我介紹時，含名字的兩句仍是英文。
- 作弊選單、座標資訊等除錯用文字維持英文。

ScummVM 本身的選單（新增遊戲、設定等）目前沒有完整的繁體中文翻譯，本包維持英文介面；說明文件裡的按鈕名稱都附上英文。

## 原始碼與授權

本中文化以 GPL-3.0 授權。引擎原始碼：<https://github.com/pmanyeh/scummvm>（分支 `ultima8-zh-tw-dev`），翻譯檔與工具：<https://github.com/pmanyeh/Ultima-8-for-ZH>。詳見 [LICENSES.md](LICENSES.md) 與 [TRANSLATION_CREDITS.md](TRANSLATION_CREDITS.md)。

本專案與 ScummVM 官方、Electronic Arts 無關。Ultima 是 Electronic Arts 的商標。
