# P20 戰鬥輔助：攻擊滑鼠所指的對象、傷害數字擴充、血條

**日期：** 2026-10-14
**結果：** ✅ PASS（使用者試玩：攻擊鎖定、聖者與敵人的傷害數字、血條都正常）
**引擎：** `ultima8-zh-tw-dev` @ `2138432ebc`、`bc801a8ae7`（本機，未 push）

使用者與朋友討論後提出四項：敵人血條（可開關）、聖者受傷也顯示數字、揮空與魔法 / 投擲物的傷害數字、攻擊時自動面向點到的對象。使用者決定：血條在**被打後顯示幾秒**；傷害數字顯示**畫面上所有人物**受傷；編號 P20（原本的「高解析介面放大」順延為 P21）。

## 攻擊滑鼠所指的對象（`attack_target`，預設開啟）

研究結果（`U8AvatarMoverProcess::handleCombatMode`）：
- 原版攻擊是戰鬥模式中**雙擊**左鍵（踢腿是雙擊右鍵）。方向由 `Mouse::getMouseDirectionWorld` 算出，是「畫面中央往下 14 像素 → 滑鼠」，只有 8 方向，**不是**「聖者 → 點到的人」。聖者不在畫面正中央時，斜方向的敵人常常差一格。
- 命中判定（`AnimationTracker::checkWeaponHit`）是在聖者面向的前方 `32 × attack_range` 放一個框，碰到誰就打誰；方向錯了就揮空。
- 沒有面向該方向時，原版的 `checkTurn` 只會**轉身就 return**，這次雙擊已被標成處理過，攻擊被吃掉。這就是「要等轉好方向後再點才有效」的原因。

修改（新增 `U8AvatarMoverProcess::attack`）：
- 雙擊時以 `TraceObjId` 找滑鼠下的人物（不是聖者、沒死），方向改為「聖者中心 → 目標中心」（`Direction_GetWorldDir`，8 方向）；指著空地仍用滑鼠方向。
- 先 `turnTowardDir`，攻擊動畫 `waitFor` 轉身，一次雙擊就轉身並出手。
- 移動中（鍵盤方向）攻擊不變。debug 1 log：`Attack target <id>: direction <d> (mouse <d>)`。
- 遠程：U8 的聖者沒有弓弩類武器（據目前所知）；法術本來就用選目標游標，不受方向影響。待使用者遊戲中確認。

## 傷害數字擴充（`damage_numbers`）

- `Actor::receiveHitU8`：原本只在攻擊者是聖者時顯示；改為**任何人物受傷**都顯示（近戰、魔法、陷阱、摔落、usecode 的 `receiveHit`），只要有實際傷害或攻擊者是人物（0 傷害 = 「格擋」）。不死 / 無敵的人物傷害視為 0。
  - 理由：魔法與投擲物的 `other` 常是 0、火球本身或 usecode 呼叫端，以「聖者造成」為條件會漏掉。
- **聖者受傷**：橘黃色（新字型 `CJK_DAMAGE_AVATAR_FONT` 71，設定類別 `damage_avatar`，`FFB020`）。
- **揮空**：`ActorAnimProcess` 動畫正常結束時，若是聖者、攻擊動畫（`AAF_ATTACK` 且有 `attack_range > 0` 的畫格）且整段沒打中任何東西，在聖者頭上顯示「揮空」（英文 Miss；灰色，`CJK_DAMAGE_MISS_FONT` 72，`damage_miss`，`C8C8C8`）。動畫被打斷（聖者被打中）時不顯示。
- 只在人物位於 fast area、不在容器內、不是 ethereal 時顯示（`DamageGump::isOnMap`），避免畫面外的人物把數字顯示在畫面底部。
- 數字起點上移 3 像素，讓出血條的位置。
- 投擲物：U8 丟出的物品撞到人物是否造成傷害，要遊戲中確認；有傷害就會走 `receiveHit` 而顯示。

## 血條（`health_bars`，預設開啟）

