# 大豐環保 職業災害分析報告網站

大豐環保法務及環安課職災分析報告，部署於 GitHub Pages。

## 網站結構

```
docs/                      ← GitHub Pages 發佈目錄
├── index.html             ← 首頁（報告總覽入口）
├── css/
│   ├── common.css         ← 共用樣式（變數、排版、元件）
│   └── sidebar.css        ← 側邊目錄樣式
├── js/
│   └── sidebar.js         ← 側邊目錄互動邏輯
└── reports/
    ├── overview.html      ← 三年總覽（2023-2025）
    ├── 2023.html          ← 2023 年度報告
    ├── 2024.html          ← 2024 年度報告
    └── 2025.html          ← 2025 年度報告
```

## 部署

- GitHub Pages source: `main` branch → `/docs` 目錄
- 推送到 `main` 後 1-2 分鐘自動更新

## 本地測試

```bash
cd docs
python -m http.server 3300
# 瀏覽器開啟 http://localhost:3300
```

## 更新流程

1. 更新 Excel 原始數據
2. 請 Claude Code 更新報告內容
3. Commit + Push → GitHub Pages 自動部署
