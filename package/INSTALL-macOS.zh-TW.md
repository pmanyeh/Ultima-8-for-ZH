# macOS 安裝說明

本包含有加入中文化功能的 ScummVM（`ScummVM.app`），翻譯檔與字型都已放在 app 裡，不需要另外安裝任何東西。

- 下載的檔名結尾 `arm64` 是 Apple Silicon（M 系列晶片）用，`x86_64` 是 Intel Mac 用。
- **本包不含遊戲資料。** 你需要擁有正版的 Ultima VIII 英文版資料（例如 GOG 的 *Ultima 8 Gold Edition*）。

## 第一次開啟

這個 app 沒有經過 Apple 公證，第一次開啟時 macOS 會擋下來：

1. 在 Finder 裡對 `ScummVM.app` 按右鍵（或按住 Control 點一下），選「打開」，再按一次「打開」。
2. 如果仍然打不開：到「系統設定」→「隱私權與安全性」，在最下面按「強制打開」（Open Anyway）。
3. 也可以在「終端機」執行（把路徑換成你放 app 的位置）：

   ```sh
   xattr -dr com.apple.quarantine /Applications/ScummVM.app
   ```

之後就可以直接點兩下開啟。

## 加入遊戲

1. 開啟 ScummVM，按「Add Game…」（新增遊戲）。
2. 選擇遊戲的**英文版資料夾**（裡面有 `STATIC`、`USECODE` 等資料夾）。
3. 選好遊戲後按「Start」（開始）。

遊戲選項（Game Options… → Game）裡的中文化、高解析中文字、快捷圖示列等開關，和 Windows 版相同，預設都已開啟，說明見 [SETTINGS.zh-TW.md](SETTINGS.zh-TW.md)。

## 進階設定檔的位置

`SETTINGS.zh-TW.md` 說的 `scummvm.ini`，在 macOS 上是：

```
~/Library/Preferences/ScummVM Preferences
```

（在 Finder 按 Shift+Command+G，輸入 `~/Library/Preferences/` 就能找到。）請在 ScummVM 關閉時，用「文字編輯」修改，設定寫在 `[scummvm]` 或 `[ultima8]` 區段，和 Windows 版的寫法相同。macOS 版沒有附帶註解的設定檔，未寫出的設定都使用預設值。

換字型時，把字型檔放進 `ScummVM.app/Contents/Resources/`（在 app 上按右鍵 →「顯示套件內容」），再設定字型檔名即可。
