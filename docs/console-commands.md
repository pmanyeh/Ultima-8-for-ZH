# 主控台指令對照表

ScummVM Ultima 8 引擎的除錯主控台指令，依 `scummvm-src/engines/ultima/ultima8/misc/debugger.cpp`（開發分支 `ultima8-zh-tw-dev`）整理，共 85 個。官方沒有逐條說明，以下的用途與參數都是依程式碼確認的。

## 基本用法

- 遊戲中按 **`Ctrl+Alt+D`** 開啟主控台，輸入指令後按 Enter。**Esc** 或輸入 `exit` 關閉。注意：**`quit` 會直接結束遊戲**（Ultima 8 引擎把它改成離開遊戲），不是關閉主控台。
- `help` 列出所有指令名稱。輸入指令名稱時可按 **Tab** 自動補完（例如輸入 `Loc` 再按 Tab）。
- 大部分指令執行後主控台會自動關閉，讓您看到畫面；只顯示資訊的指令（例如 `Localization::info`）會留在主控台。
- 數字參數可以寫十進位或十六進位：十六進位要加 `0x`，例如 `UCMachine::traceClass 0x2AD`。
- 參數有空白時用雙引號包起來，例如 `Localization::say 040A:1F16 "Hello "`。
- 主控台輸出中文會變亂碼（字型不支援），這是 ScummVM 主控台本身的限制。

### 標記說明

| 標記 | 意思 |
|---|---|
| 🀄 | 本專案新增的指令（原版 ScummVM 沒有） |
| 🔓 | 需要先開作弊模式，否則會顯示 `Cheats are disabled` |
| ⌨️ | 有預設快捷鍵（可在 ScummVM 的「按鍵對應」中更改） |
| ⚔️ | Crusader（《Crusader: No Remorse / No Regret》）專用，在 Ultima 8 中無作用或沒有意義 |

**開啟作弊模式**：ini 的 `[ultima8]` 加 `cheat=true`（`private_test/scummvm-dev.ini` 已經有），或在主控台輸入 `Cheat::toggle on`。

---

## 1. 中文化測試 🀄

| 指令 | 參數 | 用途 |
|---|---|---|
| `Localization::info` | — | 顯示翻譯狀態：語言、翻譯檔、條目數、字型 |
| `Localization::bark` | `<class>:<ip>` | 主角說出翻譯檔中該呼叫點的台詞（中文顯示，存檔仍是英文）。例：`Localization::bark 02AD:009E` |
| `Localization::say` | `<class>:<ip> <英文>` | 主角以該呼叫點說出任意英文，用來測句型與參數是否套得上。主控台會回報 `Translated` 或 `No translation, English is shown` |
| `Localization::read` | `book\|scroll\|grave\|plaque <class>:<ip>` | 直接打開書、捲軸、墓碑、牌匾，不必走到物品旁 |
| `Localization::gravestone` | — | 只顯示死亡畫面的墓碑（主角不會死） |
| `Localization::damage` | `<物件編號> [傷害]` | 在人物頭上顯示傷害數字與血條，不扣血（0 = 格擋、-1 = 揮空；1 = 聖者）（P20） |
| `Localization::guardianBark` | `<1-23>` | 守護者的嘲諷（有語音），測語音與字幕 |
| `Ultima8Engine::barkTestFile` | `<檔案> [行號]` | 主角說出文字檔中的第 n 行（預設第 1 行，`#` 開頭的行略過），測字型繪製。例：`Ultima8Engine::barkTestFile p3_test_strings.txt 3` |

`<class>:<ip>` 就是 PO 檔 `msgctxt` 裡的編號，例如 `msgctxt "bark 02AD:009E"` → `02AD:009E`。

---

## 2. 遊戲流程與存讀檔

| 指令 | 參數 | 用途 |
|---|---|---|
| `Ultima8Engine::saveGame` | `[名稱]` | 有名稱：直接存到快速存檔欄位（1）；沒有名稱：開啟存檔畫面。對話中無法存檔 |
| `Ultima8Engine::loadGame` | `[任意文字]` | 有參數：讀快速存檔欄位（1）；沒有參數：開啟讀檔畫面 |
| `Ultima8Engine::newGame` | — | 開始新遊戲 |
| `quit`、`Ultima8Engine::quit` | — | 直接結束遊戲（不詢問） |
| `QuitGump::verifyQuit` | — | 顯示「確定要離開嗎」對話框 |
| `MenuGump::showMenu` | — | 開啟主選單（同 Esc ⌨️） |
| `MovieGump::play` | `<動畫名>` | 播放 `STATIC/<名稱>.SKF`。例：`MovieGump::play endgame`（結局）、`MovieGump::play eintro`（片頭） |
| `MusicProcess::playMusic` | `<曲目編號>` | 播放指定曲目 |

