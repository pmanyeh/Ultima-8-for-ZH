# P19 遊玩輔助：輔助跳躍、傷害數字、藥水命名

**日期：** 2026-10-13
**結果：** ✅ PASS（使用者試玩：「遊戲體驗好不只 10 倍」「效果很棒」「有看到不同名稱了」）
**引擎：** `ultima8-zh-tw-dev` @ `31870b3ae0`（輔助跳躍）、`b5c29c98cf`（傷害數字）、`b5281180bb`（依畫格的 bark 條目）

## 輔助跳躍（`assisted_jump`，預設開啟）

使用者在第一個「跳跳樂」（水中踏腳石）一直失敗：跳上去後又滑進水裡。

研究結果：
- 原有的「跳向滑鼠位置」（`targetedjump`）把**聖者的座標基準點**（腳底範圍的一角）對準滑鼠點，身體偏半個身位，常落在石頭邊緣而滑下去。
- 踏腳石（usecode `020F SINKING`）在 `enterFastArea` 啟動循環：等待、分 15 步下沉、等待、浮起，是原版的機關。

修改（`U8AvatarMoverProcess::jump` 的 targeted 分支）：
- 落點以聖者腳底**中心**對準滑鼠點，並限制在目標上方（小目標則整個腳底在上面）。
- 以 `CurrentMap::getPositionInfo` 檢查落點；被擋住時沿「往聖者方向」退後或左右偏移，找最近的可站位置（解決點內陸時被岩石、植物擋住而搖頭的問題）；找不到或太遠才搖頭。
- 判斷寫在 debug 1 的 log（`Assisted jump: ...`）。
- 踏腳石下沉不改（關卡設計），說明文件提醒玩家。

## 傷害數字（`damage_numbers`，預設開啟）

原版只有聖者被打中時才噴血（`Actor::receiveHitU8`），敵人被打中幾乎沒有表示。
- `gumps/damage_gump.*`：聖者近戰打中時，在被打的人頭上浮出「-N」約一秒（不存檔）；傷害為 0 時顯示「格擋」（英文 Blocked）。
- 字型：新增 `FontManager::CJK_DAMAGE_FONT`（70），設定類別 `damage`（紅色 `FF4040`、黑框、12 像素），可用 `font_cjk_damage_*` 調整。
- 血條（方案 D）使用者決定先不做；揮空與魔法傷害未顯示。

## 藥水依效果命名

原版各色藥水都叫 potion。usecode `02FE POTION` 的 use 事件依畫格（顏色）決定效果：0 空瓶、1 紅 完全治療、2 橙 法力、3 黃 少量治療、4 綠 傷害（毒）、5 紫 暫時無敵、6 藍 沉睡、7 黑 隱形。
- 引擎：`Localization::translateBark` 先查 `bark CCCC:IIII#畫格`（說話物品的畫格），再查原本的條目；`TranslationCatalog::canonicalContext` 接受 `#畫格`（只限 bark）。單元測試補上。
- 譯文：`localization/zh_TW/ui/item_frames.po`（手動維護，抽取工具不會覆蓋）；`po_compile.py`、`u8catalog.py check` 支援此格式。

## 已研究、暫緩：高解析度的介面放大

開啟 ScummVM「高解析度」（640×480）後介面變小。可行做法是加一個 2 倍的「介面層」（拖曳時的縮回會自然成立），主要風險在高解析中文字的大小與位置換算。使用者決定先放著。
