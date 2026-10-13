# Ultima VIII: Pagan 繁體中文化

[English](README_EN.md)

讓《創世紀 VIII：異教徒》（Ultima VIII: Pagan）以**正體中文**遊玩的同好專案。以 [ScummVM](https://www.scummvm.org/) 的 Ultima 8 引擎為基礎，在不修改原始遊戲資料的前提下，把對話、選項、書籍、捲軸、墓碑與介面顯示成中文。

> **目前狀態：v1.0.1 正式版。** 全遊戲翻譯完成（99.8%），提供 Windows 與 macOS（Apple Silicon、Intel）的免安裝版本，見[下載與安裝](#下載與安裝)。

## 特色

- **不修改遊戲資料**：遊戲邏輯永遠使用英文原文，只在畫面顯示時換成中文。對話分支、語音、存檔都和原版相同。
- **存檔只有英文**：中文模式和英文模式的存檔可以互換，隨時可以切回原版。
- **完整的對話中文化**：台詞、對話選項（點中文選項會走原本的分支）、書、捲軸、墓碑、牌匾、主選單與日記。
- **專有名詞自動加註**：同一次對話中第一次出現的名稱會顯示英文，例如「不列顛尼亞(Britannia)」，方便對照原版與攻略。
- **動態句子**：含玩家名字、數量、物品種類的句子（例如「50 堆木材」「發火術魔杖（剩 3 次）」）都能正確翻譯。
- **語音與字幕**：有語音的角色播放英文原音，配上中文字幕，翻頁與語音同步。
- **中文字型**：[Cubic 11（俐方體 11 號）](https://github.com/ACh-K/Cubic-11)點陣字型（SIL OFL 1.1），風格貼近原作；支援中文換行與標點禁則。
- **高解析中文字**：遊戲畫面維持原版的 320×200，中文則以視窗解析度、[jf open 粉圓](https://justfont.com/huninn/)字型繪製，清晰易讀；屬性頁也因此能顯示中文（預設開啟，可在遊戲選項關閉）。
- **墓碑牌匾全中文**：墓碑、牌匾與死亡畫面直接刻上中文（[王漢宗魏碑體](https://code.google.com/archive/p/wangfonts/)，加上雕刻陰影）；也可以改回英文雕刻加中文字幕。
- **快捷圖示列**：滑鼠移到右下角就會出現（仿 Exult），可直接開背包、屬性頁、地圖、選單，存讀檔、切換戰鬥模式、使用鑰匙圈與召回石。
- **自動走近使用**：雙擊太遠的門、箱子、書等物品時，聖者會自己走過去再使用。
- **對話與視窗操作**：對話時點畫面任何地方都會翻頁（同 Ultima VII）；Esc 先關閉最上層的箱子、背包、屬性頁，再打開選單。
- **細部設定**：字型、字級、字距、行距、台詞框大小、音樂音源（General MIDI、AdLib、Roland MT-32）都可以調整；常用的項目在遊戲設定的中文設定頁用下拉選單和滑桿調整，ScummVM 介面也是正體中文。
- **安全退回**：找不到譯文、翻譯檔損壞或缺字型時，一律顯示英文原文，不會出現亂碼或當機。

## 翻譯進度

<!-- progress:start -->
**整體進度（以英文字元計）：`████████████████████` 99.8%**（6,986 / 7,035 條，更新於 2026-10-13）

| 類別 | 已翻譯 / 全部（條） | 英文字元 | 進度 |
|---|---|---|---|
| 台詞與物品名稱 | 4,827 / 4,835 | 375,445 | 99.8% |
| 對話選項 | 1,822 / 1,863 | 36,829 | 99.8% |
| 書 | 87 / 87 | 116,622 | 100.0% |
| 捲軸 | 22 / 22 | 7,864 | 100.0% |
| 墓碑 | 67 / 67 | 2,609 | 100.0% |
| 牌匾 | 63 / 63 | 1,410 | 100.0% |
| 句子參數 | 60 / 60 | 544 | 100.0% |
| 介面文字 | 38 / 38 | 564 | 100.0% |

已完成的角色與場景：Abacus、Agware、Airfocus、Altar、Altar_ew、Amostat、Anctones、Anvil、Aorta、Apastat、Appear、阿拉米娜、阿卡迪昂、Armguard、Armor、Axe、Axe2、Axeblade、Backpack、Bag、貝恩、Bane2、Barentry、Barrel、Basebook、Basescrl、Basket、Bathstuf、Bellows、Benchew、班提克、貝倫、Berenhch、Bgate、Bigdemst、Bigugly、Bladstrk、Blankets、Boat、Bones、Bones2、Bones3、Bones4、Book1、Bookbloo、Bookmark、Bottle、Branches、Bribook、Bribook2、Bribook3、Bribook4、Bribook5、Bribook6、Brock、Brokchar、Broken、Brokstf1、Bug、Burndout、Calguard、Campfire、Candlbra、Candle、Canopy、Canopyew、Canopytp、Cauldron、Chair、Chest_ew、Chest_ns、Child、Chimney、Chopblk、Cloth、Clothes、Clothing、Codew、Codns、黑曜石幣、珂林絲、Cuffs、Cup、Cusion、席勒斯、Daemscen、Daemspel、Dagger、Dagger2、Dart、Dartbord、Deadcloz、Deadew、Deadns、Deathdis、Deceiver、Demnstat、Demon、Deskew、Deskns、Deskpict、戴文、Door_ns、Dtable、Dummy、Earthmag、Ebrock、Endgate、Endgate2、Endhydro、Endlamp、Endlith、Endskul、Endstrat、Erthitem、Erthreag、Erthspel、Ethereag、Evilsorc、Ewbpaint、Ewcrops、Ewhollog、Ewlamptp、Ewshelf、Ewshfsid、Ewspaint、處決場景、Eye、Fallrock、Fan、Febarsew、Febarsns、Fenalia、Fgrenade、Fight、Firefeld、Fireglob、Fireitem、Firepit、Fireplac、Fireplew、Fireplns、Firereag、Fireshld、Fireshro、Firespel、Fireswmp、Firewood、Fish、Fish2、Fishbonz、Fishnet、Fishpole、Flamstng、Flask、Floatin、Flour、Food、Free、Ftableew、Ftablens、Gargoyle、Gateskul、Gemofpro、Ghost、Ghosthed、Ghoul、Girlsstu、Golem、戈格隆德、Graveii、Grave_ew、Grave_ns、Greentre、Grenade、Grimoire、城門衛兵、Guard10、Guard2、Guard3、Guard4、Guard5、Guard6、Guard7、Guard8、Guard9、Guardman、Guard_ew、威廉、Hammer、Hamostr、Hay、Helmet、Hourglas、海特蘿、Intern、Ironman、Jbox、珍娜、Jewelry、Jug、Kegew、Kegns、Key、Keyonec、Keyring、綺蘭朵、Kingbdew、Kingbdns、Kith、Korgfang、科里克、Lamp1、Lamp2、Lamp3、Lamppost、Lava、Lavasink、Layghoul、Lchst_ew、Lchst_ns、Legging、Legs、Lever、里索斯、Litlmush、Logbook、Logbook2、Logbook3、Logbook4、Logo、Loom、Lothalt、Lothcorp、Lothlay、Mace、Mace2、Magarm、Magarmr2、Magarms、Maghelm、Maglegs、Magscrol、Magshld、麥爾吉爾、Marble、Melbook、Method、Mir、Monfast、莫迪雅、Mordeabe、Mordstat、Morebrok、Morefish、Morefood、Move、Mushcap、Mushgrup、Mushroom、米瑟倫、Nec1、Nitstand、Nsbpaint、Nscrops、Nshollog、Nslamptp、Nsrunwod、Nsshelf、Nsshfsid、Nsspaint、Nssticks、Oaktblew、Oaktblns、Odistat、Offsup、Opnbdrol、歐洛克、Oven、Pedestal、Pent、Pesant1、Pesant2、Pesant3、Plaqueew、Plaquens、Platefoo、Pole、Potion、Potplant、Potspans、Protectr、Pulchnew、Pulchnns、派羅斯、Rainbarl、Rat、Recall、芮安、Rope、Sabre、Salklog、Schair、Scimitar、Scimokg、Screamer、Scroll1、Scroll2、Sgargl、Sgbook、夏娜、Shchimne、Shield、Shortmsh、Silvore、Sinking、Skeleton、Skulcand、Skullhea、Skulz、Slayer、Smalmush、Sorcerer、Sorchat、Spelcmbt、Spider、Spiky、Spitter、Spout、Stalag、Statue、Statue1、Statuet、史泰洛斯、Stevbook、Stmite、Stovpipe、Strathat、史卓拉透絲、Straw、Sword、Sword2、Tablware、Tallcand、Tankard、Tapestew、Tapestns、塔娜、Thurgist、Tomb、托蘭、Torax、Torch、Tortchar、Tortrack、托溫、Tossrock、Toys、Trap、Tree、Trialhat、Tring、Troll、Troodle、Troughew、Troughns、Trowel、Vanish、瓦迪恩、Vardion2、Vase、Vivalter、Vivdagr、維菲多斯、Wallswit、Wardew、Wardns、Wbench、Well、Winchew、Winchns、Wool、Woundtor、Wtable、Wtableew、Wthrone、_
<!-- progress:end -->

全遊戲的對話、書籍與介面都已翻譯；未翻的少數條目是刻意保留的：作弊選單的密碼與座標資訊、數字選項 0–9 等。人名、地名等譯名統一記錄在[權威檔](localization/zh_TW/authority.tsv)。製作人員名單與開發者語錄維持英文，語音維持英文原音。

## 下載與安裝

到 [Releases](https://github.com/pmanyeh/Ultima-8-for-ZH/releases) 下載：

| 檔案 | 適用 |
|---|---|
| `Ultima8-zhTW-<版本>.zip` | Windows（64 位元） |
| `Ultima8-zhTW-<版本>-macOS-arm64.zip` | macOS，Apple Silicon（M 系列晶片） |
| `Ultima8-zhTW-<版本>-macOS-x86_64.zip` | macOS，Intel |

**需要你自己的正版 Ultima VIII 英文版遊戲資料**（例如 GOG 的 *Ultima 8 Gold Edition*）。本專案**不包含**任何遊戲資料、音樂、語音或存檔。

壓縮檔內附 ScummVM（加入中文化功能的版本）、翻譯檔與字型，解壓即可使用，不需安裝。步驟與設定說明都在壓縮檔內：

- [安裝說明（Windows）](package/INSTALL.zh-TW.md)、[安裝說明（macOS）](package/INSTALL-macOS.zh-TW.md)
- [設定說明](package/SETTINGS.zh-TW.md)：字型、台詞框、音樂音源等
- [主控台指令](package/CONSOLE.zh-TW.md)：傳送、作弊、播放動畫與音樂等進階功能
- [更新紀錄](package/CHANGELOG.md)

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
| `tools/build/`、`tools/package/` | 建置引擎、打包 Windows 與 macOS 版 |
| `package/` | 玩家文件（安裝、設定、主控台指令、更新紀錄）、字型、預設設定檔 |
| `.github/workflows/` | macOS 版的自動建置（GitHub Actions） |
| `docs/` | 計畫、架構決策（ADR）、各 Phase 報告 |

## 引擎原始碼

引擎的修改在 [pmanyeh/scummvm 的 `ultima8-zh-tw-dev` 分支](https://github.com/pmanyeh/scummvm/tree/ultima8-zh-tw-dev)（GPL，原始碼公開）。想自行建置的話，Windows 用 `tools/build/build_release.bat` 與 `tools/package/make_package.ps1`，macOS 見 `.github/workflows/macos.yml`。

## 參與翻譯

翻譯檔格式、要保留的符號、檢查與編譯流程，請見 [localization/README.md](localization/README.md)。

```bash
python tools/catalog/u8catalog.py check zh_TW      # 檢查譯文
python tools/catalog/u8catalog.py stats zh_TW      # 進度統計
python tools/catalog/progress.py zh_TW             # 更新本頁的翻譯進度
```

## 版權與授權

- Ultima VIII: Pagan 及其文字的著作權屬於原權利人（Origin Systems / Electronic Arts）。翻譯檔中保留的英文原文，僅作為對照翻譯之用。
- 中文字型 Cubic 11、jf open 粉圓採用 SIL Open Font License 1.1；王漢宗魏碑體採用 GPL-2.0。
- 本專案（譯文、權威檔、工具）以 GNU General Public License v3.0 或更新版本授權，全文見 [LICENSE](LICENSE)；引擎修改沿用 ScummVM 的 GPL-3.0。

## 致謝

- [ScummVM](https://www.scummvm.org/) 與 Pentagram 團隊的 Ultima 8 引擎
- [Cubic 11（俐方體 11 號）](https://github.com/ACh-K/Cubic-11)
- [jf open 粉圓](https://justfont.com/huninn/)（justfont）
- 王漢宗教授的[王漢宗自由字型](https://code.google.com/archive/p/wangfonts/)
- 所有 Ultima 同好
