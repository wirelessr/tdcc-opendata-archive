# tdcc-opendata-archive

每週自動歸檔**台灣集中保管結算所集保戶股權分散表**（TDCC 1-5 dataset）的長期備份。

TDCC 官方 endpoint 只保留當週最新一筆，每週五被覆寫。本 repo 透過 GitHub Actions 每天檢查，將新週次的原始 CSV 永久存進 `snapshots/<YYYY>/<YYYY-MM-DD>.csv`。

## 當前覆蓋範圍

```
snapshots/
├── 2021/  (13 週，2021-07-02 ~ 2021-09-24)
│       來源：lisa4930007 的早期備份（https://github.com/lisa4930007/ownership_distribution_access_db）
└── 2026/  (從 2026-04-30 起持續累積)
```

## 使用方式

### 下載單週資料

```bash
curl -O https://raw.githubusercontent.com/wirelessr/tdcc-opendata-archive/main/snapshots/2026/2026-04-30.csv
```

### 下載全部歷史（shallow clone）

```bash
git clone --depth 1 https://github.com/wirelessr/tdcc-opendata-archive.git
```

### 程式化讀取（Python）

```python
import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/wirelessr/tdcc-opendata-archive/main/snapshots/2026/2026-04-30.csv",
    encoding="utf-8-sig",
)
# 欄位：資料日期, 證券代號, 持股分級, 人數, 股數, 占集保庫存數比例%
```

## 資料欄位

| 欄位 | 說明 |
|---|---|
| 資料日期 | `YYYYMMDD`，當週快照日期（週五）|
| 證券代號 | 股票代號（有 trailing spaces padding 到 6 字元，處理時需 `.str.strip()`）|
| 持股分級 | 1~17 的 integer。1~15 為分級（1 = 1-999 股、15 = >1,000,001 股），16 為差異調整，17 為合計列 |
| 人數 | 該分級持有人數 |
| 股數 | 該分級總持有股數 |
| 占集保庫存數比例% | 該分級佔發行股數比例 |

## 自動化機制

- **排程**：GitHub Actions 每日 UTC 02:00（CST 10:00）
- **幂等**：script 比對 `資料日期` 欄位，若該週已存檔則不 commit
- **手動觸發**：Actions 頁面可點 "Run workflow" 補抓
- **免費**：公開 repo，GHA 分鐘數無限

## 授權

- **腳本程式碼（`scripts/`、`.github/`、`LICENSE`）**：MIT License
- **資料檔（`snapshots/*.csv`）**：[政府資料開放授權條款第 1 版](https://data.gov.tw/license)，原始資料來源為[臺灣集中保管結算所 集保戶股權分散表](https://data.gov.tw/dataset/11452)（data.gov.tw dataset 11452）。可自由重製、商用、衍生，請保留來源標註。

## 致謝

- [lisa4930007/ownership_distribution_access_db](https://github.com/lisa4930007/ownership_distribution_access_db) — 提供 2021-07 至 2021-09 的 13 週早期歷史備份，本 repo 已將其納入 `snapshots/2021/`

## 相關專案

本 repo 的資料驅動另一個量化策略驗證專案 [three-gate-screener](https://github.com/wirelessr/three-gate-screener)。
