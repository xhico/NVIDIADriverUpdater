# -*- coding: utf-8 -*-
# !/usr/bin/python3

import json
import logging
import os
import traceback

from Misc import sendEmail
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


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
    select.first_selected_option.get_attribute("text")


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
    version = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "tdVersion"))).text
    releaseDate = browser.find_element(By.ID, "tdReleaseDate").text
    logger.info(f"Saved Version - {SAVED_INFO['version']}")
    logger.info(f"Live Version - {version}")
    logger.info(f"Release Date - {releaseDate}")

    # Check for newer version
    if version == SAVED_INFO["version"] or version == "" or releaseDate == "":
        logger.info(f"No new driver found")
        return

    # Found new Driver
    logger.warning("Found new Driver")

    # Goto Download Page
    browser.find_element(By.CSS_SELECTOR, "#lnkDwnldBtn > btn_drvr_lnk_txt").click()

    # Download driver
    downloadHREF = browser.find_element(By.CSS_SELECTOR, "#dnldBttns > table > tbody > tr > td:nth-child(1) > a").get_attribute("href")
    logger.info(f"Downloads - {downloadHREF}")

    # Send Email
    sendEmail("NVIDIA Driver Update", f"Version: {version}\nRelease Date: {releaseDate}\nDownload: {downloadHREF}")

    # Set new version
    SAVED_INFO["version"] = version
    SAVED_INFO["releaseDate"] = releaseDate

    # Save SAVED_INFO
    with open(SAVED_INFO_FILE, "w") as outFile:
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

    # Create Selenium
    logger.info("Launch Browser")
    Options = Options()
    Options.add_argument("-headless")
    Options.binary_location = "/usr/bin/brave-browser"
    Service = Service("/usr/bin/chromedriver")
    browser = webdriver.Firefox(options=Options, service=Service)

    try:
        main()
    except Exception as ex:
        logger.error(traceback.format_exc())
        sendEmail(os.path.basename(__file__), str(traceback.format_exc()))
    finally:
        browser.close()
        logger.info("Close")
        logger.info("End")
