from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from twilio.rest import Client
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import *


def main():

    url = 'https://egov.uscis.gov/casestatus/landing.do'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    click(url)


def click(url):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    global driver
    driver = webdriver.Chrome(PATH)

    driver.get(url)
    time.sleep(0.5)

    prefix = "MSC"
    # October 22, 2020 case received date 2190382800
    start_range = 2190379500
    end_range =   2190382800
    case_total = 0
    for i in range(start_range, end_range):
        try:
            element = WebDriverWait(driver, 5000).until(
                EC.element_to_be_clickable((By.XPATH, ".//input[@value='CHECK STATUS' and @type='submit']"))
            )
            case_number = prefix + str(i)
            case_number_input = driver.find_element_by_id("receipt_number")
            case_number_input.send_keys(case_number)

            element.click()

            if check_current_status() is True:
                case_total += 1
        except:
            print("Page Not Fully Loaded Yet")
            driver.sendKeys(Keys.RETURN)
        time.sleep(0.5)
    file = open("case_data.txt", "w")
    file.write("Case Number Starting From: " + prefix + str(start_range) + " to " + prefix + str(end_range))
    file.write("\n")
    file.write("\n")
    for data in map_pair:
        file.write(data)
        file.write("\n")
        file.write("Number of Cases: " + str(map_pair[data]))
        file.write("\n")
        file.write("Percentage of Total: " + str((map_pair[data] / case_total) * 100) + "%")
        file.write("\n")
        file.write("\n")
    file.write("Total of " + str(case_total) + " I-485 cases crawled")
    file.close()
    # send_message()


map_pair = {}


def check_current_status():
    if "I-485" not in driver.page_source:
        return False
    grab_date = driver.find_element(By.CSS_SELECTOR, 'div.rows.text-center p').text
    case_date = grab_date.split()[:5]
    date_list = []
    for i in case_date:
        if i != 'As' and i != 'of' and i != 'On' and i != 'we':
            i = str(i)
            i = i.replace(',', '')
            date_list.append(i)
    # print(date_list)
    current_status = driver.find_element_by_css_selector('h1').text
    # print(current_status)
    if current_status not in map_pair:
        map_pair[current_status] = 1
    else:
        map_pair[current_status] = map_pair[current_status] + 1
    print(map_pair)
    return True


def send_message():
    account_sid = "AC8452c9347dfd05685992f192457ee9a9"
    auth_token = "22f70069ce42ac448ffd93ad2ca2dca5"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+12534098910",
        from_="+17868286841",
        body="Message From Triton Server: Crawling Has Finished"
    )
    print(message.sid)


if __name__ == "__main__":
    main()
