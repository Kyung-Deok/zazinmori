from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, when, lit, regexp_replace, explode
from pyspark.sql.functions import monotonically_increasing_id, expr


sc = SparkContext()
spark =SparkSession.builder.getOrCreate()

user="admin"
password="qwer1234"
url="jdbc:mysql://35.79.77.17:3306/pjt3"
driver="com.mysql.cj.jdbc.Driver"



df = spark.read.format('csv').option('escape', '"').option('header', 'true').option('encoding', 'utf-8').load('/zazinmori/raw_data/jobposting.csv')

##### spark로 처리 안 되는 35행 제거)
df = df.coalesce(1).select(monotonically_increasing_id().alias('id'), expr('*'))
lst = [101, 154, 299, 366, 368, 369, 375, 382, 412, 430, 464, 502, 516, 520, 542, 585, 688, 689, 692, 693, 695, 696, 771, 787, 795, 834, 838, 865, 883, 1021, 1125, 1155, 1179, 1180]
df = df.filter(~df.id.isin(lst)).drop('id')
#################################



##########jobposting table##########

# jobposting_id 컬럼 추가(1부터 차례대로 1씩 증가)
df_id = df.coalesce(1).select(monotonically_increasing_id().alias('jobposting_id'), expr('*')).withColumn('jobposting_id', col('jobposting_id')+1)
jobposting_df=df_id.select(col('jobposting_id'), col('corp_nm'), col('period'), col('start_time'), col('end_time'), col('main').alias('posting_detail'), col('img_or_text').alias('posting_type'), col('url'))

## regi_code

## regi_code
# mysql db에 저장되어 있는 corp 테이블 불러오기
corp_df = spark.read.format("jdbc").options(user=user, password=password, url=url, driver=driver, dbtable="corporation").load()
corp_df = corp_df.select(col('corp_nm'), col('regi_code'))
corp_df1 = corp_df.withColumn('corp_nm', regexp_replace(col('corp_nm'), '\([\w]*\)', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '주식회사', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '유한회사', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), ' ', ''))\
.withColumn('corp_nm_drop2', upper(col('corp_nm')))\
.select('corp_nm_drop2', col('regi_code').alias('regi_code_drop'))

# corp 테이블과 조인하여 regi_code 컬럼 추가
jobposting_df = jobposting_df.withColumn('corp_nm', regexp_replace('corp_nm', '\([\w]*\)', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), 'KB국민카드', '케이비국민카드')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '하나금융투자', '하나금융지주')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), 'KDB산업은행', '한국산업은행')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), 'KCC', '케이씨씨')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '신한라이프', '신한라이프생명보험')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '경기주택도시공사', '경기도시공사')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), 'LG상사', 'LX인터내셔널'))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '오렌지라이프', '오렌지라이프생명보험')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '한진중공업', '한진중공업홀딩스')) \
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '에스케이트레이딩인터내셔널㈜', '에스케이트레이딩인터내셔널')) \
.withColumn('corp_nm', trim(col('corp_nm')))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '주식회사', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), '유한회사', ''))\
.withColumn('corp_nm', regexp_replace(col('corp_nm'), ' ', ''))\
.withColumn('corp_nm_drop1', upper(col('corp_nm')))\
.drop(col('corp_nm'))

jobposting_df = jobposting_df.join(corp_df1, jobposting_df.corp_nm_drop1==corp_df1.corp_nm_drop2, 'left_outer')
jobposting_df = jobposting_df.join(corp_df, jobposting_df.regi_code_drop==corp_df.regi_code, 'left_outer')
jobposting_df = jobposting_df.withColumn('corp_nm', when(jobposting_df.corp_nm.isNull(), jobposting_df.corp_nm_drop1).otherwise(jobposting_df.corp_nm))\
.drop(col('regi_code_drop')).drop(col('corp_nm_drop1')).drop(col('corp_nm_drop2'))


##########jobposting_jobs table##########

jobs_df0=df_id.select('jobposting_id', 'jobs', 'exp', 'questions', 'words')

