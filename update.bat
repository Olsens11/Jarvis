@echo off
cd %~dp0

:: Update all files and folders
git add --all
git commit -m "Update all files and folders"
git push origin main

:: Pause to see the output (remove this line if you don't want to pause)
pause
