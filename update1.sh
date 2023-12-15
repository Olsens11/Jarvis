#!/bin/bash

# Commit changes
git add --all
git commit -m "Automated commit before pull" || { echo "Error: Commit failed."; exit 1; }

# Pull changes from the "main" branch
git pull origin main || { echo "Error: Pull failed."; exit 1; }

echo "Script completed successfully."
