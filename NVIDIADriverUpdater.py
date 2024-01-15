# -*- coding: utf-8 -*-
# !/usr/bin/python3

import os
import json
import logging
import traceback
import urllib.request
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from Misc import get911, sendEmail


def setSelector(selectorElemId, value):
    """
    Set the value of a dropdown element identified by ID.

    Parameters:
    - selectorElemId (str): The ID of the dropdown element.
    - value (int): The value to be selected in the dropdown.

    Returns:
    None
    """
    selectElem = browser.find_element(By.ID, selectorElemId)
    select = Select(selectElem)
    select.select_by_value(str(value))
    selected_value = select.first_selected_option.get_attribute("text")
    logger.info(f"Selected {selected_value}")


def setSelectors():
    """
    Set values for multiple dropdown elements.

    Returns:
    None
    """
    # Find and set value for selProductSeriesType element
    selectorElemId = "selProductSeriesType"
    setSelector(selectorElemId, 3)

    # Find and set value for selProductSeries element
    selectorElemId = "selProductSeries"
    setSelector(selectorElemId, 74)

    # Find and set value for selProductFamily element
    selectorElemId = "selProductFamily"
    setSelector(selectorElemId, 909)

    # Find and set value for selOperatingSystem element
    selectorElemId = "selOperatingSystem"
    setSelector(selectorElemId, 57)

    # Find and set value for ddlDownloadTypeQnfOde element
    selectorElemId = "ddlDownloadTypeQnfOde"
    setSelector(selectorElemId, 1)

    # Find and set value for ddlLanguage element
    selectorElemId = "ddlLanguage"
    setSelector(selectorElemId, 2)


def main():
    """
    Automates the process of checking and downloading the latest NVIDIA graphics driver.

    This script uses a Selenium-driven browser to navigate to the official NVIDIA Drivers Page,
    checks for the latest version and release date, compares it with the saved information,
    and downloads the driver if a newer version is available. The script also updates and saves
    the version information for future comparisons.

    Note:
    Ensure that the required modules (logging, selenium, os, urllib, json) are properly installed,
    and the Selenium WebDriver is configured.

    Returns:
    None

    Raises:
    Any exceptions raised during the execution are propagated.
    """

    # Launch NVIDIA Drivers Page
    logger.info("Launch NVIDIA Drivers Page")
    browser.get("https://www.nvidia.com/download/index.aspx")

    # Set selectors
    setSelectors()

    # Search
    browser.find_element(By.CSS_SELECTOR, "#ManualSearchButtonTD > a > btn_drvr_lnk_txt").click()

    # Get latest version / release Date
    version = browser.find_element(By.ID, "tdVersion").text
    releaseDate = browser.find_element(By.ID, "tdReleaseDate").text
    logger.info(f"Version - {version} | Release Date - {releaseDate}")

    # Check for newer version
    if version == SAVED_INFO["version"]:
        logger.info(f"No new driver found")
        return

    # Goto Download Page
    browser.find_element(By.CSS_SELECTOR, "#lnkDwnldBtn > btn_drvr_lnk_txt").click()

    # Download driver
    downloadHREF = browser.find_element(By.CSS_SELECTOR, "#mainContent > table > tbody > tr > td > a").get_attribute("href")
    logger.info(f"Downloading {downloadHREF}")
    local_path = os.path.join(DRIVERS_FOLDER, os.path.basename(urllib.parse.urlparse(downloadHREF).path))
    urllib.request.urlretrieve(downloadHREF, local_path)
    logger.info(f"Downloaded to local file {local_path}")

    # Set new version
    SAVED_INFO["version"] = version

    # Save SAVED_INFO
    with open(SAVED_INFO_FILE, 'w') as outFile:
        json.dump(SAVED_INFO, outFile, indent=2)


if __name__ == '__main__':
    # Set Logging
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.abspath(__file__).replace(".py", ".log"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()])
    logger = logging.getLogger()

    logger.info("----------------------------------------------------")

    # Open the SAVED_INFO_FILE in read mode
    SAVED_INFO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_info.json")
    if not os.path.exists(SAVED_INFO_FILE):
        with open(SAVED_INFO_FILE, "w") as outFile:
            json.dump({"version": "0.0"}, outFile, indent=2)
    with open(SAVED_INFO_FILE) as inFile:
        SAVED_INFO = json.load(inFile)

    # Check if downloads folder exits
    DRIVERS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DRIVERS")
    os.makedirs(DRIVERS_FOLDER, exist_ok=True)

    # Create Selenium
    logger.info("Launch Browser")
    options = Options()
    options.add_argument('-headless')
    service = Service("/home/pi/geckodriver", log_output="/home/pi/geckodriver.log")
    browser = webdriver.Firefox(service=service, options=options)

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
        # sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        browser.close()
        logger.info("Close")
        logger.info("End")
