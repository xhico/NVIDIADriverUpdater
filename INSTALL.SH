#!/bin/bash

sudo mv /home/pi/NVIDIADriverUpdater/NVIDIADriverUpdater.service /etc/systemd/system/ && sudo systemctl daemon-reload
python3 -m pip install -r /home/pi/NVIDIADriverUpdater/requirements.txt --no-cache-dir
chmod +x -R /home/pi/NVIDIADriverUpdater/*