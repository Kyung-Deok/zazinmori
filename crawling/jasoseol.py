from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from random import random
import pyperclip
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains



driver = webdriver.Chrome(executable_path='drivers/chromedriver')


### 자소설 사이트 접속
target_url = 'https://jasoseol.com/recruit'
driver.get(target_url)
driver.maximize_window()
sleep(1 + random())



### 회사 id 리스트 저장
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

company_id_list = []


# 바로 채용공고로 넘어가는 회사 리스트
company_list1 = soup.select('a.company')
print('*1*', len(company_list1))
for company in company_list1:
    company_id_list.append(company.get('employment_company_id'))


# 2번 클릭해야 채용공고로 넘어가는 회사 리스트
company_list2 = driver.find_elements(By.CSS_SELECTOR, 'div.company > div.company-name')
print('*2*', len(company_list2))

action = ActionChains(driver) # 각 채용공고 클릭하기 위해 ActionChain 사용
a = 0 # 회사 수 확인 용도
for company in company_list2:
    # 2이상 채용공고 묶여 있는 회사들 클릭
    driver.execute_script("arguments[0].click();", company)
    a += 1
    print(a, company.text)
    sleep(0.5 + random())

# 클릭하여 세부 채용공고 주소 id 가져올 수 있는 상태로 만들어 두었음
group_items = driver.find_elements(By.CLASS_NAME, 'employment-group-item')
#print(len(group_items))
for item in group_items:
    company_id_list.append(item.get_attribute('employment_id'))
#print(company_id_list)
#print(len(company_id_list))

# 중복 id 제거
company_ids = []
for id in company_id_list:
    if id not in company_ids:
        company_ids.append(id)
#print(company_id)
print(len(company_ids))


