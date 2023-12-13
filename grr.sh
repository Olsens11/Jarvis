#!/bin/bash

# Step 1: Install Adafruit Blinka
sudo pip3 install --upgrade adafruit-blinka

# Step 2: Download and install the latest Adafruit CircuitPython bundle
LATEST_RELEASE=$(curl -s https://api.github.com/repos/adafruit/Adafruit_CircuitPython_Bundle/releases/latest | grep "tag_name" | cut -d'"' -f4)
sudo pip3 install https://github.com/adafruit/Adafruit_CircuitPython_Bundle/archive/$LATEST_RELEASE.tar.gz

# Step 3: Reboot the Raspberry Pi
sudo reboot
