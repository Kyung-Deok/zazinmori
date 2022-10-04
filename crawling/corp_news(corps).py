import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from multiprocessing import Pool, Manager
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from random import random
import pandas as pd


def open_browser(name, lst):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(f'https://www.bigkinds.or.kr/v2/depthAnalysis/company/{name}/depthAnalComView.do?codeGroupNo=300')
    time.sleep(7)
    npp = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='#newsTab01-news-results > li')))
    page_num = int(driver.find_element(by=By.CSS_SELECTOR, value='#newsTab01_paging > span.total').text)
    for p in range(1, page_num+1):
        print(f'*******LOOP: {p}*******')
        for k in range(1, npp + 1):
            dic = dict()
            corp_nn = driver.find_element(by=By.CSS_SELECTOR, value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > p.k-name').text
            category = driver.find_element(by=By.CSS_SELECTOR, value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > div > dl > dd:nth-child(2)').text
            try:
                wait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#newsTab01-news-results > li:nth-child({k}) > a'))).send_keys(Keys.ENTER)
                time.sleep(1 + random())
                title = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > h1').text
                keyword = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item1 > div > span').text
                date = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item1 > ul > li:nth-child(1)').text
                content = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-body').text
                url = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal > div > div > div.modal-body > div > div.news-view-head > div.item2 > div:nth-child(1) > button:nth-child(1)').get_attribute('onclick').split('=')[1].replace("'", "")

                dic['corp_nn'] = corp_nn
                dic['category'] = category
                dic['title'] = title
                dic['keyword'] = keyword
                dic['date'] = date
                dic['content'] = content
                dic['url'] = url
                print(dic)
                lst.append(dic)
                time.sleep(0.8 + random())
            except:
                pass

            close_btn = driver.find_element(by=By.CSS_SELECTOR, value='#news-detail-modal button.modal-close')
            while close_btn.is_displayed():
                close_btn.click()
                time.sleep(0.7 + random())

        wait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#newsTab01_paging > a.page-next.page-link'))).send_keys(Keys.ENTER)

        if p % 15 == 0:
            df = pd.DataFrame(list(lst))
            df.to_csv(f"기업뉴스묶음_backup{p//15}.csv", index=False, encoding="utf-8-sig")
            time.sleep(random() * 70)
        else:
            pass


def multi_processing():
    names = ['한국가스공사', 'CJ제일제당', 'GS칼텍스', 'S-OIL', '두산에너빌리티', '한국도로공사', 'GS리테일']
    num_cores = 7
    pool = Pool(num_cores)
    [pool.apply_async(open_browser, args=[name, lst]) for name in names]
    pool.close()
    pool.join()

if __name__ == "__main__":
    start = time.time()
    manager = Manager()
    lst = manager.list()
    multi_processing()
    df = pd.DataFrame(list(lst))
    df.to_csv("기업뉴스묶음7.csv", index=False, encoding="utf-8-sig")
    print('총 소요시간 : ', time.time() - start)