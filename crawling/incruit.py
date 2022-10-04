import math
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import pandas as pd

lst = list()
page_num = int(math.trunc(7281/20) + 1)
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://people.incruit.com/resumeguide/rsmpdslist.asp?pds1=1&pds2=11&page=1')
time.sleep(30)
# PAGE당 25개

lst = list()
# div.section_layout > div.section_layout > div.bbslist_resumeform > ul > li:nth-child(1) > a
for _ in range(22):
    for i in range(1, 26):
        try:
            dic = dict()
            time.sleep(3)
            driver.find_element(by=By.CSS_SELECTOR, value=f'div.section_layout > div.section_layout > div.bbslist_resumeform > ul > li:nth-child({i}) > a').send_keys(Keys.ENTER)
            time.sleep(5)
            corp_nm = driver.find_element(by=By.CSS_SELECTOR, value='div.section_layout > div:nth-child(2) > div > div.conts > div > h2 > strong > a').text
            content = driver.find_element(by=By.CSS_SELECTOR, value='div.section_layout > div.fullbg_body > div > div > div.bbsview_detail_text').text
            dic['corp_nm'] = corp_nm
            dic['content'] = content
            lst.append(dic)
            time.sleep(2)
            driver.back()
            time.sleep(2)
        except:
            time.sleep(2)
            driver.back()
            time.sleep(2)

    time.sleep(3)
    driver.find_element(by=By.CSS_SELECTOR, value='div.section_layout > div.section_layout > div.bbslist_resumeform > p > a.next').send_keys(Keys.ENTER)
    time.sleep(8)

df = pd.DataFrame(lst)
df.to_csv("crawling_ic.csv", index=False, encoding="utf-8-sig")

