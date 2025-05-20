@echo off
setlocal

if "%~1"=="" (
    echo Usage: update_remote.bat ^<new_repository_url^>
    echo Example: update_remote.bat https://github.com/username/repo-name.git
    exit /b 1
)

set REPO_URL=%~1

echo Checking Git repository status...
git status >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Git repository not initialized. Initializing now...
    git init
)

echo Checking remote configuration...
git remote | findstr "origin" >nul
if %ERRORLEVEL% equ 0 (
    echo Updating existing remote origin...
    git remote set-url origin %REPO_URL%
) else (
    echo Adding new remote origin...
    git remote add origin %REPO_URL%
)

echo.
echo Remote successfully updated to: %REPO_URL%
echo.
echo To push your project to this repository, use:
echo   git add .
echo   git commit -m "Initial commit"
echo   git push -u origin main

endlocal