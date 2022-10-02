from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from random import random
import pyperclip
from bs4 import BeautifulSoup


driver = webdriver.Chrome(executable_path='drivers/chromedriver')


### 네이버에서 로그인 ###

# 네이버 이동
target_url = 'https://www.naver.com'
driver.get(target_url)
sleep(1)

# 로그인 버튼 클릭
login_btn = driver.find_element(By.CLASS_NAME, 'link_login')
login_btn.click()
sleep(1)

# id, pw 입력
naver_id = ''
naver_pw = ''
elem_id = driver.find_element(By.ID, 'id')
elem_id.click()
pyperclip.copy(naver_id)
elem_id.send_keys(Keys.CONTROL, 'v')
sleep(0.5)
elem_pw = driver.find_element(By.ID, 'pw')
elem_pw.click()
pyperclip.copy(naver_pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
sleep(0.5)

# 로그인 버튼 클릭
driver.find_element(By.ID, 'log.login').click()
sleep(2)



### 독취사 내 합격자소서 게시판의 게시물번호 저장 ###

target_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=16996348&search.menuid=209&search.boardtype=L'
driver.get(target_url)
sleep(1 + 2*random())

driver.switch_to.frame('cafe_main')

article_ids = []


for page in range(1, 1001):
    print('*****', page, '*****')
    target_url = f'https://cafe.naver.com/ArticleList.nhn?search.clubid=16996348&search.menuid=209&search.boardtype=L&search.cafeId=16996348&search.page={page}'
    driver.get(target_url)
    sleep(1 + random())

    driver.switch_to.frame('cafe_main')
    ids = driver.find_elements(By.CLASS_NAME, 'inner_number')

    for i in range(len(ids)):
        id = ids[i].text
        article_ids.append(id)



#df.to_csv('fail_article_ids.csv')
#article_ids = pd.read_csv('fail_article_ids.csv', index_col=0)


#article_ids = article_ids_df


# 컬럼명 설정
thead = ['title', 'date', 'main']
df = pd.DataFrame(columns=thead)
# 인덱스 넘버
idx = 0

#print(len(article_ids)) #15000개


for i in range(len(article_ids)):
    print('*****', i, '*****')

    # 각 게시물번호 쿼리문에 입력해 페이지 접속
    #article_id = article_ids.loc[i][0]
    article_id = article_ids[i]
    target_url = f'https://cafe.naver.com/ArticleRead.nhn?clubid=16996348&page=1&menuid=209&boardtype=L&articleid={article_id}&referrerAllArticles=false'
    driver.get(target_url)
    sleep(4+2*random())

    try:
        driver.switch_to.alert.accept()
        sleep(2)

    except:
        try:
            driver.switch_to.frame('cafe_main')
            sleep(1+2*random())

            # bs4를 통해 문서를 객체로 반환
            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')


            # 데이터프레임의 각 row 저장해놓을 빈 리스트
            tbody = []

            # 게시글 제목 저장
            title = soup.select('.title_text')[0].text.strip('\n').strip()
            print('제목:', title)
            tbody.append(title)

            # 게시글 작성 날짜 저장
            date = soup.select('span.date')[0].text
            print('날짜:', date)
            tbody.append(date)


            # 게시글 본문 텍스트 포함되어 있는 태그들
            contents = soup.select('p.se-text-paragraph > span')
            # 게시글 본문 저장
            main = ''
            for content_num in range(len(contents)):
                main = main + contents[content_num].text
            print('본문:', len(main), main)
            if len(main) > 100:
                tbody.append(main)

                print(i, idx, tbody)
                df.loc[idx] = tbody
                idx += 1

            else:
                main = soup.select('div.ContentRenderer')[0].text
                print('본문:', main)

                if len(main) > 100:
                    tbody.append(main)

                    print(i, idx, tbody)
                    df.loc[idx] = tbody
                    idx += 1
                else:
                    print(f'**{i}** 확인')
                    continue

        except:
            continue



    if i%100 == 0:
        df.to_csv('fail_cvletter.csv')


#print(df)
df.to_csv('fail_cvletter.csv')