- `gumps/health_bar_gump.*`：`ItemRelativeGump`（不存檔），在被打的人頭上畫 24×4 遊戲像素的條：黑框、暗紅底，生命值 > 1/2 綠、> 1/4 黃、其餘紅。
- 被打中後顯示約 4 秒（144 幀）；再被打中重新計時（每個人物只有一條，`g_healthBars` 對照表）。人物死亡、離開 fast area 就關閉。聖者不顯示。
- 生命值即時讀取 `getHP()` / `getMaxHP()`，喝藥水等變化也會反映。

## 試玩中修正的兩個問題

1. **有傷害時數字與血條立刻消失**（「格擋」看得到）：人物受傷時 `receiveHitU8` 以 `killAllButCombatProcesses` / `killAllButFallAnims` 結束他身上的程序，連 gump 的 `GumpNotifyProcess`（owner = 該人物）也被結束，gump 隨即關閉。0 傷害不走這段，所以「格擋」可見。修正：兩個 gump 覆寫 `CreateNotifier()` 不建立通知程序，改在 `run()` 自行檢查人物是否還在。
2. **怪物沒有血條**：`Actor::getMaxHP()` 是 `2 × STR`，怪物的生命值來自 `MonsterInfo`（`_minHp`–`_maxHp` 隨機），STR 常為 0 → 滿血值 0 → 不畫。修正：有 `MonsterInfo` 的人物，以**第一次被打（扣血前）的生命值**為滿血值並記住（`g_fullHP`，死亡時清除）；其他人物用 `max(HP, getMaxHP())`。限制：被打前就受過傷的怪物，第一次的血條會是滿的。

除錯：新增主控台指令 `Localization::damage <objid> [damage]`（只顯示數字與血條，不扣血；-1 = 揮空）；debug 1 log `Damage: <n> over <id>`、`Health bar over <id>: <hp> of <full>`。

試玩 log：`Attack target 138: direction 4 (mouse 0)`、`142: direction 8 (mouse 12)`、`direction 6 (mouse 10)` —— 滑鼠方向與實際方向差 1–2 格的情形都已修正。揮空、魔法傷害未特別回報，之後遊玩時留意。

## 設定與文件

- `ultima8.cpp` `registerDefault`：`attack_target`、`health_bars`（`true`）。
- 中文設定頁【操作】：新增「攻擊滑鼠所指的對象」「顯示被攻擊者的血條」，「顯示聖者攻擊的傷害數字」改為「顯示傷害數字」（`tools/gui/make_zh_hant.py`，重新產生 `po/zh_Hant.po`，刪除兩條舊字串，WSL 重建 `translations.dat`）。
- `package/SETTINGS.zh-TW.md`（第十節表格與總表）、`package/CHANGELOG.md`（新的「下一版（未發布）」，也補上同 tick 迴圈保護）。

## 驗證

- MSVC Debug 建置成功（`build_dev.bat`，exe 含新程式）；g++（WSL `~/u8build`）編譯所有修改的檔案，無錯誤與警告。
- 單元測試 485 項 OK（本次沒有可單元測試的部分：gump 與 process 依賴 Kernel）。
- `startup_check.ps1`：啟動正常，沒有字型設定失敗的警告。
- **遊戲內行為待使用者試玩**（見下）。

## 試玩步驟

1. 關閉正在執行的遊戲，執行 `private_test\launch-dev.bat <存檔編號>`（或 `new`）。
2. 進入戰鬥模式（按 `C`），找敵人。
3. 確認：
   - 讓敵人在聖者斜前方或側面，滑鼠指著敵人雙擊左鍵：聖者應轉向敵人並立刻揮擊（不必再點一次）。雙擊右鍵踢腿也一樣。
   - 敵人被打中：紅色數字 + 頭上血條，約 4 秒後消失；連續打中時血條不消失；敵人死亡時血條消失。
   - 聖者被打中：聖者頭上橘黃色數字。
   - 對空地揮擊：聖者頭上灰色「揮空」。
   - 用攻擊法術打敵人：有數字與血條。
4. 中文設定頁【操作】關閉三個新選項後，行為回到原版 / 不顯示。
5. log（`private_test/dev-*.log`）有 `Attack target ...` 行，測完告訴我，我來讀 log 驗證方向。
