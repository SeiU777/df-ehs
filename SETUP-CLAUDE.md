# Claude Code 設定與 Skills 遷移指南

> Claude Code 是 Anthropic 出品的 AI 編程助手，用於自動化報告更新和職災分析。
> 預估時間：20 分鐘

---

## 什麼是 Claude Code

Claude Code 讓 Claude AI 直接在你的電腦上操作檔案：
- 讀取 Excel 職災資料，自動更新 HTML 報告
- 分析事故截圖，產出專業分析報告（.docx）
- 輔助安委會簡報製作

**這不是必要工具** — 沒有 Claude Code 也可以手動編輯 HTML 報告。
但有了它，每月更新報告只需要一句話。

---

## 第一步：安裝 Claude Code

### 1.1 安裝方式

Claude Code 可透過 VS Code 擴充功能安裝：

1. 開啟 VS Code
2. 按 `Ctrl+Shift+X` 開啟擴充功能
3. 搜尋 "Claude Code"（Anthropic 官方出品）
4. 點擊安裝

或用 npm 安裝 CLI 版本：

```bash
npm install -g @anthropic-ai/claude-code
```

### 1.2 認證

需要以下其中一種：
- **Claude Max / Claude Team / Claude Enterprise 訂閱**（推薦）
- **Anthropic API Key**

首次啟動 Claude Code 時會引導你設定認證。

---

## 第二步：全域設定檔

以下設定檔需要放在你的使用者目錄的 `.claude/` 資料夾中。

### 2.1 建立目錄

```
C:\Users\{你的使用者名稱}\.claude\
```

### 2.2 settings.json — 全域設定

建立 `~/.claude/settings.json`：

```json
{
  "autoUpdatesChannel": "latest",
  "env": {
    "SHELL": "C:\\Users\\{你的使用者名稱}\\AppData\\Local\\Programs\\Git\\bin\\bash.exe"
  }
}
```

> **重要**：`SHELL` 路徑必須指向你電腦上 Git Bash 的實際路徑。
> 安裝 Git for Windows 後，通常在 `C:\Users\{使用者}\AppData\Local\Programs\Git\bin\bash.exe`。
> 也可能在 `C:\Program Files\Git\bin\bash.exe`。

### 2.3 CLAUDE.md — 全域指令

建立 `~/.claude/CLAUDE.md`，內容：

```markdown
# Global Guidelines

## Communication
- 回覆使用繁體中文
- 程式碼註解使用繁體中文

## Code Style
- 使用 2 空格縮進
- 優先使用 TypeScript

## Constraints
- 修改前先讀取檔案
- 不做未要求的重構
```

> 這個檔案告訴 Claude 用繁體中文回覆、遵守程式碼風格等。
> 你可以依自己的偏好修改。

---

## 第三步：Skills 遷移

Skills 是 Claude Code 的「技能包」，讓它具備特定領域的專業能力。

### 3.1 複製 Skills

從 `df-ehs/skills-backup/` 複製到你的 `~/.claude/skills/`：

```bash
# 建立 skills 目錄
mkdir -p ~/.claude/skills

# 複製三個職安專用 Skills
cp -r df-ehs/skills-backup/7-accident-analysis ~/.claude/skills/
cp -r df-ehs/skills-backup/7-occupational-safety-analyzer ~/.claude/skills/
cp -r df-ehs/skills-backup/dafong-html-report ~/.claude/skills/
```

> 在 Windows 上，你也可以直接用檔案總管複製。

### 3.2 修改硬編碼路徑

**這步很重要！** Skills 中有些路徑是寫死的，需要改成你的路徑。

#### 7-accident-analysis/SKILL.md

找到類似以下的路徑，替換 `chloe.chang` 為你的使用者名稱：

```
{homedir}/Documents/claude/職安/參考資料/安委會/pptx-workspace/node_modules/jszip
{homedir}/Documents/claude/職安/參考資料/公司職災資料/公司表單之事故選單內容.docx
```

#### 7-accident-analysis/report-template.js

第 9 行：
```javascript
const modulePath = path.join(homedir, 'Documents/claude/職安/參考資料/安委會/pptx-workspace/node_modules/docx');
```

如果你的專案路徑不同，需要修改此路徑。

> **建議**：將專案放在與原開發者相同的路徑（`Documents/claude/職安/`），
> 這樣就不需要修改 Skills 中的路徑。

### 3.3 Skills 功能說明

| Skill | 觸發方式 | 功能 | 輸出 |
|-------|---------|------|------|
| `7-accident-analysis` | 「這是公司新的職災案件，請你幫我做分析報告」 | 讀取事故截圖 → 深度分析 → 產出報告 | .docx |
| `7-occupational-safety-analyzer` | 「幫我分析公司職災資料」 | 讀取 Excel → 統計分析 → 產出報告 | .html |
| `dafong-html-report` | 需要製作大豐風格的報告時自動套用 | 大豐環保企業視覺風格 | .html |

### 3.4 Skills 依賴

`7-accident-analysis` Skill 需要以下 Node.js 套件（來自 pptx-workspace）：
- `jszip` — 讀取 .docx 檔案中的 XML
- `docx` — 產生 .docx 報告

確認 `參考資料/安委會/pptx-workspace/node_modules/` 存在且有這些套件。
如果沒有，執行：

```bash
cd 參考資料/安委會/pptx-workspace
npm install
```

---

## 第四步：專案設定

### 4.1 VS Code 工作區

在專案根目錄有 `職安.code-workspace` 檔案。用 VS Code 開啟它：

```
檔案 → 開啟工作區 → 選擇 職安.code-workspace
```

這會同時開啟專案目錄和 `.claude` 設定目錄。

### 4.2 專案層級設定

在 `職安/.claude/settings.local.json` 中可設定專案專屬的權限：

```json
{
  "permissions": {
    "allow": [
      "Bash(python ...)"
    ]
  }
}
```

這些權限在你使用 Claude Code 時會自動累積，不需要手動設定。

---

## 日常使用流程

### 更新月報

```
1. 開啟 VS Code，確認在職安工作區
2. 在終端機啟動 Claude Code（或使用 VS Code 的 Claude Code 面板）
3. 說：「資料更新了，幫我更新報告」
4. Claude 會讀取 Excel → 更新 HTML → 完成後通知你
5. 在終端機執行：
   cd df-ehs
   git add -A
   git commit -m "更新 YYYY-MM 月報"
   git push
```

### 分析新職災案件

```
1. 準備事故表單截圖
2. 在 Claude Code 中說「這是公司新的職災案件，請你幫我做分析報告」
3. 提供截圖
4. Claude 會辨識 → 分析 → 產出 .docx 報告
```

### 製作安委會簡報

```
1. 準備素材（照片、數據）
2. 在 Claude Code 中描述需求
3. Claude 會使用 pptx-workspace 工具或直接生成 HTML
```

---

## 疑難排解

### Q: Claude Code 說找不到某個檔案？

確認 `參考資料/` 資料夾已正確放置，且路徑與 Skills 中的設定一致。

### Q: Skills 沒有出現在可用列表中？

確認 SKILL.md 檔案放在 `~/.claude/skills/{skill-name}/SKILL.md`。
資料夾名稱必須與 Skill 名稱一致。

### Q: 執行 report-template.js 時出錯？

確認 `node_modules/docx` 已安裝：
```bash
cd 參考資料/安委會/pptx-workspace
npm install
```

### Q: Claude Code 版本更新後功能異常？

Claude Code 更新頻繁。如遇問題：
- 查看官方文件：https://docs.anthropic.com/claude-code
- 回報問題：https://github.com/anthropics/claude-code/issues
