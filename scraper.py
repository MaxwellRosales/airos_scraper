import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import logging
import time

# SYSTEM PARAMETERS
IP                     = '192.168.1.20' # TODO: Check if this is the correct IP
USERNAME               = 'GO' # TODO: Change to correct username and password
PASSWORD               = 'BLUE'
LOGGING_FILENAME       = "signal_log.txt"
RECORDING_FREQUENCY_HZ = 1

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

# TODO: Add error handling
def log_into_airos() -> None:
    global driver 

    # Create a webdriver without a GUI to fetch data from
    print('Starting ChromeDriver...')
    driver = webdriver.Chrome(options=chrome_options)
    print('Driver started.')

    print('Logging in...')
    driver.get(f'http:{IP}/login.cgi')

    user_form = driver.find_element(By.ID, 'username')
    pass_form = driver.find_element(By.ID, 'password')

    user_form.send_keys(USERNAME)
    pass_form.send_keys(PASSWORD)
    
    submit = driver.find_element(By.XPATH, "//input[@value='Login']")
    submit.click()


def fetch_signal() -> int:
    driver.get(f'http:{IP}/signal.cgi')
    return json.loads(driver.find_element(By.TAG_NAME ,'body').text)['signal']


def main()-> None: 
    log_into_airos()
    logging.basicConfig(filename=LOGGING_FILENAME,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logging.info("\nSTARTING LOG\n")
    while True:
        scraper_signal = fetch_signal()
        print(scraper_signal)
        logging.info(f"{scraper_signal}")

        time.sleep(RECORDING_FREQUENCY_HZ)


if __name__ == '__main__':
    main()


