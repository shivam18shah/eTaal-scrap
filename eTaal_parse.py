import json
import requests
from bs4 import BeautifulSoup as bs
import webbrowser
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing import Process
import pandas
import csv
import sys, traceback


webbrowser = webdriver.Chrome(executable_path = 'D:\Chrome Driver\chromedriver.exe')#, options=options)
loginurl = 'http://etaal.gov.in/etaal/ServiceDirectory.aspx'

# dataframe to store rows
df = pandas.DataFrame(columns = ['SI', 'State/Ministry', 'Service', 'Desc', 'URL'])

# appends rows to the csv
f = open("results.csv", "a")
df.to_csv(f)

def get_and_use_page(button_xpath):
    '''
    opens the link and clicks the default search button
    '''
    webbrowser.get(loginurl)
    btn = webbrowser.find_element_by_xpath(button_xpath)
    btn.click()


def get_and_use_link(index):
    '''
    opens the page number for fetching more results
    '''
    btn = webbrowser.find_element_by_link_text(index)
    btn.click()


def get_table_row_path(num):
    return webbrowser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr['+str(num)+']')


def get_child_data_path(num, ind):
    return webbrowser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr['+str(num)+']/td['+str(ind)+']')


def get_header_path(ind):
    return webbrowser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr[1]/th['+str(ind)+']')


def find_subsequent_links(ind):
    return webbrowser.find_element_by_xpath('//*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr[12]/td/table/tbody/tr/td['+ind+']/a')


def get_table_data_from_current_page():
    '''
    scrapes the data from all rows in the current page
    '''
    global df

    for i in range(2, 12):
        try:
            table_row_path = get_table_row_path(i)
        except:
            break
        li = []
        for j in [1, 2, 3, 4, 5]:
            try:
                child_path = get_child_data_path(i, j)
            except:
                webbrowser.close()
                return

            li.append(str(child_path.text))
        
        df.loc[i-2] = li
    df.to_csv(f, header=False)


get_and_use_page('//*[@id="ContentPlaceHolder1_Button1"]')
get_table_data_from_current_page()

general_path = '//*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr[12]/td/table/tbody/tr/td['
back_path = ']/a'

# links = "javascript:__doPostBack('ctl00$ContentPlaceHolder1$gdvSearch','Page$"
# links_tail = "')"
curr = 2
page = 0
while curr <= 12:
    page += 1
    try:
        path = general_path+str(curr)+back_path
        btn = webbrowser.find_element_by_xpath(path)
        btn.click()
        time.sleep(30)
    # webbrowser.implicitly_wait(100)
        get_table_data_from_current_page()
    except ElementClickInterceptedException:
        continue
    if btn.text == "...":
        print('Last page: ', page)
        curr = 2
    curr += 1

f.close()
webbrowser.close()

# //*[@id="ContentPlaceHolder1_gdvSearch"]/tbody/tr[12]/td/table/tbody/tr/td[3]/a