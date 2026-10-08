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
- **安全退回**：找不到譯文、翻譯檔損壞或缺字型時，一律顯示英文原文，不會出現亂碼或當機。

## 翻譯進度

<!-- progress:start -->
**整體進度（以英文字元計）：`██████████████░░░░░░` 70.4%**（5,449 / 6,995 條，更新於 2026-10-09）

| 類別 | 已翻譯 / 全部（條） | 英文字元 | 進度 |
|---|---|---|---|
| 台詞與物品名稱 | 3,738 / 4,827 | 375,375 | 92.0% |
| 對話選項 | 1,672 / 1,863 | 36,829 | 95.4% |
| 書 | 1 / 87 | 116,622 | 0.2% |
| 捲軸 | 1 / 22 | 7,864 | 1.0% |
| 墓碑 | 2 / 67 | 2,609 | 1.1% |
| 牌匾 | 2 / 63 | 1,410 | 2.3% |
| 句子參數 | 21 / 54 | 505 | 38.6% |
| 介面文字 | 12 / 12 | 152 | 100.0% |

已完成的角色與場景：阿拉米娜、阿卡迪昂、貝恩、Bane2、Basket、班提克、貝倫、Berenhch、Child、黑曜石幣、柯林斯、席勒斯、戴文、處決場景、Fight、Food、戈格隆德、城門衛兵、Guard10、Guard2、Guard3、Guard4、Guard5、Guard6、Guard7、Guard8、Guard9、Guardman、Guard_ew、威廉、海德羅斯、珍娜、Keyonec、奇蘭卓、科里克、利索斯、馬爾奇爾、莫爾迪亞、Morefish、米斯蘭、歐洛克、Pent、Pesant1、Pesant2、Pesant3、派羅斯、芮安、夏娜、史泰洛斯、史特拉托斯、塔娜、托蘭、托溫、瓦爾迪恩、Vardion2、維維多斯、Winchns
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
- 中文字型 Cubic 11 採用 SIL Open Font License 1.1。
- 本專案的授權條款將在正式發布前決定。

## 致謝

- [ScummVM](https://www.scummvm.org/) 與 Pentagram 團隊的 Ultima 8 引擎
- [Cubic 11（俐方體 11 號）](https://github.com/ACh-K/Cubic-11)
- 所有 Ultima 同好