#company_id = ['68504', '68193', '68070', '67990', '68314', '68095', '67902', '68030', '67546', '67984', '68135', '67807', '68167', '68021', '68130', '67683', '67778', '67801', '67559', '67945', '68071', '67977', '68285', '68337', '67978', '67964', '68143', '67535', '67592', '67186', '67912', '67879', '68014', '67824', '68261', '67746', '68057', '67243', '68050', '68052', '67754', '67873', '68524', '68542', '68534', '68544', '68698', '68532', '68514', '68551', '68554', '68545', '68549', '68550', '68527', '68569', '68553', '68562', '68548', '68565', '68597', '68623', '68518', '68511', '68541', '68547', '68489', '68145', '68468', '68552', '68526', '68438', '67948', '68522', '68598', '68497', '68499', '68564', '68513', '68402', '68538', '68555', '68517', '68498', '68531', '68459', '68306', '68470', '68619', '67727', '68161', '68429', '68031', '68397', '67966', '68289', '67395', '68038', '68127', '68164', '68278', '68111', '67507', '67048', '67799', '68305', '68316', '68150', '68148', '67911', '66474', '68250', '68078', '67967', '68286', '68231', '67698', '67979', '68094', '67845', '67832', '68618', '68617', '68602', '68580', '68703', '68567', '68576', '68596', '68584', '68613', '68566', '68631', '68629', '68575', '68650', '68585', '68658', '68579', '68620', '68760', '68624', '68795', '68592', '68577', '68625', '68628', '68626', '68610', '68636', '68646', '68639', '68587', '68591', '68546', '68608', '68601', '68616', '68611', '68561', '68599', '68069', '67996', '67862', '68012', '68288', '67947', '68309', '68162', '68302', '68248', '68271', '62272', '68205', '67697', '67815', '67858', '68883', '68716', '68717', '68721', '68708', '68691', '68682', '68651', '68654', '68680', '68715', '68999', '68641', '68653', '68644', '68643', '68647', '68652', '68655', '68688', '68697', '68702', '68515', '68670', '68705', '68659', '68690', '68676', '68694', '68630', '68614', '68725', '68673', '68568', '68638', '68648', '68671', '68738', '68660', '68700', '68586', '68645', '68727', '68649', '68762', '68704', '68672', '68574', '69011', '68090', '67929', '68431', '66890', '68060', '67590', '68307', '67621', '68363', '66972', '68003', '68132', '67867', '68214', '68027', '67684', '67866', '67965', '68259', '67834', '67932', '67956', '67838', '68123', '67745', '67678', '67635', '68157', '67530', '68371', '61580', '66515', '68026', '67957', '68134', '67295', '68240', '67190', '67919', '68092', '67479', '67663', '68287', '67775', '67961', '68252', '68128', '68221', '68393', '67108', '68215', '67962', '68413', '68233', '68236', '67924', '67043', '68313', '68042', '67969', '67953', '67273', '66904', '68415', '68086', '68093', '68008', '68146', '67820', '68388', '68260', '68129', '68210', '68640', '68763', '68761', '68799', '68804', '68772', '68847', '68801', '68796', '68424', '69173', '68753', '68813', '68726', '68696', '68935', '68782', '69019', '68767', '68770', '68743', '68781', '68849', '68582', '68769', '68768', '68774', '68798', '68802', '68816', '68853', '68731', '68822', '68600', '68747', '68083', '68732', '68775', '68684', '68776', '68803', '68839', '68581', '68771', '68755', '68765', '69109', '68687', '68787', '68758', '68728', '68674', '68675', '68679', '68759', '68777', '68593', '68766', '68874', '68756', '68740', '68663', '68785', '68764', '68664', '68634', '68818', '68749', '68838', '68724', '68744', '68720', '68741', '68736', '68257', '67363', '67988', '68258', '67938', '68483', '68342', '68169', '68448', '65364', '68080', '68218', '68422', '68455', '68270', '68707', '68872', '68880', '68844', '68907', '68886', '68891', '68897', '68852', '68857', '68896', '68834', '68868', '68809', '68900', '68826', '68892', '68692', '68784', '68807', '68889', '68905', '68273', '68870', '68831', '68885', '68882', '68901', '69091', '68808', '68757', '68888', '68848', '68890', '68817', '68535', '68832', '68867', '68893', '68878', '68895', '68906', '68877', '68921', '69047', '69079', '67843', '63855', '68059', '68155', '68062', '68464', '68144', '68320', '68297', '68229', '68246', '68117', '68106', '68044', '68076', '68423', '67985', '68940', '68461', '68319', '68015', '68446', '68494', '68207', '68037', '68074', '68485', '68486', '68449', '68197', '68481', '68300', '68346', '68043', '68426', '68266', '67811', '68033', '67993', '68122', '67819', '68410', '68453', '68213', '68487', '68537', '68335', '68163', '68488', '68366', '68296', '68430', '67991', '66392', '68178', '68435', '68041', '68118', '68493', '67798', '68440', '68436', '67868', '68478', '68247', '67907', '68372', '68926', '68864', '69175', '68920', '68898', '68216', '68910', '69003', '68950', '68948', '68949', '68978', '68934', '69001', '68689', '68911', '68979', '69016', '68925', '69013', '68995', '69006', '69172', '68924', '68959', '68967', '68149', '69154', '68912', '68932', '68919', '68788', '68881', '68930', '68909', '68939', '68908', '68981', '68833', '68914', '68969', '68958', '68963', '68987', '68913', '68622', '68395', '68783', '68915', '68971', '69340', '68951', '68962', '69009', '68903', '68957', '68976', '69140', '68953', '68922', '68972', '68923', '68942', '68973', '68835', '68927', '68974', '68894', '68851', '68985', '68521', '68362', '67808', '68131', '68072', '68234', '68419', '68480', '68133', '68121', '68519', '68025', '68661', '68381', '67734', '68315', '68268', '66971', '68308', '68317', '68416', '67852', '68786', '68152', '68421', '68101', '67885', '68369', '69014', '69027', '69037', '69105', '69028', '69015', '69080', '69045', '69100', '69038', '69106', '69022', '69118', '69095', '69090', '69008', '69107', '69094', '69113', '69120', '69117', '69103', '69121', '69012', '69110', '69083', '69092', '68989', '69044', '69073', '69035', '69033', '69054', '69048', '69032', '69036', '68947', '69064', '69042', '69025', '69061', '69059', '69070', '69072', '69099', '68873', '69086', '69174', '69031', '69102', '69041', '69084', '69040', '69023', '69081', '69051', '69017', '69018', '69067', '68681', '69108', '69193', '69285', '68988', '68996', '69034', '69087', '69264', '69039', '69097', '69082', '69024', '69005', '69098', '69104', '68990', '68991', '69043', '67841', '68501', '68496', '68349', '68269', '67842', '68298', '68558', '68009', '68512', '68067', '68267', '68230', '68318', '68206', '68079', '67958', '67994', '68353', '68994', '69155', '69188', '69262', '69182', '69207', '69223', '69196', '69156', '69189', '69168', '69216', '69243', '69295', '69224', '69116', '69214', '69263', '69112', '69177', '69114', '69122', '69163', '69200', '69162', '69234', '69151', '69167', '69195', '69139', '69184', '69215', '69135', '69133', '69205', '69166', '69123', '69176', '69199', '69248', '69271', '69190', '69192', '69129', '69124', '69191', '69150', '68964', '69178', '69211', '69119', '69115', '64810', '68469', '68571', '68327', '68615', '68262', '68336', '68165', '68299', '69187', '69341', '69339', '69313', '69336', '69233', '69280', '69249', '69268', '69201', '69208', '69231', '69242', '68028', '69227', '69286', '69230', '69185', '69252', '69228', '69267', '69272', '69287', '69276', '69240', '69290', '69281', '69325', '69334', '69300', '69273', '69337', '69311', '69238', '69338', '69226', '69265', '69278', '69297', '69282', '69307', '69284', '69298', '69289', '69149', '68875', '69309', '69296', '69111', '69277', '68904', '69266', '69225', '69235', '69186', '68195', '68444', '68427', '68491', '68458', '68425', '67809', '65816', '69335', '67783', '68352', '68656', '68612', '68998', '65997', '68194', '69279', '68941', '68383', '68392', '68490', '68467', '68484', '68391', '68536', '68975', '68105', '68343', '68475', '68222', '68954', '68051', '68414', '67952', '68495', '68379', '68360', '68530', '68457', '69291', '69057', '68533', '68869', '68184', '68578', '68382', '68137', '68984', '68126', '68400', '67886', '68245', '68718', '66907', '68291', '68411', '69007', '68836', '68946', '68805', '67986', '69063', '68678', '65965', '69270', '66355', '69066', '67768', '67175', '68952', '67971', '68945', '67089', '68428', '67071', '68321', '68773', '68018', '67900', '69333', '68351', '69274', '68956', '66869', '66528', '69251', '68936', '69181', '68500', '69269', '68677', '69332', '69229', '68356', '68693', '68368', '66864', '68208', '68112', '69209', '66439', '69275', '66945', '68110', '66825', '67717', '63971', '68563', '69138', '67624', '68811', '68350', '69180', '68253', '68445', '67995', '67853', '67045', '68004', '67288', '68492', '66269', '66920', '67436', '67437', '68154', '69169', '69171', '66870', '68505', '69236', '69254', '68955', '68965', '69126', '69128', '69134', '69136', '69137', '69142', '69143', '69144', '69145', '69146', '69147', '69148', '69152', '69153', '68815', '68825', '68506', '68507', '68929', '68933', '69010', '69069', '69071', '68856', '68858', '69237', '69239', '69204', '69210', '69250', '69292', '69293', '68931', '68966', '69020', '69021', '68621', '68899', '69004', '69299', '69301', '69302', '69305', '69306', '68657', '68827', '69055', '69056', '68227', '68228', '69125', '69127', '68842', '68843', '68572', '68573', '68982', '68983', '69060', '69065', '69141', '69159', '68937', '68938', '68829', '68830', '68794', '69183', '69212', '69213', '68712', '68713', '68714', '68917', '68986', '68711', '69052', '69053', '68556', '68557', '69030', '69074', '69049', '69050', '68779', '68780', '69260', '69261', '68473', '68482', '68793', '68800', '68918', '68968', '69026', '69075', '69076', '68272', '68916', '69202', '69203', '68452', '68471', '69077', '69078', '69085', '68570', '69068', '68096', '68115', '68627', '68792', '68729', '68730', '68845', '68846', '68699', '68701', '69319', '69320', '69322', '69323', '69324', '68418', '68609', '67526', '67527', '69328', '69303', '69304', '69308', '69310', '69312', '68604', '68605', '68606', '68607', '68790', '68791', '67752', '68642', '68686', '68695', '68706', '69132', '69197', '69198', '69218', '69219', '69220', '69314', '69315', '69316', '69317', '69318', '69157', '69160', '68107', '68108', '68109', '68279', '68280', '69088', '69101', '69221', '69222', '69321', '69327', '69329', '69330', '68113', '68114', '68997', '68992', '68993', '69326', '68960', '68961', '68000', '68047', '68048', '67872', '68312', '68136', '68158', '68159', '68160', '68603', '68140', '68142', '68810', '68812', '68814', '68823', '68828', '68824', '68520', '68523', '68175', '68265', '68166', '68733', '68734', '68735', '68737', '68147', '68304', '68398', '68401', '68098', '68102', '68840', '68841', '68850', '68859', '68860', '68861', '68871', '68837', '68884', '68879', '68887', '68022', '68462', '68970', '68862', '68863', '68865', '68866', '68778', '68797', '68001', '68002', '67878', '67884', '67870', '67936', '68223', '68226', '66471', '67423', '67940', '68023', '67001', '67565', '67615', '67803', '67844', '66943', '67622', '67025', '67035', '68251', '68255', '68199', '68200', '68242', '63930', '68063', '67691', '67693', '67786', '67787', '67790', '67225', '67227', '67228', '67738', '68384', '64163', '64686', '67283', '68709', '68710', '68683', '68685', '67640', '67641', '67642', '68219', '68220', '67829', '67830', '68588', '68589', '67810', '67847', '67644', '67645', '68525', '68559', '68508', '68509', '68510', '68516', '68543', '68013', '68367', '67955', '68017', '67761', '68034', '68045', '68156', '68190', '67854', '67883', '68203', '68387', '67797', '67825', '68032', '68064', '68344', '68347', '68348', '67827', '67892', '68016', '68124', '68198', '68201']



