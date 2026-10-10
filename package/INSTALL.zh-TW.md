# 安裝說明

## 需要的東西

- Windows 10 / 11（64 位元）。
- 正版 **Ultima VIII: Pagan 英文版**的遊戲資料。GOG 的 *Ultima 8 Gold Edition* 可以直接使用；其他版本只要是英文版（含 Gold Edition 的 1.06 以後版本）通常也可以。
  - 法文版、德文版、日文版**不能**使用中文化（會照常以原本的語言執行）。

## 步驟

1. **解壓縮**：把整個壓縮檔解壓到一個資料夾，例如 `D:\Games\Ultima8-zhTW`。
   - 資料夾裡有 `scummvm.ini`，ScummVM 會以「可攜模式」執行：設定、存檔、截圖都放在這個資料夾裡（存檔在 `Saved games`），不會動到電腦上其他的 ScummVM。
2. **執行** `scummvm.exe`（或 `啟動 Ultima 8.bat`）。
3. **新增遊戲**：按「Add Game…」（新增遊戲），找到遊戲的英文資料夾後按「Choose」（選擇）。
   - GOG 版：`C:\GOG Games\Ultima 8\ENGLISH`（依你的安裝位置而定）。這個資料夾裡應該有 `U8.EXE`、`STATIC`、`USECODE` 等。
   - ScummVM 會辨識出「Ultima VIII: Pagan (Gold Edition/DOS/English)」，按「OK」。
4. **確認中文化已開啟**（預設就是開啟的）：選取遊戲 →「Game Options…」→「Game」分頁，確認勾選了「Traditional Chinese translation (繁體中文)」。
5. 按「Start」。片頭的守護者字幕應該是中文。

## 從原本的英文存檔繼續玩

存檔與英文版通用。若要沿用 GOG / DOSBox 原版的存檔，可以在 ScummVM 的遊戲畫面用原版的日記讀檔（「Game Options…」→「Game」→ 勾選 *Use original save/load screens*），或把原版存檔匯入 ScummVM。

## 疑難排解

| 狀況 | 處理 |
|---|---|
| 畫面上都是英文 | 確認「Traditional Chinese translation」已勾選；確認用的是**英文版**資料；確認 `extra` 資料夾裡有 `u8_zh_TW.mo` 和 `Cubic_11.ttf`。 |
| 中文顯示成方塊或亂碼 | 你換用的字型缺字，改回 `font_cjk_hd_file=jf-openhuninn-2.1.ttf`（高解析中文字關閉時則是 `font_cjk_file=Cubic_11.ttf`）。 |
| 找不到 `extra` 裡的檔案 | 請從資料夾裡直接執行 `scummvm.exe` 或用附的 `.bat` 啟動（不要從捷徑以其他「開始位置」執行）。 |
| 想看英文原文 | 取消勾選「Traditional Chinese translation」即可，存檔不受影響。 |

## 換字型、調整字級與台詞框

把字型檔（`.ttf` / `.otf`）放進 `extra` 資料夾，在 ScummVM 關閉時編輯 `scummvm.ini`：

```ini
font_cjk_hd_file=你的字型.ttf
```

字級、字距、行距、台詞框的行數與寬度等所有設定，見 [SETTINGS.zh-TW.md](SETTINGS.zh-TW.md)；`scummvm.ini` 裡每個設定也都有中文註解。

注意：Windows 內建的字型（例如細明體、微軟正黑體）**不能**隨本包散布，但你可以把自己電腦上的字型複製到 `extra` 自用。
