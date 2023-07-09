import os
import sys
import six
import pause
import argparse
import logging.config
import re
import time
import random
import json
import subprocess
import ssl
import undetected_chromedriver as uc
from selenium import webdriver
from dateutil import parser as date_parser
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC

ssl._create_default_https_context = ssl._create_unverified_context

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})


NIKE_HOME_URL = "https://www.nike.com/login"
SUBMIT_BUTTON_XPATH = "/html/body/div[2]/div/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/div/div/div[6]/button"
LOGGER = logging.getLogger()

def wait_until_visible(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    elif el_id:
        WebDriverWait(driver, duration, frequency).until(EC.visibility_of_element_located((By.ID, el_id)))

def wait_until_present(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.XPATH, xpath)))
    elif class_name:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    elif el_id:
        return WebDriverWait(driver, duration, frequency).until(EC.presence_of_element_located((By.ID, el_id)))

def wait_until_clickable(driver, xpath=None, class_name=None, el_id=None, duration=10000, frequency=0.01):
    if xpath:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elif class_name:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
    elif el_id:
        WebDriverWait(driver, duration, frequency).until(EC.element_to_be_clickable((By.ID, el_id)))

def run(driver, username, password, url):
    driver.maximize_window()

    try:
        login(driver=driver, username=username, password=password)
    except TimeoutException:
        LOGGER.info("Failed to login due to timeout. Retrying...")
    except Exception as e:
        if "net::ERR_PROXY_CONNECTION_FAILED" in str(e):
            LOGGER.error("Failed to connect to the proxy server")
        else:
            LOGGER.exception("Failed to login: " + str(e))
            six.reraise(Exception, e, sys.exc_info()[2])
    
    while True:
        try:
            try:
                LOGGER.info("Requesting page: " + url)
                driver.get(url)
                # Apri un nuovo pannello con lo stesso URL
                driver.execute_script("window.open('https://www.nike.com/login', 'new_window')")

                # Passa alla nuova finestra aperta
                driver.switch_to.window(driver.window_handles[-1])
            except TimeoutException:
                LOGGER.info("Page load timed out but continuing anyway")
                continue
                                                         
        except Exception:
                continue
    

def login(driver, username, password):
    try:
        LOGGER.info("Requesting page: " + NIKE_HOME_URL)
        driver.get(NIKE_HOME_URL)
    except TimeoutException:
        LOGGER.info("Page load timed out but continuing anyway")

    LOGGER.info("Waiting for login fields to become visible")
    wait_until_visible(driver=driver, xpath="//input[@id='username']")

    LOGGER.info("Entering username")
    email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))
    email_input.clear()
    email_input.send_keys(username)
    
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()
    
    LOGGER.info("Entering password")
    password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
    password_input.clear()
    password_input.send_keys(password)

    LOGGER.info("Clicco accedi")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    LOGGER.info("Logging in")
    signIn_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='SIGN IN']")))
    signIn_button.click()
    #driver.find_element_by_xpath("//input[@value='SIGN IN']").click()
    
    wait_until_visible(driver=driver, xpath="//a[@data-path='myAccount:greeting']", duration=5)
    
    LOGGER.info("Successfully logged in")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--driver-type", default="firefox", choices=("firefox", "chrome"))
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--webdriver-path", required=False, default=None)
    args = parser.parse_args()

    '''
    driver = None
    if args.driver_type == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--disable-blink-features=AutomationControlled')
        driver = webdriver.Firefox(options=firefox_options)
    '''

    #elif args.driver_type == "chrome":
    if args.driver_type == "chrome":
        options = uc.ChromeOptions()
        options.add_argument("--new-window")
        options.user_data_dir = "c:\\temp\\profile"

        driver = uc.Chrome(options = options) 
        wait = WebDriverWait(driver, 10)

    else:
        raise Exception("Specified web browser not supported, only Firefox and Chrome are supported at this point")
    
    
    run(driver=driver, username=args.username, password=args.password, url=args.url)
