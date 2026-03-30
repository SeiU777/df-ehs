# 職安分析報告系統 — 架構說明

> 最後更新：2026-03-30

本文件說明系統全貌，幫助你快速理解各組件如何協作。

---

## 系統總覽

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Excel 職災資料  │────→│   Claude Code    │────→│  HTML 報告檔案   │
│ （每月更新）      │     │ （AI 讀取分析）    │     │ （df-ehs/docs/） │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │ git push
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  GitHub Pages   │
                                                 │ （自動部署網站）  │
                                                 └─────────────────┘
                                                          │
                                                          ▼
                                          https://seiu777.github.io/df-ehs/
```

---

## 四大組件

### A. GitHub Pages 靜態網站

**位置**：`df-ehs/docs/`
**技術**：純 HTML + CSS + JavaScript（無建置工具，無框架）

```
docs/
├── index.html              ← 首頁（報告總覽入口）
├── css/
│   ├── common.css          ← 共用樣式（大豐深藍 #1e4a6e + 環保綠 #4caf50）
│   ├── dark.css            ← 深色模式樣式
│   ├── sidebar.css         ← 側邊目錄樣式
│   └── training.css        ← 教育訓練頁面樣式
├── js/
│   ├── sidebar.js          ← 側邊目錄互動邏輯
│   ├── theme.js            ← 深色/淺色模式切換
│   ├── auth.js             ← 靜態網站密碼保護
│   └── training.js         ← 教育訓練測驗互動
├── reports/
│   ├── overview.html       ← 三年總覽（2023-2025）
│   ├── 2023.html           ← 2023 年度報告
│   ├── 2024.html           ← 2024 年度報告
│   ├── 2025.html           ← 2025 年度報告
│   ├── environmental-factors.html  ← 環境因素分析
│   ├── *-summary.html      ← 各報告的摘要版
│   └── committee/          ← 安委會季報
│       ├── index.html
│       └── 2026-Q1.html
└── training/
    ├── hq.html             ← 總部教育訓練
    └── quanxing.html       ← 全興教育訓練
```

**部署方式**：
- GitHub repo: `seiu777/df-ehs`
- 部署來源: `main` branch → `/docs` 目錄
- 推送後 1-2 分鐘自動更新

### B. Python 資料處理腳本

**位置**：`職安/`（專案根目錄）

| 腳本 | 功能 | 主要依賴 |
|------|------|---------|
| `analyze_accidents.py` | 職災資料統計分析 | 標準庫 |
| `read_excel.py` / `read_excel_v2.py` | 讀取職災 Excel | subprocess |
| `extract_with_ocr.py` | PDF 圖片文字擷取（OCR） | pymupdf |
| `extract_ocr.py` | PDF 文字擷取 | pdfplumber |
| `extract_all_pdfs.py` | 批次 PDF 處理 | subprocess |
| `search_wu.py` | 搜尋特定人員資料 | pandas |
| `backup_conversation.py` | 備份 Claude Code 對話 | 標準庫 |
| `read_pptx.py` | 讀取簡報內容 | subprocess |

**安裝依賴**：`pip install -r requirements.txt`

### C. Node.js 簡報工具

**位置**：`參考資料/安委會/pptx-workspace/`

| 檔案 | 功能 |
|------|------|
| `create-pptx.js` | 生成安委會 PowerPoint 簡報 |
| `create-committee-template.js` | 生成安委會 Word 模板 |
| `create-forklift-proposal.js` | 生成堆高機提案簡報 |
| `產生簡報.bat` | Windows 批次執行腳本 |

**依賴**（package.json）：
- `pptxgenjs` — PowerPoint 生成
- `docx` — Word 文件生成

**安裝**：`cd 參考資料/安委會/pptx-workspace && npm install`

### D. Claude Code + Skills（AI 協作）

Claude Code 是 Anthropic 出品的 AI 編程助手，用於：
- 讀取 Excel 職災資料 → 自動更新 HTML 報告
- 執行個案職災分析 → 產出 .docx 分析報告
- 輔助安委會簡報製作

**職安專用 Skills**：

| Skill | 功能 | 輸出格式 |
|-------|------|---------|
| `7-accident-analysis` | 個案職災分析報告 | .docx |
| `7-occupational-safety-analyzer` | 職災統計分析報告 | .html |
| `dafong-html-report` | 大豐企業風格 HTML 報告 | .html |

Skills 備份在 `df-ehs/skills-backup/`，遷移方式見 [SETUP-CLAUDE.md](SETUP-CLAUDE.md)。

---

## 三大工作流程

### 流程 1：月度報告更新

```
1. 使用者更新 Excel 最新職災資料
2. 在 Claude Code 中說「資料更新了，幫我更新報告」
3. Claude 讀取 Excel → 更新 HTML 報告（docs/reports/ 中的檔案）
4. 使用者在終端機執行 git add + commit + push
5. GitHub Pages 1-2 分鐘後自動部署
```

### 流程 2：個案職災分析

```
1. 使用者提供事故表單截圖
2. 使用 /7-accident-analysis skill
3. Claude 辨識截圖 → 讀取公司下拉選單 → 執行深度分析
4. 產出 .docx 報告，存放於 參考資料/公司職災資料/分析報告/{年份}/
```

### 流程 3：安委會簡報生成

```
1. 準備素材（照片、數據、會議紀錄）
2. 使用 pptx-workspace 中的 Node.js 腳本生成簡報
3. 或使用 Claude Code 直接生成安委會季報 HTML（docs/committee/）
```

---

## 目錄結構全覽

```
職安/                                    ← 專案根目錄
├── df-ehs/                             ← Git repo（GitHub Pages）
│   ├── docs/                           ← 網站檔案（見上方 A 節）
│   ├── skills-backup/                  ← Skills 備份
│   ├── requirements.txt                ← Python 依賴
│   ├── README.md                       ← 專案說明
│   ├── ARCHITECTURE.md                 ← 本文件
│   ├── SETUP.md                        ← 基礎工具安裝指南
│   ├── SETUP-CLAUDE.md                 ← Claude Code 設定指南
│   ├── SETUP-REFERENCE-DATA.md         ← 參考資料指南
│   └── .gitignore
├── 參考資料/                            ← 不進 Git（1.1GB+）
│   ├── 公司職災資料/                    ← 職災 Excel + 分析報告
│   ├── 安委會/                          ← 安委會素材 + pptx-workspace
│   ├── 職災分析方法/                    ← 事故調查手冊 + HSG48
│   ├── 教育訓練/                        ← 安全教育訓練資料
│   └── 原google分析內容與簡報/          ← 舊版分析報告
├── *.py                                ← Python 工具腳本
├── .claude/                            ← Claude Code 專案設定
└── 職安.code-workspace                 ← VS Code 工作區
```

---

## 環境版本參考

以下為 2026-03 開發環境版本，僅供參考：

| 工具 | 版本 |
|------|------|
| Windows | 11 Pro |
| Python | 3.12+ |
| Node.js | LTS（22.x 或 24.x） |
| Git | 2.52+ |
| Claude Code | 最新版 |
| VS Code | 最新版 |
