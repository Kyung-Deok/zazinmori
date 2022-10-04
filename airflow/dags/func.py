import math
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json, requests, xmltodict
import numpy as np
import pandas as pd
from datetime import datetime


def _get_news():
    tdy = datetime.today()
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.bigkinds.or.kr/v2/depthAnalysis/company.do?codeGroupId=corp_top300_list&page=1')
    time.sleep(5)
    lst = []
    for _ in range(1, 18):
        cpp = int(len(driver.find_elements(by=By.CSS_SELECTOR,
                                           value='#contents > section.spacial-page.company300-list > div > a')))
        for i in range(1, cpp + 1):
            time.sleep(3)
            driver.find_element(by=By.CSS_SELECTOR,
                                value=f'#contents > section.spacial-page.company300-list > div > a:nth-child({i})').send_keys(
                Keys.ENTER)
            time.sleep(10)
            npp = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='#newsTab01-news-results > li')))
            page_num = int(driver.find_element(by=By.CSS_SELECTOR, value='#newsTab01_paging > span.total').text)
            # for k in range(1, npp+1):
            for _ in range(1, page_num + 1):
                for k in range(1, npp + 1):
                    dic = dict()
                    corp_nn = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > p.k-name').text
                    category = driver.find_element(by=By.CSS_SELECTOR,
                                                   value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > div > dl > dd:nth-child(2)').text
                    time.sleep(3)
                    driver.find_element(by=By.CSS_SELECTOR,
                                        value=f'#newsTab01-news-results > li:nth-child({k}) > a').send_keys(Keys.ENTER)
                    time.sleep(3)
                    title = driver.find_element(by=By.CSS_SELECTOR,
                                                value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > h1').text
                    keyword = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item1 > div > span').text
                    date = driver.find_element(by=By.CSS_SELECTOR,
                                               value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item1 > ul > li:nth-child(1)').text
                    content = driver.find_element(by=By.CSS_SELECTOR,
                                                  value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-body').text
                    url = driver.find_element(by=By.CSS_SELECTOR,
                                              value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item2 > div:nth-child(1) > button:nth-child(1)').get_attribute(
                        'onclick').split('=')[1].replace("'", "")

                    dic['corp_nn'] = corp_nn
                    dic['category'] = category
                    dic['title'] = title
                    dic['keyword'] = keyword
                    dic['date'] = date
                    dic['content'] = content
                    dic['url'] = url

                    lst.append(dic)
                    time.sleep(5)

                    driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > button').send_keys(
                        Keys.ENTER)
                    time.sleep(3)

                driver.find_element(by=By.CSS_SELECTOR, value='#newsTab01_paging > a.page-next.page-link').send_keys(
                    Keys.ENTER)
                time.sleep(5)

        driver.find_element(by=By.CSS_SELECTOR,
                            value='#contents > section.spacial-page.sp-pagenavi.company300-nav > div > div > div:nth-child(6) > a').send_keys(
            Keys.ENTER)

    driver.close()
    df = pd.DataFrame(lst)
    df.to_csv(f"/home/ubuntu/update/news{tdy}.csv", index=False, encoding="utf-8-sig")

def _get_total():
    tdy = datetime.today()
    df_8digit = pd.read_csv('corp_info_add.csv', dtype={'corp_code': 'string'})
    print(df_8digit.iloc[0, 0])
    code_list = list(np.array(df_8digit['corp_code'].tolist()))
    print(code_list[0])
    print(code_list)

    lst = []
    for code in code_list:
        try:
            url = 'https://opendart.fss.or.kr/api/company.xml?crtfc_key=e7c46b16d0b9cb8676f649882a4501285f5b77cb&corp_code=' + code
            response = requests.get(url)
            content = response.content
            parsing = xmltodict.parse(content)
            dic = parsing['result']

            if dic['status'] != '000':
                print(f'{code} : ' + dic['message'])
                pass
            else:
                lst.append(dic)

        except:
            print(f'{code}로 ' + dic['message'])
        print(f'***** LOOP{code} DONE ****')

    df_info = pd.DataFrame(lst)
    df_info.to_csv(f"/home/ubuntu/update/total{tdy}.csv", index=False, encoding="utf-8-sig")

def _get_fin():
    tdy = datetime.today()
    df_8digit = pd.read_csv('corp_code_8digit.csv', dtype={'corp_code': 'string'})
    code_list = list(np.array(df_8digit['corp_code'].tolist()))
    for code in code_list[:20000]:
        lst = []
        try:
            url = f'https://opendart.fss.or.kr/api/fnlttSinglAcnt.xml?crtfc_key=015205a39ab61396ba4de99e4fc7a5c90b778641&corp_code={code}&bsns_year=2021&reprt_code=11011'
            response = requests.get(url, verify=False)
            content = response.content
            parsing = xmltodict.parse(content)
            try:
                dic = parsing['result']['list']
                lst.extend(dic)
                df = pd.DataFrame(lst)
                df.drop(['fs_div', 'fs_nm', 'frmtrm_nm', 'sj_div', 'sj_nm', 'frmtrm_dt', 'thstrm_nm', 'thstrm_dt',
                         'frmtrm_amount',
                         'bfefrmtrm_nm', 'bfefrmtrm_dt', 'bfefrmtrm_amount', 'ord', 'currency'], axis=1, inplace=True)
                sr1 = df.loc[2]
                sr2 = df.loc[5]
                sr3 = df.loc[8]
                sr4 = df.loc[9]
                sr5 = df.loc[10]
                sr6 = df.loc[12]

                sr = pd.concat([sr1, sr2, sr3, sr4, sr5, sr6])
                sr = sr.drop_duplicates()
                df_add = sr.to_frame().T

                df_start = pd.concat([df_start, df_add])
            except:
                pass
        except:
            print(f'{code}번에서 에러발생')

    df_start.to_csv(f'/home/ubuntu/update/findata{tdy}.csv', index=False, encoding="utf-8-sig")


def _get_cvletter():
    lst = list()
    tdy = datetime.today()
    page_num = int(math.trunc(7281 / 20) + 1)
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.jobkorea.co.kr/Starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=0&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page=341')
    time.sleep(30)
    for _ in range(2):
        for u in range(2, 12):
            for n in range(1, 21):
                try:
                    dic = dict()
                    corp_nm = driver.find_element(by=By.CSS_SELECTOR,
                                                  value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > a > span.titTx').text
                    employment_date = driver.find_element(by=By.CSS_SELECTOR,
                                                          value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(1)').text
                    new_or_exp = driver.find_element(by=By.CSS_SELECTOR,
                                                     value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(2)').text
                    job = driver.find_element(by=By.CSS_SELECTOR,
                                              value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > span.linkArray > span:nth-child(3)').text
                    time.sleep(3)
                    driver.find_element(by=By.CSS_SELECTOR,
                                        value=f'ul.selfLists > li:nth-child({n}) > div.txBx > p.tit > a').send_keys(
                        Keys.ENTER)
                    time.sleep(3)

                    num = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='div.selfQnaWrap > dl.qnaLists > dt')))
                    dic['corp_nm'] = corp_nm
                    dic['employment_date'] = employment_date
                    dic['new_or_exp'] = new_or_exp
                    dic['job'] = job
                    num = int(
                        len(driver.find_elements(by=By.CSS_SELECTOR, value='div.selfQnaWrap > dl.qnaLists > dt'))) * 2
                    for j in range(1, num + 1):
                        if int(j) % 2 != 0:
                            c = j // 2 + 1
                            question = driver.find_element(by=By.CSS_SELECTOR,
                                                           value=f'div.selfQnaWrap > dl.qnaLists > dt:nth-child({j}) > button > span.tx').text
                            dic['Q' + str(c)] = question
                        else:
                            d = j // 2
                            if j >= 6:
                                time.sleep(3)
                                driver.find_element(by=By.CSS_SELECTOR,
                                                    value=f'div.selfQnaWrap > dl.qnaLists > dt:nth-child({j - 1}) > button').send_keys(
                                    Keys.ENTER)
                                time.sleep(5)
                                answer = driver.find_element(by=By.CSS_SELECTOR,
                                                             value=f'div.selfQnaWrap > dl.qnaLists > dd:nth-child({j}) > div.tx').text
                                dic['A' + str(d)] = answer
                            else:
                                answer = driver.find_element(by=By.CSS_SELECTOR,
                                                             value=f'div.selfQnaWrap > dl.qnaLists > dd:nth-child({j}) > div.tx').text
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
                driver.find_element(by=By.CSS_SELECTOR,
                                    value=f'div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > ul > li:nth-child({u}) > a').send_keys(
                    Keys.ENTER)
                time.sleep(15)
            else:
                time.sleep(3)
                driver.find_element(by=By.CSS_SELECTOR,
                                    value='div.stContainer > div.starListsWrap.ctTarget > div.tplPagination > p:nth-child(3) > a').send_keys(
                    Keys.ENTER)
                time.sleep(15)

    driver.close()

    df = pd.DataFrame(lst)
    df.to_csv(f"/home/ubuntu/update/cvletter{tdy}.csv", index=False, encoding="utf-8-sig")