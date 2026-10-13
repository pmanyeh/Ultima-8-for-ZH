# 主控台指令

ScummVM 內建一個「除錯主控台」，可以輸入指令：傳送、作弊、播放動畫與音樂、查看物件資訊等。本文整理 Ultima VIII 可用的指令。這些是給進階玩家的工具，一般遊玩不需要。

> **使用前請先存檔。** 傳送、修改劇情變數等指令可能讓遊戲卡關，存檔後再試比較安心。

## 基本用法

- 遊戲中按 **`Ctrl+Alt+D`** 開啟主控台（macOS 是 `Control+Option+D`），輸入指令後按 Enter。
- 按 **Esc** 或輸入 `exit` 關閉主控台。注意：**`quit` 會直接結束遊戲**，不是關閉主控台。
- `help` 列出所有指令名稱。輸入一部分再按 **Tab** 會自動補完（例如輸入 `Cheat` 再按 Tab）。
- 指令名稱要分大小寫，例如 `Cheat::heal`。
- 大部分指令執行後主控台會自動關閉，讓你看到畫面；只顯示資訊的指令會留在主控台。
- 數字可以寫十進位或十六進位，十六進位要加 `0x`，例如 `0x2AD`。
- 主控台不能顯示中文，中文會變成亂碼，這是 ScummVM 主控台本身的限制。

### 標記說明

| 標記 | 意思 |
|---|---|
| 🔓 | 需要先開啟作弊，否則會顯示 `Cheats are disabled` |
| ⌨️ | 有預設快捷鍵（可在 ScummVM 的「按鍵對應」（Keymaps）中更改） |

**開啟作弊**：在 ScummVM 選取遊戲 →「遊戲設定」（Game Options…）→「遊戲」分頁，勾選「開啟作弊」；或在主控台輸入 `Cheat::toggle on`。

---

## 一、作弊

| 指令 | 參數 | 用途 |
|---|---|---|
| `Cheat::toggle` | `[on\|off]` | 開關作弊（不帶參數 = 切換） |
| `Cheat::maxstats` 🔓 | — | 力量、敏捷、智力設為 25，體力與法力補滿 |
| `Cheat::heal` 🔓 | — | 體力與法力補滿 |
| `Cheat::toggleInvincibility` 🔓 | `[on\|off]` | 無敵 |
| `Cheat::items` 🔓 | — | 背包放入：黑曜石 500、地震頭骨、召回石、數把武器（含烈焰之刺、屠殺者）、降靈術材料一袋、神通術法器一袋、油瓶 3 個、盾牌 2 面、盔甲、死靈之碟 3 個 |
| `Cheat::equip` 🔓 | — | 現有裝備移進背包，換上欺詐者與一整套魔法護甲 |
| `Cheat::hackMover` | `[on\|off]` | 可以拖動任何物品，不受距離限制，平常拖不動的物品也可以 |
| `QuickAvatarMoverProcess::toggleClipping` 🔓 | `[on\|off]` | 穿牆 ⌨️ `Alt+Insert`。穿牆時可用 `Alt+Home` 上升、`Alt+End` 下降 |

前四項也可以用畫面左下角的作弊圖示（見 [SETTINGS.zh-TW.md](SETTINGS.zh-TW.md) 的「作弊圖示組」）。

---

## 二、傳送與位置標記

| 指令 | 參數 | 用途 |
|---|---|---|
| `MainActor::mark` | `<名稱>` | 把目前位置記成一個標記（名稱用英文或數字） |
| `MainActor::recall` 🔓 | `<名稱>` | 傳送回標記的位置 |
| `MainActor::listmarks` | — | 列出所有標記 |
| `MainActor::teleport` 🔓 | 見下 | 傳送到指定座標 |
| `CameraProcess::moveToAvatar` | — | 鏡頭移回聖者 |

標記存在設定檔裡，關掉遊戲再開也還在。例如：

```text
MainActor::mark shop
MainActor::recall shop
```

`MainActor::teleport` 的寫法（座標可以用 `ObjectManager::objectInfo` 查物件的位置得知）：

```text
MainActor::teleport <地圖> <x> <y> <z>   傳送到指定地圖的座標
MainActor::teleport <x> <y> <z>          傳送到目前地圖的座標
MainActor::teleport <地圖> <egg>         傳送到指定地圖的傳送點
MainActor::teleport <egg>                傳送到目前地圖的傳送點
```

---

## 三、遊戲流程、動畫與音樂

| 指令 | 參數 | 用途 |
|---|---|---|
| `Ultima8Engine::saveGame` | `[名稱]` | 有名稱：直接存到快速存檔欄位；沒有名稱：開啟存檔畫面。對話中無法存檔 |
| `Ultima8Engine::loadGame` | `[任意文字]` | 有參數：讀快速存檔；沒有參數：開啟讀檔畫面 |
| `Ultima8Engine::newGame` | — | 開始新遊戲 |
| `quit` | — | 直接結束遊戲（不詢問） |
| `QuitGump::verifyQuit` | — | 顯示「確定要離開嗎」 |
| `MenuGump::showMenu` | — | 開啟主選單 ⌨️ `Esc` |
| `MovieGump::play` | `<動畫名>` | 播放動畫。`MovieGump::play eintro`：片頭；`MovieGump::play endgame`：結局 |
| `MusicProcess::playMusic` | `<曲目編號>` | 播放指定曲目 |
| `AudioProcess::playSFX` | `<音效編號>` | 播放音效 |
| `AudioProcess::stopSFX` | `<音效編號> [物件編號]` | 停止音效 |
| `AudioProcess::listSFX` | — | 列出正在播放的音效與語音 |

