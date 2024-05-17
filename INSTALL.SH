#!/bin/bash

sudo mv /home/pi/NVIDIADriverUpdater/NVIDIADriverUpdater.service /etc/systemd/system/ && sudo systemctl daemon-reload
sudo apt install chromium-browser chromium-chromedriver -y
python3 -m pip install -r /home/pi/NVIDIADriverUpdater/requirements.txt --no-cache-dir
chmod +x -R /home/pi/NVIDIADriverUpdater/*