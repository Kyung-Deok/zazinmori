from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring, concat, col
from pyspark.sql.functions import regexp_extract, split, trim, regexp_replace, when, lit, upper
from pyspark.sql.functions import length
from datetime import datetime

tdy = datetime.today()

sc = SparkContext()
spark =SparkSession.builder.getOrCreate()

user="root"
password="qwer1234"
url="jdbc:mysql://35.79.77.17:3306/pjt3"
driver="com.mysql.cj.jdbc.Driver"
dbtable="passcvletter"


########## dokchi ##########
df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').option('multiline', 'true').load(f'update/dokchi{tdy}.csv')

###recruit_date 추가
df=df.withColumn('recruit_date', concat(substring(col('date'), 1, 4), substring(col('date'), 6, 2))).drop(col('date'))


#양식에 따라 구분
df1 = df.where(col('_c0')<=152)
df2 = df.where(1154>=col('_c0')).where(col('_c0')>=153)
df3 = df.where(1849>=col('_c0')).where(col('_c0')>=1155)
df4 = df.where(2781>=col('_c0')).where(col('_c0')>=1850)
df5 = df.where(4517>=col('_c0')).where(col('_c0')>=2782)
df6 = df.where(5076>=col('_c0')).where(col('_c0')>=4518)
df7 = df.where(col('_c0')>=5077)


###corp_nm
df1_1=df1.withColumn('corp_nm_1', regexp_extract(col('main'), r'(\(예\: 현대자동차 연구개발직\))([\wa-zA-Zㄱ-ㅎ가-힣 ]*)( )', 2)).withColumn('corp_nm_2', regexp_extract(col('main'), r'(부서\(직무\) \☞)([\wa-zA-Zㄱ-ㅎ가-힣 ]*)( )', 2))
df1_1=df1_1.withColumn('corp_nm', when(df1_1.corp_nm_1=='', df1_1.corp_nm_2).otherwise(df1_1.corp_nm_1)).drop(col('title')).drop(col('corp_nm_1')).drop(col('corp_nm_2'))
df2_1=df2.withColumn('corp_nm', regexp_extract(col('main'), r'(합격기업 :)(.*)', 2)).withColumn('corp_nm', trim(split(col('corp_nm'), '-').getItem(0))).drop(col('title'))
df3_1=df3.withColumn('corp_nm', trim(split('title', r'합격|자소서|자기소|서류|[0-9]+년|\/|\]').getItem(0))).drop(col('title'))
df4_1=df4.withColumn('corp_nm', regexp_extract(col('main'), r'(합격기업 :)(.*)', 2)).withColumn('corp_nm', trim(split(col('corp_nm'), '-').getItem(0))).drop(col('title'))
df5_1=df5.withColumn('corp_nm', regexp_extract(col('main'), r'(지원 직무)(.*)', 2)).withColumn('corp_nm', split(col('corp_nm'), '/|지원').getItem(0)).drop(col('title')).withColumn('corp_nm', trim(regexp_replace('corp_nm', 'ex\)', '')))
df6_1=df6.withColumn('corp_nm_1', trim(split('main', '지원기업:').getItem(1))).withColumn('corp_nm_1', trim(split('corp_nm_1', '☞ ').getItem(0)))
df6_1=df6_1.withColumn('corp_nm_2', trim(split('title', r'합격|자소서|자기소|\]').getItem(0))).withColumn('corp_nm_2', regexp_replace('corp_nm_2', r'\[|RE:', ''))
df6_1=df6_1.withColumn('corp_nm', when(df6_1.corp_nm_1=='', df6_1.corp_nm_2).otherwise(df6_1.corp_nm_1)).drop(col('title')).drop(col('corp_nm_1')).drop(col('corp_nm_2'))
df7_1=df7.withColumn('corp_nm', trim(split('title', r'합격|자소서|자기소|\]|채용|[0-9]+년|/|\>|\,|최종|서류').getItem(0))).withColumn('corp_nm', regexp_replace('corp_nm', r'RE:|\[|\<|\>|↓', '')).drop(col('title'))


###job
df1_2=df1_1.withColumn('job',regexp_extract(col('main'), r'(부서\(직무\) ☞)([\D]*)(\&| )([\D]*)(✍)', 4))
df2_2=df2_1.withColumn('job', regexp_extract(col('main'), r'(지원부서 or 직무 :)(.*)', 2)).withColumn('job', split(col('job'), '02.').getItem(0))
df3_2=df3_1.withColumn('job', lit(''))
df4_2=df4_1.withColumn('job', regexp_extract(col('main'), r'(지원부서 or 직무 :)(.*)', 2)).withColumn('job', split(col('job'), '02.').getItem(0))
df5_2=df5_1.withColumn('job', regexp_extract(col('main'), r'(지원 직무)(.*)', 2)).withColumn('job', split(col('corp_nm'), '지원').getItem(0)).withColumn('job', trim(split(col('job'), '/', 2).getItem(1)))
df6_2=df6_1.withColumn('job', trim(split('main', '지원분야:').getItem(1))).withColumn('job', trim(split('job', '☞ ').getItem(0)))
df7_2=df7_1.withColumn('job', lit(''))


