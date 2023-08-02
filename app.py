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
import itertools
import imaplib
import email
import re
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
    time.sleep(1)
    driver.maximize_window()

    try:
        login(driver=driver, username=username, password=password)
    #except TimeoutException:
        #LOGGER.info("Failed to login due to timeout. Retrying...")
    except Exception as e:
        LOGGER.exception("Failed to login: " + str(e))
        six.reraise(Exception, e, sys.exc_info()[2])
    
    while True:
        try:
            try:
                LOGGER.info("Requesting page: " + url)
                driver.get(url)
                time.sleep(2)
            except TimeoutException:
                LOGGER.info("Page load timed out but continuing anyway")
                continue
                                                         
        except Exception as e:
                LOGGER.exception("Error while processing page: " + str(e))
                continue
    

def login(driver, username, password):

    desired_url = "https://www.nike.com/gb/"

    try:
        LOGGER.info("Requesting page: " + NIKE_HOME_URL)
        driver.get(NIKE_HOME_URL)
        '''
        LOGGER.info("Opening new panel")
        time.sleep(2)
        # Apri un nuovo pannello con lo stesso URL
        driver.execute_script("window.open();")
        time.sleep(1)
        # Passa alla nuova finestra aperta
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://www.nike.com/login")
        '''
        time.sleep(1.5)
    except TimeoutException:
        LOGGER.info("Page load timed out but continuing anyway")
    except Exception as e:
        LOGGER.exception("Error while loading login page: " + str(e))

    current_url = driver.current_url
    LOGGER.info("Current url: " + current_url)
    LOGGER.info("Desired url: " + desired_url)

    if not desired_url in current_url:

        LOGGER.info("Waiting for login fields to become visible")
        wait_until_visible(driver=driver, xpath="//input[@id='username']")

        LOGGER.info("Entering username")
        time.sleep(2)
        email_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))
        email_input.clear()

        for char in username:
            email_input.send_keys(char)
            time.sleep(0.25674) 
        
        time.sleep(1)
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()
        
        time.sleep(1)
        LOGGER.info("Entering password")
        try:
            time.sleep(2)
            password_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
        except TimeoutException:
            LOGGER.info("Opening new panel")
            time.sleep(2)
            # Apri un nuovo pannello con lo stesso URL
            driver.execute_script("window.open();")
            time.sleep(1.4)
            # Passa alla nuova finestra aperta
            driver.switch_to.window(driver.window_handles[1])
            login(driver, username, password)

        password_input.clear()
        time.sleep(2.5)

        for char in password:
            password_input.send_keys(char)
            time.sleep(0.2334222) 

        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()
        time.sleep(20)

        current_url = driver.current_url

        if desired_url in current_url:
            LOGGER.info("Successfully logged in")
            return
        else:

            # Connessione al server IMAP di Gmail
            imap_server = imaplib.IMAP4_SSL('imap.gmail.com', 993)

            # Effettua l'accesso all'account Gmail
            imap_server.login('sacchettisamuele@gmail.com', 'mzrhpmmmmhmkpabd')

            # Seleziona la casella di posta "INBOX"
            status, mailbox_data = imap_server.select('INBOX')

            if status == 'OK':
                # Criteri di ricerca per mittente e oggetto
                search_criteria = '(FROM "nike@notifications.nike.com" SUBJECT "Ecco il tuo codice monouso")'

                # Cerca le email corrispondenti ai criteri
                status, email_ids = imap_server.search(None, search_criteria)

                if status == 'OK':
                    # Leggi l'ultima email corrispondente
                    latest_email_id = email_ids[0].split()[-1]
                    status, email_data = imap_server.fetch(latest_email_id, '(RFC822)')
                    if status == 'OK':
                        raw_email = email_data[0][1]
                        email_message = email.message_from_bytes(raw_email)

                        # Esegui il parsing del messaggio email per ottenere il codice di verifica
                        email_body = ''
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                content_type = part.get_content_type()
                                if content_type == 'text/plain':
                                    try:
                                        email_body = part.get_payload(decode=True).decode('utf-8')
                                    except UnicodeDecodeError:
                                        email_body = part.get_payload(decode=True).decode('latin-1')
                                    break
                        else:
                            try:
                                email_body = email_message.get_payload(decode=True).decode('utf-8')
                            except UnicodeDecodeError:
                                email_body = email_message.get_payload(decode=True).decode('latin-1')

                        # Estrai l'ultimo codice di verifica utilizzando una espressione regolare
                        verification_code = re.findall(r'codice di verifica monouso che hai richiesto: (\d+)', email_body)
                        if verification_code:
                            latest_verification_code = verification_code[-1]
                            time.sleep(1)
                            LOGGER.info("Entering enamil verification code: " + latest_verification_code)
                            try:
                                time.sleep(2)
                                verificationCode_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='verificationCode']")))
                            except TimeoutException:
                                LOGGER.info("Opening new panel")
                                time.sleep(2)
                                # Apri un nuovo pannello con lo stesso URL
                                driver.execute_script("window.open();")
                                time.sleep(1.4)
                                # Passa alla nuova finestra aperta
                                driver.switch_to.window(driver.window_handles[1])
                                login(driver, username, password)

                            verificationCode_input.clear()
                            time.sleep(1.5)

                            for char in latest_verification_code:
                                verificationCode_input.send_keys(char)
                                time.sleep(0.4)  # Ritardo di 500 ms tra ogni carattere

                            time.sleep(1)

                        else:
                            print("Nessun codice di verifica trovato nella email")

            # Chiudi la connessione
            imap_server.close()
            imap_server.logout()

            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            submit_button.click()

            time.sleep(5)
            
            LOGGER.info("Successfully logged in")
    else:
        LOGGER.info("Just logged in")
        return


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
        options.add_argument("--disable-popup-blocking")
        options.user_data_dir = "c:\\temp\\profile"

        driver = uc.Chrome(options = options) 
        wait = WebDriverWait(driver, 10)

    else:
        raise Exception("Specified web browser not supported, only Firefox and Chrome are supported at this point")
    
    
    try:
        run(driver=driver, username=args.username, password=args.password, url=args.url)
    except Exception as e:
        LOGGER.exception("Error while running the script: " + str(e))
