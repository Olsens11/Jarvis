#!/bin/bash

# Commit changes
git add --all
git commit -m "Automated commit before pull"

# Check if the commit was successful
if [ $? -eq 0 ]; then
    echo "Commit successful."
else
    echo "Error: Commit failed."
    exit 1
fi

# Pull changes from the "main" branch
git pull origin main

# Check if the pull was successful
if [ $? -eq 0 ]; then
    echo "Pull successful."
else
    echo "Error: Pull failed."
    exit 1
fi

# Pause to see the output (remove this line if you don't want to pause)
read -p "Press Enter to continue..."
