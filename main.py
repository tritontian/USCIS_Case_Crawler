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
from tkinter.filedialog import askopenfilename
import easygui
from PIL import ImageTk, Image

url = 'https://egov.uscis.gov/casestatus/landing.do'
window = tk.Tk()
start_var = tk.StringVar()
end_var = tk.StringVar()
out_var = tk.StringVar()
button_var = tk.StringVar()


def main():
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    build_gui()


def build_gui():
    select_category()
    window.title("USCIS Case Status Crawler")
    window.resizable(False, False)
    window.config(bg="#1c3464")
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    window.geometry('+%d+%d' % (x, y))
    frame1 = Frame(window, width=400, height=260, bg="white")
    frame1.config(bg="#1c3464")
    frame1.grid(row=0, column=0)

    my_img = Image.open("uscis.png")
    my_img = my_img.resize((200, 180), Image.ANTIALIAS)
    pic = ImageTk.PhotoImage(my_img)
    pic_label = Label(frame1, image=pic, bg="#1c3464")
    pic_label.grid(row=0, column=0, sticky=NW)

    menu = Menu(window)

    window.config(menu=menu)
    menu.add_cascade(label="Help", command=show_info)

    start_range_label = Label(frame1, text="Case Range Start: ", bg="#1c3464", fg="white", font=("Georgia", 15))
    start_range_label.grid(row=2, column=0, sticky=W)

    start_entry = Entry(frame1, textvariable=start_var, width=20)
    start_entry.grid(row=2, column=1, sticky=W)
    eg_start = Label(frame1, text="eg: MSC2190370000", bg="#1c3464", fg="grey", font=("Trattatello",12))
    eg_start.grid(row=3, column=1, sticky=W)

    end_label = Label(frame1, text="Case Range End: ", bg="#1c3464", fg="white", font=("Georgia", 15))
    end_label.grid(row=4, column=0, sticky=W)
    end_entry = Entry(frame1, textvariable=end_var, width=20)
    end_entry.grid(row=4, column=1, sticky=W)
    eg_end = Label(frame1, text="eg: MSC2190370005", bg="#1c3464", fg="grey", font=("Trattatello", 12))
    eg_end.grid(row=5, column=1, sticky=W)

    global button
    button = tk.Button(frame1, text="Choose directory", relief=RAISED, width=20,
                       command=choose_file, bg="light grey", font=("Arial", 12))
    button.grid(row=6, column=1, sticky=E)

    msg_label = Label(frame1, textvariable=out_var, width=50, bg="#1c3464", fg="red", font=("Impact", 12))
    msg_label.grid(row=7, column=0)

    window.mainloop()


def select_category():
    # easygui.egdemo()
    message = "Select the category you want to look up for: \n" \
              "For more detail, you can visit: https://www.uscis.gov/forms/all-forms"
    title = "Select Case Category: "
    choice_list = ["AR-11", "G-28", "G-1041", "G-1145", "I-9", "I-90",
                   "I-129", "I-130", "I-131", "I-134", "I-140",
                   "I-192", "I-193", "I-407", "I-485", "I-526", "I-539",
                   "I-600", "I-698", "I-730", "I-765", "I-800", "I-817",
                   "I-824", "I-907", "I-914", "I-918", "I-941", "I-942",
                   "I-944", "N-300", "N-400", "N-426", "N-565", "N-648"]
    global case_category
    pos = int(window.winfo_screenwidth() * 0.5), int(window.winfo_screenheight() * 0.2)

    rootWindowPosition = "+%d+%d" % pos
    easygui.rootWindowPosition = rootWindowPosition
    case_category = easygui.choicebox(message, title, choice_list)


def choose_file():
    global text_entry_start
    global text_entry_end
    text_entry_start = str(start_var.get())
    text_entry_end = str(end_var.get())

    if len(text_entry_start) != 13 or len(text_entry_end) != 13:
        out_var.set("Invalid input: case number must be 13 digits")
        return
    out_var.set("")
    # easygui.msgbox("where you want to store retrieved data?", ok_button="File")
    global file_name
    file_name = easygui.filesavebox()

    button.config(text="Run", command=click)
    return file_name


def show_info():
    does_accept = easygui.indexbox("This program will retrieve data from the USCIS website, simply as \"Crawler\".\n"
                                   " Data retrieved will be stored into local directory where user can choose.\n"
                                   "  This program is ONLY for individual use NOT for commercial purpose.", "Info",
                                   ["Accept"])
    return does_accept


def click():

    print(text_entry_start)
    print(text_entry_end)
    prefix = text_entry_start[0:3]
    start_range = int(text_entry_start[3:])
    end_range = int(text_entry_end[3:])

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    global driver
    driver = webdriver.Chrome(PATH)
    driver.get(url)
    time.sleep(0.5)

    case_total = 0
    for i in range(start_range, end_range + 1):
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

    file = open(file_name + ".txt", "w")
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
    file.write("Total of " + str(case_total) + " " + str(case_category) + " cases crawled")
    file.close()
    #User can decide to receive a message notification after the application has finished
    # send_message()


map_pair = {}


def check_current_status():
    print(case_category)
    if str(case_category) not in driver.page_source:
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

# This uses Twilio API to send message, register an account before using
# For More Info, Visit: https://www.twilio.com/docs/sms/quickstart/python

# def send_message():
#     account_sid = "register your personal account serial id"
#     auth_token = "register your personal token"
#
#     client = Client(account_sid, auth_token)
#
#     message = client.messages.create(
#         to="Your Recipient Number",
#         from_="Virtual Number From Twilio",
#         body="Message From Triton Server: Crawling Has Finished"
#     )
#     print(message.sid)


if __name__ == "__main__":
    main()

