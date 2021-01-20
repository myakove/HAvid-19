# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
import time
from argparse import ArgumentParser
import os
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from loguru import logger
# import temp_helpers as helpers
import helpers


def sign(userCode, sitePassword, Image):
    try:
        #### Starting Sign Proc ####
        logger.info("Starting process")
        logger.debug('-----------------------0000000000-----------------------------------------------')
        if not os.path.isdir(Image):
            os.mkdir(Image)

        image_path = os.path.join(Image, "pedagogy_statement.png")
        logger.debug(str(image_path))
        #### Initialize Browser ####
        browser = helpers.GetBrowser()
        browser.get("https://pedagogy.co.il/parentsmoe.html")
        start = '//*[@id="main-app"]/div/div/div/div[2]/div/div[1]/div[2]/a/div/img'
        time.sleep(2)
        helpers.fullpage_screenshot(browser, image_path)
        helpers.log_browser(browser)
        browser.find_element_by_xpath(start).click()
        time.sleep(2)
        helpers.fullpage_screenshot(browser, image_path)
        helpers.log_browser(browser)
        browser.find_element_by_xpath('//*["EduCombinedAuthUidPwd"]').click()
        time.sleep(2)
        helpers.fullpage_screenshot(browser, image_path)

        #### Logging In ####
        user = '//*[@id="HIN_USERID"]'
        siteAccess = '//*[@id="Ecom_Password"]'
        NextPhase = '//*[@id="loginButton2"]'
        browser.find_element_by_xpath(user).send_keys(userCode)
        browser.find_element_by_xpath(siteAccess).send_keys(sitePassword)
        browser.find_element_by_xpath(NextPhase).click()
        time.sleep(2)
        helpers.log_browser(browser)
        logger.info(f"Logged in")
        time.sleep(4)

        try:
            select = Select(browser.find_element_by_xpath("//select[*]"))
            for idx, user_select in enumerate(select.options):
                if "נא לבחור תלמיד/ה" in user_select.text:
                    continue

                try:
                    select.select_by_index(index=idx)
                    time.sleep(2)
                    browser.find_element_by_xpath('//*[@type="button"]').click()
                    logger.info(f"signed: {user_select.text}")
                except NoSuchElementException as ex:
                    if "נשלח" in browser.page_source:
                        logger.info(f"{user_select.text}: already signed")
                    else:
                        logger.error(str(ex))

                helpers.fullpage_screenshot(browser, f"{Image}/{user_select.text}.png")
        except Exception as ex:
            logger.error(str(ex))

        browser.close()
        return 1
    except Exception as ex:
        logger.info('#################################################################################################')
        logger.error(str(ex))
        browser.close()
        return 0


# if __name__ == '__main__':
#     sign(userCode="5472412", sitePassword="Liat2Ayala", Image="pedagogy_approval")
