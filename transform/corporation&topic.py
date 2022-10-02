from pyspark.sql.functions import lit, explode, col, arrays_zip, substring, regexp_replace, trim, desc, split
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("yarn") \
    .appName("corporation&topic") \
    .getOrCreate()

# MySQL 연결 설정
user = "admin"
password = "qwer1234"
url = "jdbc:mysql://35.79.77.17:3306/pjt3"
driver = "com.mysql.cj.jdbc.Driver"
dbtable1 = "topic"
dbtable2 = "corporation"
dbtable3 = 'corp_toal_info'
## 기업 정보 데이터 가공  => 파일 갱신해야함(숫자 -> 문자로바꾼 csv파일로) : corporation 테이블로 들어감
df_info = spark.read.option("header", "true")\
                    .option("multiline", "true")\
                    .option('escape', '"')\
                    .csv("corp_data/corp_total.csv")\
                    .drop('status', 'message', 'corp_cls', 'ir_url', 'induty_code', 'acc_mt', 'bizr_no', 'hm_url', 'fax_no', 'jurir_no')\
                    .distinct()\
                    .sort(col('corp_name'), col('est_dt'))\
                    .withColumn('corp_name', regexp_replace(col('corp_name'), r'\(.*\)|\s-\s.*', ''))\
                    .drop_duplicates(['corp_name'])\
                    .withColumnRenamed('corp_name', 'corp_nm')\
                    .withColumnRenamed('corp_name_eng', 'corp_nm_eng')\
                    .withColumnRenamed('adres', 'address')\
                    .withColumnRenamed('corp_code', 'regi_code')\
                    .withColumnRenamed('stock_name', 'stock_nm')\
                    .select('regi_code', 'corp_nm', 'corp_nm_eng', 'ceo_nm', 'address', 'phn_no', 'est_dt', 'stock_code', 'stock_nm')\
                    .withColumn('est_dt', regexp_replace(col('est_dt'), '2130129', '20130129'))\
                    .withColumn('est_dt', regexp_replace(col('est_dt'), '20890525', ''))\
                    .withColumn('est_dt', regexp_replace(col('est_dt'), '20261019', ''))\
                    .sort(desc('est_dt'))


## 기업뉴스데이터 가공

# 파일불러오기(293259)
df_news = spark.read.option("header", "true")\
                    .option("multiline", "true")\
                    .option('escape', '"')\
                    .csv("corp_news/news_raw*.csv")\
                    .withColumnRenamed('corp_nn', 'corp_nm')\
                    .na.drop("any", subset=["corp_nm"])\
                    .distinct()

# 기사 주소만 있는것들 따로 빼놓기(2390)
df2 = df_news.where(col('keyword').isNull())\
             .withColumn('keyword1', split(col('keyword'), ' ').getItem(0))\
             .withColumn('keyword2', split(col('keyword'), ' ').getItem(2))\
             .withColumn('keyword3', split(col('keyword'), ' ').getItem(4))\
             .drop('keyword')

# 기초가공 (279421)
df_news = df_news.withColumn('corp_nm', regexp_replace(col('corp_nm'), r'\(.*\)|\s-\s.*', '')) \
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
                 .withColumn('keyword', regexp_replace(col('keyword'), '|', '')) \
                 .filter(~col('keyword').contains('스포츠'))\
                 .withColumn('keyword1', split(col('keyword'), ' ').getItem(0))\
                 .withColumn('keyword2', split(col('keyword'), ' ').getItem(2))\
                 .withColumn('keyword3', split(col('keyword'), ' ').getItem(4))\
                 .drop('keyword')


# 스포츠/부고/인사 기사 제거 , 에스씨케이컴퍼니는 쓸수없어서 드랍(278715)
df_news = df_news.filter(~col('title').contains('[인사]'))\
                 .filter(~col('title').contains('[부고'))\
                 .where(col('corp_nm') != '에스씨케이컴퍼니')\
                 .union(df2)\
                 .sort('corp_nm', desc('date'))\
                 .distinct()




# topic 테이블 만들기
df_joined1 = df_news.join(df_info, 'corp_nm', 'inner').select(df_news['*'], df_info['regi_code'])
df_joined2 = df_news.join(df_info, df_news.corp_nm == df_info.stock_nm, 'inner').select(df_news['*'], df_info['regi_code'])
df_topic = df_joined1.union(df_joined2).distinct().select('regi_code', 'corp_nm', 'date', 'title', 'content', 'url', 'keyword1', 'keyword2', 'keyword3').sort('corp_nm', desc('date'))

# corporation 테이블 만들기
df_joined3 = df_info.join(df_news, 'corp_nm', 'left').select(df_info['*'], df_news['category'])
df_joined4 = df_info.join(df_news, df_news.corp_nm == df_info.stock_nm, 'left').select(df_info['*'], df_news['category'])
df_corporation = df_joined3.union(df_joined4).distinct().select('regi_code', 'corp_nm', 'corp_nm_eng', 'category', 'ceo_nm', 'address', 'phn_no', 'est_dt', 'stock_code', 'stock_nm').sort(desc('est_dt'))

# MySQL 적재(db : pjt3, table : topic)
df_topic.write.jdbc(url, dbtable1, "append", properties={"driver": driver, "user": user, "password": password})
# MySQL 적재(db : pjt3, table : corporation)
df_corporation.write.jdbc(url, dbtable2, "append", properties={"driver": driver, "user": user, "password": password})


# 운영용 table(corp_info)
df_total = df_corporation.join(df_fin, 'regi_code', 'left').select(df_corporation['*'], 
                                            df_fin['year'], df_fin['total_assets'], df_fin['total_debt'], df_fin['total_capital'], 
                                            df_fin['total_sales'], df_fin['operating_income'], df_fin['net_income']
                                            ).sort(desc('est_dt'))


df_total.write.jdbc(url, dbtable3, "append", properties={"driver": driver, "user": user, "password": password})
