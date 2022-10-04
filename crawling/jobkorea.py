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
driver.get('https://www.jobkorea.co.kr/Starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page=341')
time.sleep(30)
for _ in range(2):
    for u in range(2, 12):
        # container > div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > ul > li:nth-child(8) > a
        # container > div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > ul > li:nth-child(10) > a
        for n in range(1, 21):
            try:
                dic = dict()
                corp_nm = driver.find_element(by=By.CSS_SELECTOR, value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > a > span.titTx').text
                employment_date = driver.find_element(by=By.CSS_SELECTOR, value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(1)').text
                new_or_exp = driver.find_element(by=By.CSS_SELECTOR, value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(2)').text
                job = driver.find_element(by=By.CSS_SELECTOR, value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(3)').text
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR, value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > a').send_keys(Keys.ENTER)
                time.sleep(3)

                num = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='div.selfQnaWrap > dl.qnaLists > dt')))
                dic['corp_nm'] = corp_nm
                dic['employment_date'] = employment_date
                dic['new_or_exp'] = new_or_exp
                dic['job'] = job
                num = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='div.selfQnaWrap > dl.qnaLists > dt')))*2
                for j in range(1, num+1):
                    if int(j)%2!=0:
                        c = j//2 + 1
                        question = driver.find_element(by=By.CSS_SELECTOR, value=f'div.selfQnaWrap > dl.qnaLists > dt:nth-child({j}) > button > span.tx').text
                        dic['Q' + str(c)] = question
                    else:
                        d = j//2
                        if j>=6:
                            time.sleep(3)
                            driver.find_element(by=By.CSS_SELECTOR, value=f'div.selfQnaWrap > dl.qnaLists > dt:nth-child({j-1}) > button').send_keys(Keys.ENTER)
                            time.sleep(5)
                            answer = driver.find_element(by=By.CSS_SELECTOR, value=f'div.selfQnaWrap > dl.qnaLists > dd:nth-child({j}) > div.tx').text
                            dic['A' + str(d)] = answer
                        else:
                            answer = driver.find_element(by=By.CSS_SELECTOR, value=f'div.selfQnaWrap > dl.qnaLists > dd:nth-child({j}) > div.tx').text
                            dic['A' + str(d)] = answer

                lst.append(dic)
                time.sleep(3)
                driver.back()
                time.sleep(3)
            except:
                time.sleep(3)
                driver.back()
                time.sleep(3)

        if u != 11:
            time.sleep(3)
            driver.find_element(by=By.CSS_SELECTOR, value=f'div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > ul > li:nth-child({u}) > a').send_keys(Keys.ENTER)
            time.sleep(15)
        else:
            time.sleep(3)
            driver.find_element(by=By.CSS_SELECTOR, value='div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > p:nth-child(3) > a').send_keys(Keys.ENTER)
            time.sleep(15)


driver.close()

df = pd.DataFrame(lst)
df.to_csv("crawling_jk8.csv", index=False, encoding="utf-8-sig")