> 主選單的「7.語錄」「8.結局」平常隱藏，破關後才出現。要提前看，在 ini 的 `[ultima8]` 加 `quotes=true`、`endgame=true`（遊戲關閉時修改）。

---

## 3. 作弊

| 指令 | 參數 | 用途 |
|---|---|---|
| `Cheat::toggle` | `[on\|off]` | 開關作弊模式（不帶參數 = 切換） |
| `Cheat::maxstats` 🔓 | — | 力量、敏捷、智力設為 25，生命與法力補滿 |
| `Cheat::heal` 🔓 | — | 生命與法力補滿 |
| `Cheat::toggleInvincibility` 🔓 | `[on\|off]` | 無敵 |
| `Cheat::items` 🔓 | — | 背包放入：黑曜石 500、地震頭骨、召回石、數把武器（含烈焰之刺、屠殺者）、死靈術材料一袋、神術法器一袋、油瓶 3 個、盾牌 2 面、盔甲、死靈之碟 3 個 |
| `Cheat::equip` 🔓 | — | 現有裝備移進背包，換上欺詐者與一整套魔法護甲 |
| `Cheat::hackMover` | `[on\|off]` | 可以拖動任何物品，不受距離與「能否拖動」限制 |
| `QuickAvatarMoverProcess::toggle` | `[on\|off]` | 開關快速移動模式 |
| `QuickAvatarMoverProcess::toggleClipping` 🔓 | `[on\|off]` | 穿牆（⌨️ `Alt+Insert`）。搭配 `Alt+Home` 上升、`Alt+End` 下降 |

---

## 4. 傳送與位置標記

| 指令 | 參數 | 用途 |
|---|---|---|
| `MainActor::teleport` 🔓 | 見下 | 傳送主角 |
| `MainActor::mark` | `<名稱>` | 把目前位置記成一個標記（存進 ini 的 `mark_<名稱>`） |
| `MainActor::recall` 🔓 | `<名稱>` | 傳送回標記的位置 |
| `MainActor::listmarks` | — | 列出所有標記 |
| `CameraProcess::moveToAvatar` | — | 鏡頭移回主角 |

`MainActor::teleport` 的四種寫法：

```text
MainActor::teleport <地圖> <x> <y> <z>   傳送到指定地圖的座標
MainActor::teleport <x> <y> <z>          傳送到目前地圖的座標
MainActor::teleport <地圖> <egg>         傳送到指定地圖的傳送點（target egg）
MainActor::teleport <egg>                傳送到目前地圖的傳送點
```

> 小技巧：在想測試的地點用 `MainActor::mark 名稱` 記下來，之後用 `MainActor::recall 名稱` 隨時回去，比存檔方便。

---

## 5. 主角操作（多半有快捷鍵）

| 指令 | 用途 | 快捷鍵 |
|---|---|---|
| `MainActor::useBackpack` | 打開背包 | ⌨️ `I` |
| `MainActor::useInventory` | 打開裝備與能力值畫面 | ⌨️ `Z` |
| `MainActor::useRecall` | 使用召回石 | ⌨️ `R` |
| `MainActor::useBedroll` | 使用睡袋 | ⌨️ `B` |
| `MainActor::useKeyring` | 使用鑰匙圈 | ⌨️ `K` |
| `MainActor::toggleCombat` | 拔出 / 收起武器（可加 `on\|off`） | ⌨️ `C` |
| `MainActor::name` | 顯示主角名字；加參數則改名，例：`MainActor::name Avatar` | — |
| `Ultima8Engine::closeItemGumps` | 關閉所有物品視窗 | ⌨️ `Backspace` |
| `MiniMapGump::toggle` | 開關小地圖 | ⌨️ `M` |
| `MiniMapGump::generate` | 重新產生小地圖；加檔名則同時存成圖片 | — |
| `MiniMapGump::clear` | 清除小地圖 | — |
| `GameMapGump::toggleHighlightItems` | 標示可互動的物品（可加 `on\|off`） | ⌨️ `H` |

⚔️ Crusader 專用：`MainActor::nextWeapon`、`nextInvItem`、`useInventoryItem`、`useMedikit`、`useEnergyCube`、`detonateBomb`、`dropWeapon`，以及 `ItemSelectionProcess::startSelection`、`useSelectedItem`、`grabItems`。

---

## 6. 畫面與地圖除錯

