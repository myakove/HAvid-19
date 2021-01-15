# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from datetime import time
from datetime import datetime
import time
import os
from os import path
from selenium.common.exceptions import InvalidSessionIdException
from loguru import logger

#### Setting ChromeOptions ####
def GetBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-maximized')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=360,640")
    options.add_argument('--ignore-certificate-errors')
    browser = webdriver.Chrome(executable_path='/opt/chromedriver-87.0.4280.88/chromedriver', options=options)
    return browser


def GetMobileBrowser():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--start-maximized')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=360,640")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    browser = webdriver.Chrome(executable_path='/opt/chromedriver-87.0.4280.88/chromedriver', options=options)
    return browser


##### Screenshot for mobile view - like webtop #####
def mobile_screenshot(browser,Image):
    if path.exists(Image):
        os.remove(Image)
    logger.info(browser)
    browser.set_window_size(380, 660) #the trick
    time.sleep(2)
    browser.save_screenshot(Image)
    browser.close()

#### Screenshot for regular view ####
def fullpage_screenshot(browser,Image):
    if path.exists(Image):
        os.remove(Image)
    logger.info(browser)
    browser.set_window_size(800, 600) #the trick
    time.sleep(2)
    browser.save_screenshot(Image)

#### Screenshot for regular view ####
def largepage_screenshot(browser,Image):
    if path.exists(Image):
        os.remove(Image)
    logger.info(browser)
    browser.set_window_size(800, 2070) #the trick
    time.sleep(2)
    browser.save_screenshot(Image)



#### Browser state logging ####
def log_browser(browser):
    logger.debug(f"Opened page. Url: {browser.current_url}, size: {len(browser.page_source)}")



def ping(browser, page):
    try:
        browser.get('https://bots.techblog.co.il/' + page + '.html')
    except:
        logger.info("Unable to ping")


def get_clear_browsing_button(browser):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return browser.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(browser, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    browser.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(browser, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(browser).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)