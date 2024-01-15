# NVIDIADriverUpdater

## Automates the process of checking and downloading the latest NVIDIA graphics driver.

## Saved Info

Loads Saved Info from local file (Example bellow)

```
{
  "version": "R535 U9 (537.99)  WHQL"
}
```

## Installation

```
python3 -m pip install -r /home/pi/NVIDIADriverUpdater/requirements.txt --no-cache-dir
sudo apt install firefox-esr -y
```

## Usage

Manual

```
python3 NVIDIADriverUpdater.py
```

Crontab (every 60 mins)

```
0 */1 * * * python3 /home/pi/NVIDIADriverUpdater/NVIDIADriverUpdater.py
```

