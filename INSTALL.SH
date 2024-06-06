#!/bin/bash

sudo apt install chromium-browser chromium-chromedriver -y
python3 -m venv /home/pi/NVIDIADriverUpdater/venv
source /home/pi/NVIDIADriverUpdater/venv/bin/activate
python3 -m pip install -r /home/pi/NVIDIADriverUpdater/requirements.txt --no-cache-dir
chmod +x -R /home/pi/NVIDIADriverUpdater/*
sudo mv /home/pi/NVIDIADriverUpdater/NVIDIADriverUpdater.service /etc/systemd/system/ && sudo systemctl daemon-reload

git clone https://github.com/xhico/Misc.git /home/pi/Misc
rsync -avp --progress /home/pi/Misc/Misc.py /home/pi/NVIDIADriverUpdater/venv/lib/python$(python3 -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")/site-packages/
rm -rf /home/pi/Misc/