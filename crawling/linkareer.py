from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd
from random import random


# 컬럼명 설정
thead = ['title', 'spec', 'main']
linkareer_df = pd.DataFrame(columns=thead)
# 인덱스 넘버
id_num = 0


driver = webdriver.Chrome(executable_path='../drivers/chromedriver')

#for page in range(1, 51):
for page in range(1, 569):
    target_url = f'https://linkareer.com/cover-letter/30563?page={page}&sort=PASSED_AT&tab=all'
    driver.get(target_url)
    sleep(1+2*random())

    # 한 페이지에 20개씩의 자소서 존재
    for i in range(1, 21):

        try:

            print(id_num)

            # i번째 자소서 클릭
            letter_link = driver.find_element(By.XPATH, f'/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[1]/div/div[2]/div[{i}]/a/div/p')
            letter_link.click()
            sleep(0.5 + 2 * random())

            tbody = []

            # 자소서 제목 가져오기
            title = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/h1')
            #print(title.text)
            tbody.append(title.text)

            # 작성자 스펙 가져오기
            spec = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[2]/div[1]/div/div/div[3]/p')
            #print(spec.text)
            tbody.append(spec.text)

            # 작성내용 가져오기(문항구분 없음)
            main = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div[2]/div/div[2]/div[3]/article/main')
            #print(main.text)
            tbody.append(main.text)

            linkareer_df.loc[id_num] = tbody
            id_num += 1


        except:

            pass


linkareer_df.to_csv('./coverletter_linkareer.csv', index=True)