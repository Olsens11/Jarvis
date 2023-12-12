#!/bin/bash

original_dir=$(pwd)

cd "$(dirname "${BASH_SOURCE[0]}")"

# Commit changes
git add --all
git commit -m "Automated commit before pull"

# Pull changes from the "main" branch
git pull origin main

# Change back to the original directory
cd "$original_dir"

# Pause to see the output (remove this line if you don't want to pause)
read -p "Press Enter to continue..."
