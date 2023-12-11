#!/bin/bash

# Your GitHub username
USERNAME="Olsens11"

# Your GitHub repository name
REPO_NAME="Jarvis"

# Change to your project directory
cd C:\Users\olsen\Jarvis

# Initialize Git if not done yet
if [ ! -d ".git" ]; then
  git init
fi

# Add all files to the staging area
git add .

# Commit changes
git commit -m "Initial commit"

# Add GitHub remote
git remote add origin https://github.com/Olsens11/Jarvis.git

# Push changes to GitHub
git push -u origin master
