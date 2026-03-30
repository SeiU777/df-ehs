@echo off
chcp 65001 >nul
title 職安專案 - 環境設定腳本

echo ============================================
echo   大豐環保 職安分析報告系統 - 環境設定
echo ============================================
echo.

:: ===== 檢查必要工具 =====
echo [1/6] 檢查 Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✘ Git 未安裝！請先安裝 Git for Windows：
    echo     https://git-scm.com/download/win
    echo.
    set HAS_ERROR=1
) else (
    for /f "tokens=*" %%v in ('git --version') do echo   ✔ %%v
)

echo [2/6] 檢查 Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✘ Python 未安裝！請先安裝 Python 3.12+：
    echo     https://www.python.org/downloads/
    echo     安裝時請勾選 "Add Python to PATH"
    echo.
    set HAS_ERROR=1
) else (
    for /f "tokens=*" %%v in ('python --version') do echo   ✔ %%v
)

echo [3/6] 檢查 Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   ✘ Node.js 未安裝！請先安裝 Node.js LTS：
    echo     https://nodejs.org/
    echo.
    set HAS_ERROR=1
) else (
    for /f "tokens=*" %%v in ('node --version') do echo   ✔ Node.js %%v
)

if defined HAS_ERROR (
    echo.
    echo ============================================
    echo   請先安裝上述缺少的工具後，再重新執行此腳本
    echo ============================================
    pause
    exit /b 1
)

echo.

:: ===== 安裝 Python 依賴 =====
echo [4/6] 安裝 Python 依賴...
if exist "%~dp0df-ehs\requirements.txt" (
    pip install -r "%~dp0df-ehs\requirements.txt"
) else if exist "%~dp0requirements.txt" (
    pip install -r "%~dp0requirements.txt"
) else (
    echo   ✘ 找不到 requirements.txt
)
echo.

:: ===== 安裝 Node.js 依賴 =====
echo [5/6] 安裝 Node.js 依賴（簡報工具）...
if exist "%~dp0參考資料\安委會\pptx-workspace\package.json" (
    cd /d "%~dp0參考資料\安委會\pptx-workspace"
    npm install
    cd /d "%~dp0"
) else (
    echo   ⚠ 找不到 pptx-workspace，跳過（安委會簡報功能將無法使用）
)
echo.

:: ===== 複製 Claude Code 設定 =====
echo [6/6] 設定 Claude Code...
set CLAUDE_DIR=%USERPROFILE%\.claude

if exist "%~dp0claude-config\CLAUDE.md" (
    if not exist "%CLAUDE_DIR%" mkdir "%CLAUDE_DIR%"

    :: 複製全域設定（不覆蓋已存在的檔案）
    if not exist "%CLAUDE_DIR%\CLAUDE.md" (
        copy "%~dp0claude-config\CLAUDE.md" "%CLAUDE_DIR%\CLAUDE.md" >nul
        echo   ✔ 已複製 CLAUDE.md
    ) else (
        echo   ⚠ CLAUDE.md 已存在，跳過（避免覆蓋你的設定）
    )

    if not exist "%CLAUDE_DIR%\settings.json" (
        copy "%~dp0claude-config\settings.json" "%CLAUDE_DIR%\settings.json" >nul
        echo   ✔ 已複製 settings.json
    ) else (
        echo   ⚠ settings.json 已存在，跳過
    )

    :: 複製 Skills
    if exist "%~dp0df-ehs\skills-backup" (
        if not exist "%CLAUDE_DIR%\skills" mkdir "%CLAUDE_DIR%\skills"
        xcopy /E /I /Y "%~dp0df-ehs\skills-backup\7-accident-analysis" "%CLAUDE_DIR%\skills\7-accident-analysis" >nul
        xcopy /E /I /Y "%~dp0df-ehs\skills-backup\7-occupational-safety-analyzer" "%CLAUDE_DIR%\skills\7-occupational-safety-analyzer" >nul
        xcopy /E /I /Y "%~dp0df-ehs\skills-backup\dafong-html-report" "%CLAUDE_DIR%\skills\dafong-html-report" >nul
        echo   ✔ 已複製 3 個職安專用 Skills
    )
) else (
    echo   ⚠ 找不到 claude-config/，跳過 Claude Code 設定
    echo     你可以稍後手動設定，參考 df-ehs/SETUP-CLAUDE.md
)

echo.
echo ============================================
echo   設定完成！
echo ============================================
echo.
echo   下一步：
echo   1. 開啟 VS Code，用「開啟工作區」載入 職安.code-workspace
echo   2. 在終端機執行：cd df-ehs\docs ^&^& python -m http.server 3300
echo   3. 瀏覽器開啟 http://localhost:3300 測試網站
echo.
echo   ⚠ 重要提醒：
echo   - Skills 中的路徑可能需要修改，詳見 df-ehs/SETUP-CLAUDE.md
echo   - settings.json 中的 SHELL 路徑需指向你電腦的 Git Bash
echo.
pause