### 로그인
target_url = 'https://jasoseol.com/recruit'
driver.get(target_url)
login_section = driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div[3]/div[2]/div[1]')
login_section.click()
sleep(2)
jss_id = ''
jss_pw = ''
elem_id = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/div/input')
elem_pw = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[1]/div[2]/div/input')
elem_id.click()
pyperclip.copy(jss_id)
elem_id.send_keys(Keys.CONTROL, 'v')
sleep(0.5)
elem_pw.click()
pyperclip.copy(jss_pw)
elem_pw.send_keys(Keys.CONTROL, 'v')
sleep(0.5)
login_btn = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[3]/div[2]/div[2]/a')
login_btn.click()
sleep(2)



### 크롤링 내용 저장할 데이터프레임
thead = ['corp_nm', 'start_time', 'end_time', 'period', 'main', 'img_or_text', 'jobs', 'exp', 'questions', 'words', 'url']
df = pd.DataFrame(columns=thead)
idx = 0

# 각 채용공고에 대해 반복
for company_id in company_ids:
    print('*****', idx, company_id, '*****')

    target_url = f'https://jasoseol.com/recruit/{company_id}'
    driver.get(target_url)
    sleep(2 + 2*random())

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    # corp_nm(회사명)
    corp_nm = driver.find_element(by=By.CSS_SELECTOR, value='div.ec-info-content.ec-name > span').text
    print('회사명: ', corp_nm)



    # start_time(시작기간), end_time(마감기간), period(수시채용 여부)
    try:
        start_time = driver.find_elements(by=By.CSS_SELECTOR, value='span.time > span')[0].text
        end_time = driver.find_elements(by=By.CSS_SELECTOR, value='span.time > span')[1].text
        period = ''
    except:
        start_time = ''
        end_time = ''
        period = '수시'
    print('채용기간:', start_time, '/', end_time, '/', period)



    # main(채용공고 내용)
    main_content = soup.select('div.employment-notice')[0]
    main = []
    if len(main_content.text) > 10:
        print('case1')
        print(soup.select('div.employment-notice')[0].text)
        main.append(soup.select('div.employment-notice')[0].text)
        img_or_text = 'text'
    else:
        print('case2')
        imgs = soup.select('div.employment-notice div.content img')
        for i in range(len(imgs)):
            src = imgs[i].get('src')
            main.append(src)
        print(len(main))
        img_or_text = 'img'
    print('채용공고:', len(main))
    print('채용공고 형태:', img_or_text)



    recruit_trs = soup.select('div.write-resume > table > tbody > tr')
    print('모집 직군 수 :', len(recruit_trs))

    # jobs(모집 직군), exp(경력 여부)
    jobs = []
    exp = []
    for tr in recruit_trs:
        jobs.append(tr.select('td')[1].text)
        exp.append(tr.select('td')[0].text)
    print('모집 직군:', len(jobs), jobs)
    print('경력 여부:', len(exp), exp)


    # questions(자소서 항목), words(글자 수)
    questions = []
    words = []

    for i in range(1, len(recruit_trs) + 1):

        job_questions = []
        job_words = []

        resume_btn = driver.find_element(By.XPATH,
                                         f'/html/body/div/div/div[2]/div/div[4]/div/div[2]/div/div/div[2]/recruit-slide/div[1]/div[2]/table/tbody/tr[{i}]/td[4]/div')
        mouse = ActionChains(driver).move_to_element(resume_btn)
        mouse.perform()
        sleep(0.5 + random())
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        sleep(1 + random())

        q_list = soup.select('ul.question-area > li')
        for k in range(len(q_list)):
            job_questions.append(soup.select('ul.question-area div.question')[k].text)
            job_words.append(soup.select('ul.question-area div.count')[k].text.strip('\n').strip().strip('\n'))

        questions.append(job_questions)
        words.append(job_words)

    print('자소서항목: ', len(questions), questions)
    print('글자 수: ', len(words), words)



    # url(지원사이트 주소)
    url = soup.select('div.homepage > a')[0].get('href')
    print('지원사이트:', url)



    tbody = []
    tbody.append(corp_nm)
    tbody.append(start_time)
    tbody.append(end_time)
    tbody.append(period)
    tbody.append(main)
    tbody.append(img_or_text)
    tbody.append(jobs)
    tbody.append(exp)
    tbody.append(questions)
    tbody.append(words)
    tbody.append(url)

    df.loc[idx] = tbody
    idx += 1


    # 중간 저장
    if len(df)%10 == 0:
        df.to_csv('jobposting.csv', index=True)

    print('*****', idx, corp_nm, '끝 *****')
    sleep(2*random())



df.to_csv('jobposting.csv', index=True)
