@echo off
setlocal
cd /d "D:\5TH SEM\extention"

echo ==============================================
echo  CyberShield GitHub Daily Auto-Push
echo ==============================================

set MSG=%~1
if "%MSG%"=="" set MSG=daily update: %date% %time%

echo [1/3] Staging changes...
git add .

echo [2/3] Committing changes with message: "%MSG%"...
git commit -m "%MSG%"

echo [3/3] Pushing to GitHub (origin main)...
git push origin main

echo.
echo ==============================================
echo  Successfully Pushed to GitHub!
echo  Actions will build APK automatically:
echo  https://github.com/meetbhai78/ai-phishing-link/actions
echo ==============================================
pause
