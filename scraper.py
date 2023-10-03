import sys 
sys.path.append('../')

from credentials import *

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import json
import logging
import time

# SYSTEM PARAMETERS
WEBSITE_URL              = f"https:{IP}/" # DO NOT CHANGE THIS
LOADING_DELAY            = 10 # Time to wait for the website to load
LOGGING_FILENAME         = "Ubiquiti_rssi_log.txt"
RECORDING_PERIOD_SECONDS = 1

# OPTIONS FOR THE WEBDRIVER ON START UP
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument("--headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features")
chrome_options.accept_insecure_certs = True

# TODO: Add error handling
def get_airos_page() -> None:
    global driver 

    # Create a webdriver without a GUI to fetch data from
    print('Starting ChromeDriver...')
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print('Driver started.')

    # TRY GETTING THE WEBSITE THROUGH THE SCRAPER
    try:
        login_page = WEBSITE_URL + 'login.cgi'
        print(f'Going to {login_page}')
        driver.get(login_page)
    except:
        with Exception as e:
            print("Came across an exception when fetching the website!\n")
            print(e)
            pass

def log_into_airos() -> None:
    # SEND PASSWORD AND USERNAME TO THE AIROS PAGE
    try:
        user_form = WebDriverWait(driver, LOADING_DELAY).until(EC.presence_of_element_located((By.ID, 'loginform-username')))
        pass_form = WebDriverWait(driver, LOADING_DELAY).until(EC.presence_of_element_located((By.ID, 'loginform-password')))
        print( "Loaded Air OS page")
    except TimeoutException:
        print( "Air OS page was unable to load.")

    # TODO ADD ERROR HANDLING HERE
    user_form.send_keys(USERNAME)
    pass_form.send_keys(PASSWORD)

    submit = driver.find_element(By.XPATH, "//input[@value='Login']")
    submit.click()

    return None

# KEYS FROM THIS PAGE
# dict_keys(['chain_names', 'host', 'genuine', 'services', 'firewall', 'portfw', 'wireless', 'interfaces', 'provmode', 'ntpclient', 'unms'])
def fetch_status() -> int:
    status_page = WEBSITE_URL + 'status.cgi'
    driver.get(status_page)
    json_data = json.loads(driver.find_element(By.TAG_NAME ,'body').text)
    return json_data

def fetch_airviewdata() -> int:
    airview_page = WEBSITE_URL + 'airviewdata.cgi'
    driver.get(airview_page)
    json_data = json.loads(driver.find_element(By.TAG_NAME ,'body').text)
    return json_data

def main()-> None: 
    get_airos_page()
    log_into_airos()

    logging.basicConfig(filename=LOGGING_FILENAME,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    
    # MAIN LOOP FOR FETCHING DATA
    logging.info("\nSTARTING LOGGING\n")
    time.sleep(1)

    while True:
        scraper_signal  = fetch_status()
        gs_sta = scraper_signal["wireless"]["sta"][0]["rssi"]
        logging.info(f"{gs_sta}")
        time.sleep(RECORDING_PERIOD_SECONDS)

if __name__ == '__main__':
    main()