> 主選單的「7.語錄」「8.結局」平常隱藏，看完製作人員名單或破關後才出現。想提前看，可在 `scummvm.ini` 的 `[ultima8]` 區段加上 `quotes=true`、`endgame=true`（請在 ScummVM 關閉時修改）。

---

## 四、聖者操作（都有快捷鍵）

| 指令 | 用途 | 快捷鍵 |
|---|---|---|
| `MainActor::useBackpack` | 打開背包 | ⌨️ `I` |
| `MainActor::useInventory` | 打開裝備與屬性畫面 | ⌨️ `Z` |
| `MainActor::useRecall` | 使用召回石 | ⌨️ `R` |
| `MainActor::useBedroll` | 使用睡袋 | ⌨️ `B` |
| `MainActor::useKeyring` | 使用鑰匙圈 | ⌨️ `K` |
| `MainActor::toggleCombat` | 拔出 / 收起武器（可加 `on\|off`） | ⌨️ `C` |
| `MainActor::name` | 顯示聖者的名字；加參數則改名，例如 `MainActor::name Avatar` | — |
| `Ultima8Engine::closeItemGumps` | 關閉所有物品視窗 | ⌨️ `Backspace` |
| `MiniMapGump::toggle` | 開關小地圖 | ⌨️ `M` |
| `GameMapGump::toggleHighlightItems` | 標示可互動的物品（可加 `on\|off`） | ⌨️ `H` |

---

## 五、中文化相關

| 指令 | 參數 | 用途 |
|---|---|---|
| `Localization::info` | — | 顯示中文化狀態：語言、翻譯檔、條目數、字型 |
| `Localization::gravestone` | — | 顯示死亡畫面的墓碑（聖者不會死） |
| `Localization::guardianBark` | `<1-23>` | 守護者的嘲諷（有語音） |
| `Localization::bark` | `<編號>` | 聖者說出翻譯檔中的某一句台詞 |
| `Localization::say` | `<編號> <英文>` | 以某一句台詞的位置說出任意英文，檢查會不會翻成中文 |
| `Localization::read` | `book\|scroll\|grave\|plaque <編號>` | 直接打開某一本書、捲軸、墓碑或牌匾 |

`<編號>` 是翻譯檔中每一句的位置編號，格式是 `XXXX:XXXX`，例如 `02AD:009E`。翻譯檔（`.po`）在本專案的 GitHub（見 [README.zh-TW.md](README.zh-TW.md)），每一句前面的 `msgctxt "bark 02AD:009E"` 就是它的編號。這幾個指令主要用來校對譯文。

---

## 六、畫面與地圖

| 指令 | 參數 | 用途 |
|---|---|---|
| `Ultima8Engine::togglePaintEditorItems` | `[on\|off]` | 顯示平常看不到的物件（觸發點、傳送點等） |
| `Ultima8Engine::toggleShowTouchingItems` | `[on\|off]` | 標示與聖者接觸的物品 |
| `GameMapGump::toggleFootpads` | `[on\|off]` | 顯示物品佔用的地面範圍 |
| `GameMapGump::gridlines` | `[on\|off\|<間距>]` | 顯示格線 |
| `GameMapGump::dumpMap` | `[地圖編號]` | 把整張地圖存成圖片（Windows 版存成 `map_NNN.png`，放在本包資料夾；macOS 版存成 `map_NNN.bmp`）。會先自動存檔，完成後讀回 |
| `GameMapGump::dumpAllMaps` | — | 所有地圖都存成圖片（需要很久） |
| `MiniMapGump::generate` | `[檔名]` | 重新產生小地圖；加檔名則同時存成圖片 |
| `MiniMapGump::clear` | — | 清除小地圖 |
| `FastAreaVisGump::toggle` | — | 右上角顯示目前載入的區域 |
| `ShapeViewerGump::U8ShapeViewer` | — | 圖形檢視器，可瀏覽遊戲所有圖片 |
| `InverterProcess::invertScreen` | — | 畫面上下翻轉（遊戲中的特效） |
| `Ultima8Engine::setVideoMode` | `<寬> <高>` | 改變遊戲解析度 |

---

## 七、進階：物件、程序與劇情變數

給熟悉遊戲內部的人使用。

| 指令 | 參數 | 用途 |
|---|---|---|
| `ObjectManager::objectInfo` | `<物件編號>` | 物件的詳細資訊（形狀、位置等） |
| `ObjectManager::objectTypes` | — | 各種物件的數量 |
| `Kernel::listProcesses` | `[物件編號]` | 列出執行中的程序 |
| `Kernel::processInfo` | `<程序編號>` | 單一程序的詳細資訊 |
| `Kernel::processTypes` | — | 各種程序的數量 |
| `Ultima8Engine::engineStats` | — | 引擎統計 |
| `Ultima8Engine::toggleAvatarInStasis` | `[on\|off]` | 凍結聖者，無法操作（對話時遊戲本身也會這樣做） |
| `UCMachine::getGlobal` | `<位置> <長度>` | 讀取劇情變數 |
| `UCMachine::setGlobal` | `<位置> <長度> <值>` | 修改劇情變數。**會改變劇情進度，請先存檔** |
| `UCMachine::traceClass`、`traceObjID`、`tracePID`、`traceAll`、`stopTrace` | | 追蹤遊戲腳本的執行，輸出到 log |

另有幾個 Crusader（同一個引擎的另一款遊戲）專用的指令，例如 `MainActor::useMedikit`，在 Ultima VIII 中沒有作用。

---

## 八、ScummVM 共用指令

| 指令 | 用途 |
|---|---|
| `help` | 列出所有指令 |
| `exit` | 關閉主控台 |
| `clear`、`cls` | 清除主控台畫面 |
| `exec <檔案>` | 依序執行文字檔中的指令 |
