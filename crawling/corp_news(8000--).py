import time, math
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


def open_browser(page, lst, name):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(f'https://www.bigkinds.or.kr/v2/depthAnalysis/company/{name}/depthAnalComView.do?codeGroupNo=300')
    time.sleep(7)
    npp = int(len(driver.find_elements(by=By.CSS_SELECTOR, value='#newsTab01-news-results > li')))
    page_num = int(driver.find_element(by=By.CSS_SELECTOR, value='#newsTab01_paging > span.total').text)
    element = wait(driver, 10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#newsTab01_paging > input")))[0]
    element.clear()
    element.send_keys(page)
    time.sleep(1 + random())
    element.send_keys(Keys.ENTER)
    time.sleep(3 + random())
    for p in range(1, math.trunc(page_num/7)+1):
        print(f'*******LOOP: {p}*******')
        for k in range(1, npp + 1):
            dic = dict()
            corp_nn = driver.find_element(by=By.CSS_SELECTOR, value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > p.k-name').text
            category = driver.find_element(by=By.CSS_SELECTOR, value='#contents > div.contents > section.spacial-page.detail-intro > div > div.infomation > div > dl > dd:nth-child(2)').text
            try:
                wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f'/html/body/div[1]/main/div[1]/div[1]/section[2]/div/div/div[2]/div[2]/div/div[1]/ul/li[{k}]/a'))).send_keys(Keys.ENTER)
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
                time.sleep(0.5 + random())

        wait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#newsTab01_paging > a.page-next.page-link'))).send_keys(Keys.ENTER)

        if p % 15 == 0:
            df = pd.DataFrame(list(lst))
            df.to_csv(f"{name}_backup{p//15}.csv", index=False, encoding="utf-8-sig")
            time.sleep(random() * 95)
        else:
            pass

def multi_processing():
    pages = [1, 18, 35, 52, 69, 86, 103]
    num_cores = 7
    pool = Pool(num_cores)
    [pool.apply_async(open_browser, args=[page, lst, name]) for page in pages]
    pool.close()
    pool.join()

if __name__ == "__main__":
    start = time.time()
    manager = Manager()
    name = '농심'
    lst = manager.list()
    multi_processing()
    df = pd.DataFrame(list(lst))
    df.to_csv(f"{name}.csv", index=False, encoding="utf-8-sig")
    print('총 소요시간 : ', time.time() - start)

