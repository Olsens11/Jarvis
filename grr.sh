#!/bin/bash

# Step 1: Download the latest Adafruit CircuitPython bundle
wget https://circuitpython.org/libraries/all_releases.atom -O all_releases.atom

# Step 2: Install Adafruit Blinka
sudo pip3 install --upgrade adafruit-blinka

# Step 3: Install the required libraries from the downloaded bundle
sudo pip3 install $(cat all_releases.atom | grep 'link href' | grep -Eo "(https|http)://[a-zA-Z0-9./?=_-]*tar.gz" | sed 's/\.tar\.gz//g')

# Step 4: Clean up the downloaded atom file
rm all_releases.atom