### q1~a5

#자소서 본문 내용만 main으로 분리
df1_3=df1_2.withColumn('main', trim(regexp_extract(col('main'), r'(:\)☞*)(.*)(📣)', 2)))
df2_3=df2_2.withColumn('main', trim(regexp_extract(col('main'), r'(남겨주세요.)(.*)(★★)', 2)))
df3_3=df3_2
df4_3=df4_2.withColumn('main', trim(regexp_extract(col('main'), r'(남겨주세요.)(.*)(★★)', 2)))
df5_3=df5_2.withColumn('main', trim(regexp_extract(col('main'), r'(남겨주세요.)(.*)', 2)))
df6_3=df6_2.withColumn('main', trim(regexp_extract(col('main'), r'(☞ 합격자소서)(.*)', 2)))
df7_3=df7_2

#다시 합치기
udf=df1_3.union(df2_3).union(df3_3).union(df4_3).union(df5_3).union(df6_3).union(df7_3)

#넘버링 제거
udf=udf.withColumn('main', regexp_extract('main', r'([0-9A-Z]*\.)(.*)', 2))
#질문 특수기호로 끊기, 답변 넘버링으로 끊기
#q1, a1
udf=udf.withColumn('q1', split(col('main'), r'\[|\(|\.|\\').getItem(0)).withColumn('main', split(col('main'), r'\[|\(|\.|\\', 2).getItem(1))
udf=udf.withColumn('a1', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
#q2, a2
udf=udf.withColumn('q2', split(col('main'), r'\[|\(|\.|\\').getItem(0)).withColumn('main', split(col('main'), r'\[|\(|\.|\\', 2).getItem(1))
udf=udf.withColumn('a2', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
#q3, a3
udf=udf.withColumn('q3', split(col('main'), r'\[|\(|\.|\\').getItem(0)).withColumn('main', split(col('main'), r'\[|\(|\.|\\', 2).getItem(1))
udf=udf.withColumn('a3', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
#q4, a4
udf=udf.withColumn('q4', split(col('main'), r'\[|\(|\.|\\').getItem(0)).withColumn('main', split(col('main'), r'\[|\(|\.|\\', 2).getItem(1))
udf=udf.withColumn('a4', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
#q5, a5
udf=udf.withColumn('q5', split(col('main'), r'\[|\(|\.|\\').getItem(0)).withColumn('main', split(col('main'), r'\[|\(|\.|\\', 2).getItem(1))
udf=udf.withColumn('a5', split(col('main'), r'[0-9A-Z]\.').getItem(0))

cv1 = udf.withColumn('new_or_exp', lit('')).drop(col('main')).drop(col('_c0'))



########## linkareer ##########
df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').option('multiline', 'true').load(f'updata/linkareer{tdy}.csv')

###corp_nm
df1=df.withColumn('corp_nm', trim(split(col('title'), '/').getItem(0)))

###job
df2=df1.withColumn('job', trim(split(col('title'), '/').getItem(1)))

###recruit_date
df3_1=df2.withColumn('date', trim(split(col('title'), '/').getItem(2)))
df3_2=df3_1.withColumn('year', substring('date', 1, 4)).withColumn('month', substring('date', 6, 1))
df3_3=df3_2.withColumn('month', when(df3_2.month=='상', '03').otherwise('09'))
df3=df3_3.withColumn('recruit_date', concat(col('year'), col('month'))).drop(col('year')).drop(col('month')).drop(col('date'))

###new_or_exp
df4=df3.withColumn('new_or_exp', lit(''))

###q,a추출
udf=df4.drop(col('title')).drop(col('spec'))
udf1=udf.withColumn('q1', regexp_extract('main', r'([0-9A-Z]*\.*)(.*)', 2)).withColumn('main', regexp_extract('main', r'([0-9A-Z]*\.*)(.*)([\w\W]*)', 3))
udf2=udf1.withColumn('a1', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
udf3=udf2.withColumn('q2', regexp_extract('main', r'(.*)([\w\W]*)', 1)).withColumn('main', regexp_extract('main', r'(.*)([\w\W]*)', 2))
udf4=udf3.withColumn('a2', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
udf5=udf4.withColumn('q3', regexp_extract('main', r'(.*)([\w\W]*)', 1)).withColumn('main', regexp_extract('main', r'(.*)([\w\W]*)', 2))
udf6=udf5.withColumn('a3', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
udf7=udf6.withColumn('q4', regexp_extract('main', r'(.*)([\w\W]*)', 1)).withColumn('main', regexp_extract('main', r'(.*)([\w\W]*)', 2))
udf8=udf7.withColumn('a4', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))
udf9=udf8.withColumn('q5', regexp_extract('main', r'(.*)([\w\W]*)', 1)).withColumn('main', regexp_extract('main', r'(.*)([\w\W]*)', 2))
udf10=udf9.withColumn('a5', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', split(col('main'), r'[0-9A-Z]\.', 2).getItem(1))

cv2 = udf10.drop(col('main')).drop(col('_c0'))



########## incruit ##########
df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').option('multiline', 'true').load(f'updata/incruit{tdy}.csv')

###job
df1=df.withColumn('job', trim(regexp_extract(col('content'), r'(직무 :)(.*)', 2)))

###recruit_date, new_or_exp
df2=df1.withColumn('recruit_date', lit('')).withColumn('new_or_exp', lit(''))

###q,a추출
#넘버링제거
udf1=df2.withColumn('q1', regexp_extract('content', r'([0-9A-Z]\.)(.*)', 2)).withColumn('main', regexp_extract('content', r'([0-9A-Z]\.)(.*)(\n*)([\w\W]*)', 4))
udf2=udf1.withColumn('a1', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', trim(split(col('main'), r'[0-9A-Z]\.', 2).getItem(1)))
udf3=udf2.withColumn('q2', regexp_extract('main', r'(.*)([\w\W])', 1)).withColumn('main', regexp_extract('main', r'(.*)(\n*)([\w\W]*)', 3))
udf4=udf3.withColumn('a2', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', trim(split(col('main'), r'[0-9A-Z]\.', 2).getItem(1)))
udf5=udf4.withColumn('q3', regexp_extract('main', r'(.*)([\w\W])', 1)).withColumn('main', regexp_extract('main', r'(.*)(\n*)([\w\W]*)', 3))
udf6=udf5.withColumn('a3', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', trim(split(col('main'), r'[0-9A-Z]\.', 2).getItem(1)))
udf7=udf6.withColumn('q4', regexp_extract('main', r'(.*)([\w\W])', 1)).withColumn('main', regexp_extract('main', r'(.*)(\n*)([\w\W]*)', 3))
udf8=udf7.withColumn('a4', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', trim(split(col('main'), r'[0-9A-Z]\.', 2).getItem(1)))
udf9=udf8.withColumn('q5', regexp_extract('main', r'(.*)([\w\W])', 1)).withColumn('main', regexp_extract('main', r'(.*)(\n*)([\w\W]*)', 3))
udf10=udf9.withColumn('a5', split(col('main'), r'[0-9A-Z]\.').getItem(0)).withColumn('main', trim(split(col('main'), r'[0-9A-Z]\.', 2).getItem(1)))

cv3 = udf10.drop(col('main')).drop(col('content'))



########## jobkorea ##########
df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').option('multiline', 'true').load(f'updata/jobkorea{tdy}.csv')

df1=df.select(col('corp_nm'), col('job'), col('employment_date').alias('date'), col('new_or_exp'), col('Q1').alias('q1'), col('A1').alias('a1'), col('Q2').alias('q2'), col('A2').alias('a2'), col('Q3').alias('q3'), col('A3').alias('a3'), col('Q4').alias('q4'), col('A4').alias('a4'), col('Q5').alias('q5'), col('A5').alias('a5'))
df2=df1.withColumn('year', substring('date', 1, 4)).withColumn('month', substring('date', 7, 1))
df3=df2.withColumn('month', when(df2.month=='상', '03').otherwise('09'))
df4=df3.withColumn('recruit_date', concat(col('year'), col('month'))).drop(col('year')).drop(col('month')).drop(col('date'))

cv4=df4



#################################

cv1=cv1.select('corp_nm', 'job', 'recruit_date', 'new_or_exp', 'q1', 'a1', 'q2', 'a2', 'q3', 'a3', 'q4', 'a4', 'q5', 'a5')
cv2=cv2.select('corp_nm', 'job', 'recruit_date', 'new_or_exp', 'q1', 'a1', 'q2', 'a2', 'q3', 'a3', 'q4', 'a4', 'q5', 'a5')
cv3=cv3.select('corp_nm', 'job', 'recruit_date', 'new_or_exp', 'q1', 'a1', 'q2', 'a2', 'q3', 'a3', 'q4', 'a4', 'q5', 'a5')
cv4=cv4.select('corp_nm', 'job', 'recruit_date', 'new_or_exp', 'q1', 'a1', 'q2', 'a2', 'q3', 'a3', 'q4', 'a4', 'q5', 'a5')

cv=cv1.union(cv2).union(cv3).union(cv4)
cv=cv.withColumn('corp_nm', regexp_replace(col('corp_nm'), r'\([^)]*\)', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), r' ', ''))\
.withColumn('corp_nm', upper('corp_nm'))\
.filter(length('corp_nm')<20)\
.filter(length('job')<20)

## regi_code
## mysql db에 저장되어 있는 corp 테이블 불러오기
#corp_df = spark.read.format("jdbc").options(user=user, password=password, url=url, driver=driver, dbtable="corporation").load()
#corp_df = corp_df.select(col('corp_nm'), col('regi_code'))
## corp 테이블과 조인하여 regi_code 컬럼 추가
#cv = cv.join(corp_df, cv.corp_nm==corp_df.corp_nm, 'left_outer')


cv.write.jdbc(url, dbtable, "append", properties={"driver": driver, "user": user, "password": password})

