# Phase P17 Report — Walk to Use（自動走近使用）

## Result

**PASS**（2026-10-10 使用者試玩：「運作良好」）

## 目標

U8 雙擊物品（門、箱子、書、拉桿…）時有距離限制，太遠只會閃叉叉游標；而遊戲的移動操作不方便。改為：距離不夠時，聖者自動走到物品旁邊再使用。

## 使用者的決定（2026-10-10）

| 項目 | 決定 |
|---|---|
| 範圍 | 先只做「雙擊使用」（從遠處拖曳物品之後再說） |
| 走路方式 | 用走的（沿用 ScummVM 的尋路） |
| 走不到時 | 主角搖頭 |
| 開關 | 遊戲選項勾選框「Walk to use (自動走近使用)」，預設開啟 |

## Environment

- Engine: `scummvm-src/` 分支 `ultima8-zh-tw-dev`：`51f9d26759`（自動走近使用）、`5c882724ab`（可觸及的尋路目標）

## 內容

- 距離判斷在引擎的 `GameMapGump::onMouseDouble`（`canReach(item, 128)`），不在 Usecode。距離不夠時改為啟動 `PathfinderProcess` 走向物品；`GameMapGump::run` 每幀檢查：尋路結束後再判斷一次，碰得到就 `item->use()`，碰不到就 `shakeHead`。
- 取消：玩家自己移動（`AvatarMoverProcess::MOVE_ANY_DIRECTION`）、戰鬥、對話（stasis）、物品消失，或再雙擊別的東西。
- 不變：雙擊 NPC（本來就沒有距離限制）、戰鬥中與劇情凍結中、容器視窗內的物品。
- **存檔相容**：不新增 process 類別。存檔裡只有原版也有的 `PathfinderProcess`；「走到後要使用的物品」只記在記憶體。途中存讀檔，主角會走完但不會自動使用。
- 設定 `walk_to_use`（預設 true）。

## 發現：尋路「走向物品」的判斷

第一版在門前永遠搖頭。加記錄後發現尋路在 45～112 ms 內就失敗（不是超時）。`PathfindingState::checkItem` 以主角座標框的**最遠角**與物品比較距離（≤ 32），沒有扣掉主角本身的寬度：從某些側（例如門的正面）接近時，主角不能與物品重疊，這個距離至少等於主角寬度，永遠不成立。原始碼也註明「these ranges are probably a bit too high」。

修正方式：不改原本的判斷（NPC 劇情的尋路也用它），新增 `Pathfinder::setReachTarget(item, range)`，以兩個框之間的實際間隙判斷（≤ 16），只有自動走近使用使用；`PathfinderProcess` 多一個 `reachRange` 參數（預設 0 = 原行為），不寫進存檔。

## Verification

| 項目 | 結果 |
|---|---|
| 建置（MSVC Debug） | 成功 |
| 啟動回歸 | 11 / 11 |
| 遠處雙擊門、箱子等，走不到時搖頭，途中移動取消 | 使用者試玩通過（雙擊遠處物品無法自動化測試） |