# 형식은 list이지만, 실제로는 string타입인 컬럼들(jobs, exp, questions, words) split()으로 리스트로 만들어 주기
jobs_array =jobs_df0.withColumn('jobs', regexp_replace('jobs', "^\['", '')).withColumn('jobs', regexp_replace('jobs', "'\]$", ''))\
.withColumn('exp', regexp_replace('exp', "^\['", '')).withColumn('exp', regexp_replace('exp', "'\]$", ''))\
.withColumn('questions', regexp_replace('questions', '^\[\[', '')).withColumn('questions', regexp_replace('questions', '\]\]$', ''))\
.withColumn('words', regexp_replace('words', '^\[\[', '')).withColumn('words', regexp_replace('words', '\]\]$', ''))\
.select(col('jobposting_id'), split(col('jobs'), "', '").alias('job'), split(col('exp'), "', '").alias('new_or_exp'), split(col('questions'), '\], \[').alias('questions'), split(col('words'), '\], \[').alias('words'))

# explode 써서 리스트 풀기 + jobs_id 추가
jobs_explode1 = jobs_array.select('jobposting_id', explode(jobs_array.job).alias('job'))\
.coalesce(1).select(monotonically_increasing_id().alias('jobs_id'), expr('*')).withColumn('jobs_id', col('jobs_id')+1)
jobs_explode2 = jobs_array.select(col('jobposting_id').alias('jobposting_id2'), explode(jobs_array.new_or_exp).alias('new_or_exp'))\
.coalesce(1).select(monotonically_increasing_id().alias('jobs_id'), expr('*')).withColumn('jobs_id', col('jobs_id')+1)
jobs_explode3 = jobs_array.select(col('jobposting_id').alias('jobposting_id3'), explode(jobs_array.questions).alias('questions'))\
.coalesce(1).select(monotonically_increasing_id().alias('jobs_id'), expr('*')).withColumn('jobs_id', col('jobs_id')+1)
jobs_explode4 = jobs_array.select(col('jobposting_id').alias('jobposting_id4'), explode(jobs_array.words).alias('words'))\
.coalesce(1).select(monotonically_increasing_id().alias('jobs_id'), expr('*')).withColumn('jobs_id', col('jobs_id')+1)


# jobs_id 기준으로 join
explode_df = jobs_explode1.join(jobs_explode2, 'jobs_id', 'left').join(jobs_explode3, 'jobs_id', 'left').join(jobs_explode4, 'jobs_id', 'left')

##### spark로 처리 안 되는 일부행 제거
lst2 = [152, 949, 1282, 1475, 3200, 4401]
explode_df = explode_df.filter(~explode_df.jobs_id.isin(lst2)).drop('jobs_id').coalesce(1).select(monotonically_increasing_id().alias('jobs_id'), expr('*')).withColumn('jobs_id', col('jobs_id')+1)
#################################

jobs_df = explode_df.select(col('jobs_id'), col('jobposting_id'), col('job'), col('new_or_exp'))



##########cvletter_items table##########

items_df0 = explode_df.select(col('jobs_id'), col('questions'), col('words'))

# 이중 list형식이지만 실제로는 string타입인 컬럼들(questions, words) split()으로 리스트로 만들어 주기
items_array = items_df0.withColumn('questions', regexp_replace('questions', "^'", '')).withColumn('questions', regexp_replace('questions', "'$", ''))\
.withColumn('words', regexp_replace('words', "^'", '')).withColumn('words', regexp_replace('words', "'$", ''))\
.select(col('jobs_id'), split(col('questions'), "', '").alias('question'), split(col('words'), "', '").alias('word'))

# explode 써서 리스트 풀기 + items_id 추가
items_explode1 = items_array.select('jobs_id', explode(items_array.question).alias('question'))\
.coalesce(1).select(monotonically_increasing_id().alias('items_id'), expr('*')).withColumn('items_id', col('items_id')+1)
items_explode2 = items_array.select(col('jobs_id').alias('jobs_id2'), explode(items_array.word).alias('word'))\
.coalesce(1).select(monotonically_increasing_id().alias('items_id'), expr('*')).withColumn('items_id', col('items_id')+1)


items_explode_df = items_explode1.join(items_explode2, 'items_id', 'left')
items_df = items_explode_df.drop('jobs_id2')


##### db 넣기 #####

jobposting_df.write.jdbc(url, "jobposting", "append", properties={"driver": driver, "user": user, "password": password})
jobs_df.write.jdbc(url, "jobposting_jobs", "append", properties={"driver": driver, "user": user, "password": password})
items_df.write.jdbc(url, "cvletter_items", "append", properties={"driver": driver, "user": user, "password": password})