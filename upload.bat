@echo off

rem Your GitHub username
set USERNAME=Olsens11

rem Your GitHub repository name
set REPO_NAME=Jarvis

rem Change to your project directory
cd /d C:\Users\olsen\Jarvis

rem Initialize Git if not done yet
if not exist ".git" (
   git init
)

rem Add all files to the staging area
git add .

rem Commit changes
git commit -m "Initial commit"

rem Add GitHub remote
git remote add origin https://github.com/Olsens11/Jarvis.git

rem Push changes to GitHub
git push -u origin master
