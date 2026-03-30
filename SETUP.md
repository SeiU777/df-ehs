# 環境設定指南 — 基礎工具安裝

> 從零開始，在一台全新的 Windows 電腦上建立完整工作環境。
> 預估時間：30 分鐘

---

## 前置條件

- Windows 10 或 11 電腦
- 可連上網路（安裝軟體、存取 GitHub）
- 管理員權限（安裝軟體用）

---

## 第一步：安裝 Git

Git 是版本控制工具，用來管理網站程式碼和部署。

1. 前往 https://git-scm.com/download/win 下載安裝程式
2. 安裝時保持預設選項即可
3. 安裝完成後，開啟「命令提示字元」或「PowerShell」驗證：

```
git --version
```

應顯示類似 `git version 2.x.x`。

---

## 第二步：安裝 Python

Python 用來執行資料處理腳本（讀取 Excel、處理 PDF 等）。

1. 前往 https://www.python.org/downloads/ 下載最新版（3.12 以上）
2. **安裝時務必勾選 "Add Python to PATH"**（在安裝畫面底部的核取方塊）
3. 驗證：

```
python --version
```

應顯示 `Python 3.x.x`。

> **注意**：如果顯示「不是內部或外部命令」，表示 PATH 沒設好。
> 請重新安裝並勾選 "Add Python to PATH"，或手動將 Python 路徑加入系統環境變數。

---

## 第三步：安裝 Node.js

Node.js 用來執行簡報生成工具（安委會 PowerPoint/Word）。

1. 前往 https://nodejs.org/ 下載 LTS 版本（長期支援版）
2. 安裝時保持預設選項
3. 驗證：

```
node --version
npm --version
```

---

## 第四步：安裝 VS Code（建議）

VS Code 是程式碼編輯器，用來瀏覽和編輯專案檔案。

1. 前往 https://code.visualstudio.com/ 下載安裝
2. 建議安裝的擴充功能：
   - **Claude Code** — Anthropic 官方 AI 編程助手（見 [SETUP-CLAUDE.md](SETUP-CLAUDE.md)）
   - **Live Server** — 本地預覽 HTML 報告

---

## 第五步：複製專案

### 5.1 取得 GitHub 存取權限

你需要 `seiu777/df-ehs` repo 的存取權限。請聯繫 repo 管理員，將你的 GitHub 帳號加為 collaborator。

### 5.2 Clone 專案

建議放置路徑（與原開發者一致，減少設定修改）：

```
C:\Users\{你的使用者名稱}\Documents\claude\職安\
```

執行：

```bash
# 先建立資料夾
mkdir -p C:\Users\{你的使用者名稱}\Documents\claude\職安

# 進入資料夾
cd C:\Users\{你的使用者名稱}\Documents\claude\職安

# Clone 專案
git clone https://github.com/seiu777/df-ehs.git
```

### 5.3 設定 Git 使用者資訊

```bash
git config --global user.name "你的姓名"
git config --global user.email "你的信箱@example.com"
```

---

## 第六步：安裝 Python 依賴

```bash
cd C:\Users\{你的使用者名稱}\Documents\claude\職安\df-ehs
pip install -r requirements.txt
```

驗證安裝成功：

```bash
python -c "import openpyxl; import pdfplumber; import pandas; print('所有依賴安裝成功')"
```

---

## 第七步：取得參考資料

參考資料（1.1GB+）不在 Git 中，需要另外取得。

請參閱 [SETUP-REFERENCE-DATA.md](SETUP-REFERENCE-DATA.md) 的詳細說明。

取得後，在 `職安/` 目錄下應有 `參考資料/` 資料夾。

---

## 第八步：安裝 Node.js 依賴

```bash
cd 參考資料\安委會\pptx-workspace
npm install
```

這會安裝 `pptxgenjs`（PowerPoint 生成）和 `docx`（Word 生成）等套件。

---

## 第九步：本地測試網站

```bash
cd C:\Users\{你的使用者名稱}\Documents\claude\職安\df-ehs\docs
python -m http.server 3300
```

開啟瀏覽器，輸入 http://localhost:3300 ，應可看到職災分析報告首頁。

按 `Ctrl+C` 停止伺服器。

---

## 第十步：設定 Claude Code（選擇性）

如果需要使用 AI 輔助更新報告和分析職災案件，請參閱 [SETUP-CLAUDE.md](SETUP-CLAUDE.md)。

---

## 常見問題

### Q: `python` 指令找不到？

Windows 上有時需要用 `py` 代替 `python`：

```
py --version
py -m http.server 3300
```

或者重新安裝 Python 並確認勾選 "Add Python to PATH"。

### Q: `git push` 被拒絕？

確認你已被加入 `seiu777/df-ehs` repo 的 collaborator。聯繫 repo 管理員。

### Q: 網站更新後沒變化？

GitHub Pages 部署有 1-2 分鐘延遲。清除瀏覽器快取（Ctrl+Shift+R）後再試。

### Q: 中文資料夾名稱有問題？

本專案的資料夾名稱含中文（如 `職安`、`參考資料`）。如果遇到編碼問題：

```bash
# 設定 Git 支援 UTF-8 檔名
git config --global core.quotepath false
```

### Q: npm install 失敗？

確認 Node.js 已正確安裝，且網路可連上 npm registry。如果公司有代理伺服器：

```bash
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080
```
