from selenium import webdriver
import os
import time


def driverFunc():
     #option = webdriver.ChromeOptions()

    chromeOptions = webdriver.ChromeOptions()
        
    #chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--disable-notifications')

    #chromeOptions.add_argument("window-size=1280,800")

    chromeOptions.add_argument('--disable-extensions')
    chromeOptions.add_argument("--user-data-dir="+os.getcwd()+"\\src\\UserData")

    chromeOptions.add_argument("--disable-plugins-discovery")
    chromeOptions.add_argument("--start-maximized")
    chromeOptions.add_argument('--ignore-certificate-errors')
    chromeOptions.add_argument('--ignore-ssl-errors')

    # For older ChromeDriver under version 79.0.3945.16
    chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
    chromeOptions.add_experimental_option('useAutomationExtension', False)
    # For ChromeDriver version 79.0.3945.16 or over
    chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=chromeOptions)
    driver.implicitly_wait(5)
    return driver

driver = driverFunc()
driver.get('https://www.olx.com.pk/')
time.sleep(100)