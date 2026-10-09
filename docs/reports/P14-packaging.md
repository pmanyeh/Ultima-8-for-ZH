# Phase P14 Report — Packaging

## Result

**PASS**（2026-10-09 使用者以發佈版本實際測試：運作良好，中文顯示正常）

## Decisions（使用者，2026-10-09）

| 項目 | 決定 |
|---|---|
| 發布形式 | Windows 免安裝包：自建的 ScummVM Release + 翻譯檔 + 字型 + 說明文件，可攜模式 |
| 授權 | 全專案 GPL-3.0-or-later（譯文、權威檔、工具；引擎沿用 ScummVM 的 GPL-3.0） |
| 開啟方式 | ScummVM 遊戲選項的勾選框，預設開啟 |

## Environment

- Engine: `scummvm-src/` 分支 `ultima8-zh-tw-dev`：`d90d7a8c19`（勾選框）、`cd9bc7ec90`（預設開啟）
- Windows build: `build-dev/Releasex64`（Release x64，新增 `tools/build/build_release.bat`）、`build-dev/Debugx64`：成功
- Unit test: WSL Ubuntu，485 項全部通過
- VC 執行階段：`Microsoft.VC145.CRT`（VS 2026 Redist 14.51.36231）

## Scope Performed

1. **遊戲選項勾選框**：`Traditional Chinese translation (繁體中文)`（`localization_zh_tw`）、`Show the English after names (名稱加註英文)`（`localization_annotate`），兩者預設開啟。優先順序：勾選框 → 舊的 `localization` 鍵 → 預設 zh_TW。非英文版遊戲在未明確要求時不顯示警告、維持原語言。
2. **玩家文件**（`package/`，正體中文）：`README.zh-TW.md`、`INSTALL.zh-TW.md`、`TRANSLATION_CREDITS.md`、`LICENSES.md`、`CHANGELOG.md`。按鈕名稱附英文（ScummVM 的 `zh_Hant.po` 是空的，`zh.po` 雖標「Trad」但內容為簡體，故不預設介面語言）。
3. **授權**：根目錄新增 `LICENSE`（GPL-3.0 全文），README 中英文版更新。
4. **打包腳本** `tools/package/make_package.ps1`：產生 `dist/Ultima8-zhTW-<版本>/` 與 zip（`dist/` 已加入 .gitignore）。
   - `scummvm.exe` + 16 個相依 DLL + VC 執行階段 DLL
   - `extra/`：當場由 PO 編譯的 `u8_zh_TW.mo`、`Cubic_11.ttf`、`Cubic_11-OFL.txt`
   - `scummvm.ini`（可攜模式；`[scummvm]` 區段：`extrapath=extra`、Cubic 11、字距 1 / 中英間距 3 / 行距 0）
   - `啟動 Ultima 8.bat`（先切到套件資料夾，確保相對路徑 `extra` 有效）
   - 文件、`COPYING.txt`、`COPYRIGHT-ScummVM.txt`、`AUTHORS-ScummVM.txt`、`LICENSES/`
   - `CHANGELOG.md` 自動填入兩個 repo 的 commit
   - `-Test`：複製到 `private_test/package_test`，把 dev 設定的遊戲區段（去掉字型 / 語言 / 路徑設定）加進 `scummvm.ini`，以真正的可攜模式啟動一次、讀 log。

## Verification

| 項目 | 結果 |
|---|---|
| 單元測試（WSL） | 485 / 485 |
| 啟動回歸（`regression_startup.ps1`，新增 J 勾選框關、K 勾選框開） | 11 種情境皆符合預期；G（未設定）現在為啟用 |
| 套件測試（可攜模式，只帶 `--logfile` 與遊戲 ID） | 載入 6,949 條、`localization zh_TW active`、遊戲初始化完成 |
| 使用者驗收（發佈版本解壓、新增遊戲、試玩） | 運作良好，中文顯示正常 |
| 套件大小 | 資料夾約 110 MB（`scummvm.exe` 98 MB，內嵌 ScummVM 資源）；zip 82 MB |

## Findings

- **可攜模式存檔資料夾**是 exe 旁的 `Saved games`（ScummVM 自動建立）。
- 字型與字距設定放 `[scummvm]` 區段即可：`ConfMan.hasKey/get` 依序查遊戲區段、全域區段，玩家若在遊戲區段另外設定會覆蓋。
- **使用者自用的 `chinese.ttf`（細明體 MingLiU，DynaComware / Microsoft）不能散布**，套件只附 Cubic 11（OFL 1.1）。文件說明玩家可自行換字型。
- `scummvm.exe` 很大是因為 Release build 內嵌 `fonts-cjk.dat`、SoundFont、主題等；不影響使用，暫不精簡。

## Risks / Open Items

- 尚未在**沒有安裝 VC 執行階段**的乾淨 Windows 上測試（已附 DLL，理論上可行）。
- 尚未測試含中文字元的解壓路徑。
- 抽取工具「清單取名」缺口（巫師門徒自我介紹兩句）列在已知問題。
- 發布管道（GitHub Releases 等）由使用者決定；push / 上傳只在使用者要求時進行。
