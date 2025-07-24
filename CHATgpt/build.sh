#!/bin/bash
apt-get update && apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3-dev libxss1 libappindicator1 libindicator7 libu2f-udev fonts-liberation libasound2 libatk-bridge2.0-0 libgtk-3-0
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install
