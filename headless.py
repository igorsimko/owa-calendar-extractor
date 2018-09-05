from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *

import requests
import os
import json
import time

# month is from <span class="_cb_p2 _cb_q2 ms-font-weight-regular ms-font-color-themePrimary label">
def parse_month(month):
    if "JAN" in month:
        return 1
    if "FEB" in month:
        return 2
    if "MAR" in month:
        return 3
    if "APR" in month:
        return 4
    if "MÁJ" in month:
        return 5
    if "JÚN" in month:
        return 6
    if "JÚL" in month:
        return 7
    if "AUG" in month:
        return 8
    if "SEP" in month:
        return 9
    if "OKT" in month:
        return 10
    if "NOV" in month:
        return 11
    if "DEC" in month:
        return 12

    return -1

def parse_date(date_string):
    date_split = date_string.split(' ')
    day = date_split[0].replace('.','')
    month = parse_month(date_split[1])
    year = date_split[2]
    return str(month) + "/" + str(day) + "/" + str(year)

def parse_time(time_string):
    time_split = time_string.split(' ')
    hours = time_split[0]
    minutes = 0
    if len(time_split) > 2:
        minutes = time_split[2]
    return str(hours) + ":" + str(minutes)


# instantiate a chrome options object so you can set the size and headless preference
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

# download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads and put it in the
# current directory
chrome_driver = os.getcwd() +"\\chromedriver.exe"

driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
driver.get("https://<<YOUR OWA ADDRESS>>")

try:
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys("<<YOUR USERNAME>>")
    password.send_keys("<<YOUR PASSWORD>>")

    driver.find_element_by_class_name("signinbutton").click()

    wait = WebDriverWait(driver, 10)

    menu_item_calendar_element=wait.until(ec.presence_of_element_located((By.XPATH,'//button[@data-pi="1"]')))
    driver.find_element_by_xpath('//button[@data-pi="1"]').click()

    calendar_page_element=wait.until(ec.presence_of_element_located((By.CLASS_NAME, '_ce_p')))

    calendar = []
    key_days = []
    # get days divs
    for day in driver.find_elements_by_class_name('_ce_P1'):
        print("parsing day...")
        try:
            day.click()
            # get day/month span. see parse_month.
            cur_date = driver.find_elements_by_class_name('_cb_p2')[0].text
            print(parse_date(cur_date))
            events = []
            # get events divs after click on day with calendar events
            for event in driver.find_elements_by_class_name('_cb_E'):
                calendar_event = []
                # itterate over events in one day
                for span in event.find_elements_by_tag_name('span'):
                    # if span contains hours text then parse as time.
                    # hours text in slovak is 'hodin'. In english version of OWA change text to 'hour'
                    if "hodin" in span.text:
                        calendar_event.append(parse_time(span.text))
                    else:
                        calendar_event.append(span.text)
                events.append(calendar_event[:4])
            
            if parse_date(cur_date) not in key_days:
                calendar.append({'date': parse_date(cur_date), 'events': events})
                key_days.append(parse_date(cur_date))

        finally:
            pass
    
    json_string = json.dumps(calendar)

    req = requests.get("https://script.google.com/macros/s/<<YOUR GOOGLE APP SCRIPT ID>>/exec?callback=doGet&data=" + json_string)
    print(json_string)

    # capture the screen
    driver.get_screenshot_as_file("capture.png")
    driver.quit()
except (NoSuchElementException, TimeoutException) as e:
    print(e)
    driver.get_screenshot_as_file("error.png")
finally:
    driver.quit()

