# Ultima VIII: Pagan 繁體中文化

[English](README_EN.md)

讓《創世紀 VIII：異教徒》（Ultima VIII: Pagan）以**正體中文**遊玩的同好專案。以 [ScummVM](https://www.scummvm.org/) 的 Ultima 8 引擎為基礎，在不修改原始遊戲資料的前提下，把對話、選項、書籍、捲軸、墓碑與介面顯示成中文。

> **目前狀態：開發中，尚無可下載的版本。** 技術架構已經完成並經過遊戲內驗證（Phase 0–12），正在進行正式翻譯。

## 特色

- **不修改遊戲資料**：遊戲邏輯永遠使用英文原文，只在畫面顯示時換成中文。對話分支、語音、存檔都和原版相同。
- **存檔只有英文**：中文模式和英文模式的存檔可以互換，隨時可以切回原版。
- **完整的對話中文化**：台詞、對話選項（點中文選項會走原本的分支）、書、捲軸、墓碑、牌匾、主選單與日記。
- **專有名詞自動加註**：同一次對話中第一次出現的名稱會顯示英文，例如「不列顛尼亞(Britannia)」，方便對照原版與攻略。
- **動態句子**：含玩家名字、數量、物品種類的句子（例如「50 堆木頭」「點燃術魔杖（剩 3 次）」）都能正確翻譯。
- **語音與字幕**：有語音的角色播放英文原音，配上中文字幕，翻頁與語音同步。
- **中文字型**：[Cubic 11（俐方體 11 號）](https://github.com/ACh-K/Cubic-11)點陣字型（SIL OFL 1.1），風格貼近原作；支援中文換行與標點禁則。
- **高解析中文字**：遊戲畫面維持原版的 320×200，中文則以視窗解析度、[jf open 粉圓](https://justfont.com/huninn/)字型繪製，清晰易讀；屬性頁也因此能顯示中文（預設開啟，可在遊戲選項關閉）。
- **快捷圖示列**：滑鼠移到右下角就會出現（仿 Exult），可直接開背包、屬性頁、地圖、選單，存讀檔、切換戰鬥模式、使用鑰匙圈與召回石。
- **安全退回**：找不到譯文、翻譯檔損壞或缺字型時，一律顯示英文原文，不會出現亂碼或當機。

## 翻譯進度

<!-- progress:start -->
**整體進度（以英文字元計）：`████████████████████` 99.8%**（6,956 / 7,007 條，更新於 2026-10-10）

| 類別 | 已翻譯 / 全部（條） | 英文字元 | 進度 |
|---|---|---|---|
| 台詞與物品名稱 | 4,817 / 4,827 | 375,375 | 99.8% |
| 對話選項 | 1,822 / 1,863 | 36,829 | 99.8% |
| 書 | 87 / 87 | 116,622 | 100.0% |
| 捲軸 | 22 / 22 | 7,864 | 100.0% |
| 墓碑 | 67 / 67 | 2,609 | 100.0% |
| 牌匾 | 63 / 63 | 1,410 | 100.0% |
| 句子參數 | 54 / 54 | 505 | 100.0% |
| 介面文字 | 24 / 24 | 457 | 100.0% |

已完成的角色與場景：Abacus、Agware、Airfocus、Altar、Altar_ew、Amostat、Anctones、Anvil、Aorta、Apastat、Appear、阿拉米娜、阿卡迪昂、Armguard、Armor、Axe、Axe2、Axeblade、Backpack、Bag、貝恩、Bane2、Barentry、Barrel、Basebook、Basescrl、Basket、Bathstuf、Bellows、Benchew、班提克、貝倫、Berenhch、Bgate、Bigdemst、Bigugly、Bladstrk、Blankets、Boat、Bones、Bones2、Bones3、Bones4、Book1、Bookbloo、Bookmark、Bottle、Branches、Bribook、Bribook2、Bribook3、Bribook4、Bribook5、Bribook6、Brock、Brokchar、Broken、Brokstf1、Bug、Burndout、Calguard、Campfire、Candlbra、Candle、Canopy、Canopyew、Canopytp、Cauldron、Chair、Chest_ew、Chest_ns、Child、Chimney、Chopblk、Cloth、Clothes、Clothing、Codew、Codns、黑曜石幣、柯林斯、Cuffs、Cup、Cusion、席勒斯、Daemspel、Dagger、Dagger2、Dart、Dartbord、Deadcloz、Deadew、Deadns、Deathdis、Deceiver、Demnstat、Demon、Deskew、Deskns、Deskpict、戴文、Door_ns、Dtable、Dummy、Earthmag、Ebrock、Endgate、Endgate2、Endhydro、Endlamp、Endlith、Endskul、Endstrat、Erthitem、Erthreag、Erthspel、Ethereag、Evilsorc、Ewbpaint、Ewcrops、Ewhollog、Ewlamptp、Ewshelf、Ewshfsid、Ewspaint、處決場景、Eye、Fallrock、Fan、Febarsew、Febarsns、Fenalia、Fgrenade、Fight、Firefeld、Fireglob、Fireitem、Firepit、Fireplac、Fireplew、Fireplns、Firereag、Fireshld、Fireshro、Firespel、Fireswmp、Firewood、Fish、Fish2、Fishbonz、Fishnet、Fishpole、Flamstng、Flask、Floatin、Flour、Food、Free、Ftableew、Ftablens、Gargoyle、Gateskul、Gemofpro、Ghost、Ghosthed、Ghoul、Girlsstu、Golem、戈格隆德、Graveii、Grave_ew、Grave_ns、Greentre、Grenade、Grimoire、城門衛兵、Guard10、Guard2、Guard3、Guard4、Guard5、Guard6、Guard7、Guard8、Guard9、Guardman、Guard_ew、威廉、Hammer、Hamostr、Hay、Helmet、Hourglas、海德羅斯、Intern、Ironman、Jbox、珍娜、Jewelry、Jug、Kegew、Kegns、Key、Keyonec、Keyring、奇蘭卓、Kingbdew、Kingbdns、Kith、Korgfang、科里克、Lamp1、Lamp2、Lamp3、Lamppost、Lava、Lavasink、Layghoul、Lchst_ew、Lchst_ns、Legging、Legs、Lever、利索斯、Litlmush、Logbook、Logbook2、Logbook3、Logbook4、Logo、Loom、Lothalt、Lothcorp、Lothlay、Mace、Mace2、Magarm、Magarmr2、Magarms、Maghelm、Maglegs、Magscrol、Magshld、馬爾奇爾、Marble、Melbook、Method、Mir、Monfast、莫爾迪亞、Mordeabe、Mordstat、Morebrok、Morefish、Morefood、Move、Mushcap、Mushgrup、Mushroom、米斯蘭、Nec1、Nitstand、Nsbpaint、Nscrops、Nshollog、Nslamptp、Nsrunwod、Nsshelf、Nsshfsid、Nsspaint、Nssticks、Oaktblew、Oaktblns、Odistat、Offsup、Opnbdrol、歐洛克、Oven、Pedestal、Pent、Pesant1、Pesant2、Pesant3、Plaqueew、Plaquens、Platefoo、Pole、Potion、Potplant、Potspans、Protectr、Pulchnew、Pulchnns、派羅斯、Rainbarl、Rat、Recall、芮安、Rope、Sabre、Salklog、Schair、Scimitar、Scimokg、Screamer、Scroll1、Scroll2、Sgargl、Sgbook、夏娜、Shchimne、Shield、Shortmsh、Silvore、Sinking、Skeleton、Skulcand、Skullhea、Skulz、Slayer、Smalmush、Sorchat、Spelcmbt、Spider、Spiky、Spitter、Spout、Stalag、Statue、Statue1、Statuet、史泰洛斯、Stevbook、Stmite、Stovpipe、Strathat、史特拉托斯、Straw、Sword、Sword2、Tablware、Tallcand、Tankard、Tapestew、Tapestns、塔娜、Thurgist、Tomb、托蘭、Torax、Torch、Tortchar、Tortrack、托溫、Tossrock、Toys、Trap、Tree、Trialhat、Tring、Troll、Troodle、Troughew、Troughns、Trowel、Vanish、瓦爾迪恩、Vardion2、Vase、Vivalter、Vivdagr、維維多斯、Wallswit、Wardew、Wardns、Wbench、Well、Winchew、Winchns、Wool、Woundtor、Wtable、Wtableew、Wthrone、_
<!-- progress:end -->

翻譯順序依劇情進行：第一批是開場（戴文 → 泰尼伯瑞碼頭的處決）。人名、地名等譯名統一記錄在[權威檔](localization/zh_TW/authority.tsv)。

## 運作方式

```text
遊戲（Usecode）── 英文字串 ──▶ 對話、比對、語音、存檔（全部維持英文）
                      │
                      ▼ 只在建立顯示元件時
            翻譯檔（gettext MO）查表：位置 + 英文原文 → 中文
                      │
                      ▼
               中文顯示（CJK 字型）
```

- 每一句台詞以「Usecode class + 呼叫位置」識別，對話選項以「class + 英文」識別。英文必須完全相符才會顯示譯文，所以譯文永遠不會出現在錯誤的地方。
- 翻譯檔是 PO 格式，每個 Usecode class 一個檔（`localization/zh_TW/dialog/`），依對話流程排列，可用 Poedit 或文字編輯器編輯。
- 詳細設計見 [Master Plan](ULTIMA8_CHINESE_LOCALIZATION_MASTER_PLAN.md) 與 [docs/architecture](docs/architecture/)；各階段的實作與驗證紀錄在 [docs/reports](docs/reports/)。

## 目錄

| 路徑 | 內容 |
|---|---|
| `localization/zh_TW/dialog/` | 翻譯檔（394 個，依 Usecode class 分檔） |
| `localization/zh_TW/authority.tsv` | 權威檔：人名、地名、物品、魔法等的統一譯名 |
| `localization/README.md` | 給譯者的說明：格式、要保留的符號、流程 |
| `tools/extract/` | 從遊戲資料抽取文字（依對話流程與分支） |
| `tools/catalog/` | 合併、檢查、統計、編譯翻譯檔、翻譯批次工具 |
| `tools/validate/`、`tools/automation/` | 字型覆蓋、存檔檢查、存讀檔矩陣、啟動回歸測試 |
| `tools/diagnostics/` | Usecode 反組譯等研究工具 |
| `docs/` | 計畫、架構決策（ADR）、各 Phase 報告 |

## 你需要準備

- **合法的 Ultima VIII 遊戲資料**（例如 GOG 版 Ultima VIII Gold Edition，英文版）。本 repo **不包含**任何遊戲資料檔、音樂、語音或存檔。
- 修改過的 ScummVM：引擎的修改在 [pmanyeh/scummvm 的 `ultima8-zh-tw-dev` 分支](https://github.com/pmanyeh/scummvm/tree/ultima8-zh-tw-dev)（GPL，原始碼公開）。目前需要自行建置；之後會提供建置好的專用版與安裝說明。

## 參與翻譯

翻譯檔格式、要保留的符號、檢查與編譯流程，請見 [localization/README.md](localization/README.md)。

```bash
python tools/catalog/u8catalog.py check zh_TW      # 檢查譯文
python tools/catalog/u8catalog.py stats zh_TW      # 進度統計
python tools/catalog/progress.py zh_TW             # 更新本頁的翻譯進度
```

## 版權與授權

- Ultima VIII: Pagan 及其文字的著作權屬於原權利人（Origin Systems / Electronic Arts）。翻譯檔中保留的英文原文，僅作為對照翻譯之用。
- 中文字型 Cubic 11、jf open 粉圓採用 SIL Open Font License 1.1。
- 本專案（譯文、權威檔、工具）以 GNU General Public License v3.0 或更新版本授權，全文見 [LICENSE](LICENSE)；引擎修改沿用 ScummVM 的 GPL-3.0。

## 致謝

- [ScummVM](https://www.scummvm.org/) 與 Pentagram 團隊的 Ultima 8 引擎
- [Cubic 11（俐方體 11 號）](https://github.com/ACh-K/Cubic-11)
- [jf open 粉圓](https://justfont.com/huninn/)（justfont）
- 所有 Ultima 同好
