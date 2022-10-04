from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring, concat, col
from pyspark.sql.functions import regexp_extract, split, trim, regexp_replace, when, lit, upper
from pyspark.sql.functions import isnull, length


sc = SparkContext()
spark =SparkSession.builder.getOrCreate()

user="root"
password="qwer1234"
url="jdbc:mysql://35.79.77.17:3306/pjt3"
driver="com.mysql.cj.jdbc.Driver"
dbtable="failcvletter"


df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').load('cvletter_data/fail_cvletter.csv')

###빈행제거, 중복제거
df = df.dropna().dropDuplicates(['title'])
#df.count():7223


###recruit_date, corp_nm, job, new_or_exp
df1=df.withColumn('recruit_date', concat(substring(col('date'), 1, 4), substring(col('date'), 6, 2))).drop(col('date')).drop(col('title'))\
.withColumn('corp_nm', trim(regexp_extract(col('main'), r'(1\. 기업명 :)(.*)(2\. 지원)', 2)))\
.withColumn('job', trim(regexp_extract(col('main'), r'(2\. 지원분야 :)(.*)(3\. 지원)', 2)))\
.withColumn('new_or_exp', lit(''))


###자소서 부분 추출
df2=df1.withColumn('main1', split('main', '자기소개서 작성', 2).getItem(1))
df3=df2.withColumn('main', when(df2.main1.isNull(), df2.main).otherwise(df2.main1)).drop('main1')\
.withColumn('main', split('main', '\[참고\]').getItem(0)).withColumn('main', split('main', '좋은 결과 있').getItem(0)).withColumn('main', split('main', '⚠').getItem(0))\
.withColumn('main', regexp_replace('main', '▼', ''))\
.withColumn('main', regexp_replace('main', '\xa0', ' ')).withColumn('main', regexp_replace('main', '\u200b', ' '))\
.withColumn('main', trim('main'))


###질문, 답변 분리
df4=df3.withColumn('q1', concat(regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 1), regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 2)))\
.withColumn('main', trim(split('main', r'(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))', 2).getItem(1)))\
.withColumn('a1', trim(split('main', r'([1-9Q]\.|\*|-----)').getItem(0))).withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))
df5=df4.withColumn('a1', when(df4.a1=='', df4.main).otherwise(df4.a1))\
.withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))

df5=df4.withColumn('q2', concat(regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 1), regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 2)))\
.withColumn('main', trim(split('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))', 2).getItem(1)))\
.withColumn('a2', trim(split('main', r'([1-9Q]\.|\*|-----)').getItem(0))).withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))
df6=df5.withColumn('a2', when(df5.a2=='', df5.main).otherwise(df5.a2))\
.withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))

df7=df6.withColumn('q3', concat(regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 1), regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 2)))\
.withColumn('main', trim(split('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))', 2).getItem(1)))\
.withColumn('a3', trim(split('main', r'([1-9Q]\.|\*|-----)').getItem(0))).withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))
df8=df7.withColumn('a3', when(df7.a3=='', df7.main).otherwise(df7.a3))\
.withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))

df9=df8.withColumn('q4', concat(regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 1), regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 2)))\
.withColumn('main', trim(split('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))', 2).getItem(1)))\
.withColumn('a4', trim(split('main', r'([1-9Q]\.|\*|-----)').getItem(0))).withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))
df10=df9.withColumn('a4', when(df9.a4=='', df9.main).otherwise(df9.a4))\
.withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))

df11=df10.withColumn('q5', concat(regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 1), regexp_extract('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))([\w\W]*)', 2)))\
.withColumn('main', trim(split('main', r'(.*?)(하\)|내\)|자\)|능\)|0자|\[|시오\.|세요\.|니까|랍니다\.|함\))', 2).getItem(1)))\
.withColumn('a5', trim(split('main', r'([1-9Q]\.|\*|-----)').getItem(0))).withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))
df12=df11.withColumn('a5', when(df11.a5=='', df11.main).otherwise(df11.a5))\
.withColumn('main', trim(split('main', r'([1-9Q]\.|\*|-----)', 2).getItem(1)))


cv= df12.withColumn('corp_nm', trim(regexp_replace('corp_nm', r'\(.*\)', ''))).withColumn('corp_nm', regexp_replace('corp_nm', ' ', '')).withColumn('corp_nm', upper(col('corp_nm')))\
.withColumn('q1', trim(regexp_replace('q1', r'\[$', ''))).withColumn('q2', trim(regexp_replace('q2', r'\[$', ''))).withColumn('q3', trim(regexp_replace('q3', r'\[$', ''))).withColumn('q4', trim(regexp_replace('q4', r'\[$', ''))).withColumn('q5', trim(regexp_replace('q5', r'\[$', '')))\
.withColumn('a1', trim(split('a1', '>>').getItem(0)))\
.filter(length('corp_nm')<20)\
.filter(length('job')<20)


# q1, a1 중 빈 컬럼 있으면 제거
cv1=cv.withColumn("a1", when(col("a1")=="" ,None).otherwise(col("a1"))).na.drop('any', subset=['q1', 'a1']).drop('main').drop('_c0')
#cv1.count() : 5575

## regi_code
## mysql db에 저장되어 있는 corp 테이블 불러오기
#corp_df = spark.read.format("jdbc").options(user=user, password=password, url=url, driver=driver, dbtable="corporation").load()
#corp_df = corp_df.select(col('corp_nm'), col('regi_code'))
## corp 테이블과 조인하여 regi_code 컬럼 추가
#cv1 = cv1.join(corp_df, cv1.corp_nm==corp_df.corp_nm, 'left_outer')


cv1.write.jdbc(url, dbtable, "append", properties={"driver": driver, "user": user, "password": password})