| 指令 | 參數 | 用途 |
|---|---|---|
| `Ultima8Engine::setVideoMode` | `<寬> <高>` | 改變遊戲解析度 |
| `Ultima8Engine::toggleAvatarInStasis` | `[on\|off]` | 凍結主角（無法操作；對話時遊戲本身也會這樣做）⌨️ `F10` |
| `Ultima8Engine::togglePaintEditorItems` | `[on\|off]` | 顯示平常看不到的編輯用物件（觸發點、egg 等）⌨️ `F9` |
| `Ultima8Engine::toggleShowTouchingItems` | `[on\|off]` | 標示與主角接觸的物品 ⌨️ `Ctrl+H` |
| `GameMapGump::toggleFootpads` | `[on\|off]` | 顯示物品的底面範圍 |
| `GameMapGump::gridlines` | `[on\|off\|<間距>]` | 顯示格線 |
| `GameMapGump::incrementSortOrder`、`decrementSortOrder` | `[數量]` | 調整繪製順序的除錯顯示 ⌨️ `]`、`[` |
| `GameMapGump::dumpMap` | `[地圖編號]` | 把整張地圖存成 PNG（`map_NNN.png`）。會先自動存檔、完成後讀回 |
| `GameMapGump::dumpAllMaps` | — | 所有地圖都存成 PNG（很久） |
| `FastAreaVisGump::toggle` | — | 右上角顯示目前載入的區域 |
| `InverterProcess::invertScreen` | — | 畫面上下翻轉（遊戲中的特效） |
| `ShapeViewerGump::U8ShapeViewer` | — | 圖形檢視器，可瀏覽遊戲所有圖片 ⌨️ `F11` |
| `RenderSurface::benchmark` | `<shape> <frame> <次數>` | 繪圖效能測試 |

---

## 7. 程序、物件與 Usecode（進階）

| 指令 | 參數 | 用途 |
|---|---|---|
| `Ultima8Engine::engineStats` | — | 程序、物件、Usecode、世界的統計 |
| `Kernel::listProcesses` | `[物件編號]` | 列出所有執行中的程序（或某物件的程序） |
| `Kernel::processInfo` | `<程序編號>` | 單一程序的詳細資訊 |
| `Kernel::processTypes` | — | 各種程序的數量 |
| `Kernel::toggleFrameByFrame` | `[on\|off]` | 逐格模式（暫停遊戲）⌨️ `F12` |
| `Kernel::advanceFrame` | — | 逐格模式下前進一格 ⌨️ `F` |
| `ObjectManager::objectInfo` | `<物件編號>` | 單一物件的詳細資訊 |
| `ObjectManager::objectTypes` | — | 各種物件的數量 |
| `UCMachine::getGlobal` | `<offset> <size>` | 讀 Usecode 全域變數（劇情旗標） |
| `UCMachine::setGlobal` | `<offset> <size> <值>` | 改 Usecode 全域變數。**會改變劇情進度，請先存檔** |
| `UCMachine::traceClass` | `<class>` | 追蹤某個 class 的 Usecode 執行（輸出到 log）。class 是十六進位時要加 `0x` |
| `UCMachine::traceObjID` | `<物件編號>` | 追蹤某物件的 Usecode |
| `UCMachine::tracePID` | `<程序編號>` | 追蹤某程序的 Usecode |
| `UCMachine::traceAll` | — | 追蹤全部 Usecode（log 會非常大） |
| `UCMachine::stopTrace` | — | 停止追蹤 |
| `AudioProcess::listSFX` | — | 列出正在播放的音效與語音 |
| `AudioProcess::playSFX` | `<音效編號>` | 播放音效 |
| `AudioProcess::stopSFX` | `<音效編號> [物件編號]` | 停止音效 |

> 只有用 `DEBUG_PATHFINDER` 編譯時才有 `Pathfinder::visualDebug <物件編號>`（顯示尋路過程，`-1` 停止），平常的建置沒有這個指令。

---

## 8. ScummVM 共用指令（所有引擎都有）

不算在上面的 85 個裡，由 ScummVM 本身提供（`gui/debugger.cpp`）。

| 指令 | 用途 |
|---|---|
| `help` | 列出所有指令 |
| `exit` | 關閉主控台 |
| `clear`、`cls` | 清除主控台畫面 |
| `exec <檔案>` | 依序執行文字檔中的指令（可把常用的測試步驟寫成檔案） |
| `debugflag_list` | 列出除錯分類，例如本專案的 `Localization` |
| `debugflag_enable <分類>`、`debugflag_disable <分類>` | 開關某個分類的 log（`launch-dev.bat` 已用 `--debugflags=Localization` 開啟） |
| `debuglevel [數字]` | 顯示或設定 log 詳細程度 |
| `openlog` | 開啟 log 檔 |

---

## 附錄：沒有對應指令的快捷鍵

| 按鍵 | 用途 |
|---|---|
| `F1` | 快速存檔 |
| `F5` / `F7` | 存檔 / 讀檔畫面 |
| `Space` | 跳躍 |
| `Left Shift` | 跑步 |
| `Left Ctrl` | 小心走一步 |
