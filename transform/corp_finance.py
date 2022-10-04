from pyspark.sql.functions import lit, explode, col, arrays_zip, substring, regexp_replace, trim, desc
from pyspark.sql import SparkSession

"""
corp_code : 기업고유번호 => regi_code
bsns_year : 사업연도 => year
stock_code : 상장회사의 종목코드
thstrm_amount6 : 총자산 => total_assets
thstrm_amount8 : 총부채 => total_debt
thstrm_amount10 : 총자본 => total_captial
thstrm_amount12 : 총매출 => total_sales
thstrm_amount14 : 영업이익 => operation_income
thstrm_amount16 : 당기순이익 => net_income
"""

spark = SparkSession.builder \
    .master("yarn") \
    .appName("corp_finance") \
    .getOrCreate()

# MySQL 연결 설정
user = "root"
password = "qwer1234"
url = "jdbc:mysql://35.79.77.17:3306/pjt3"
driver = "com.mysql.cj.jdbc.Driver"
dbtable = "corp_finance"

df_fin = spark.read.option("header", "true")\
                    .option("multiline", "true")\
                    .option('escape', '"')\
                    .csv("corp_data/corp_findata.csv")\
                    .distinct()\
                    .select(col('corp_code').alias('regi_code'),
                            col('bsns_year').alias('year'),
                            col('stock_code'),
                            col('thstrm_amount6').alias('total_assets'),
                            col('thstrm_amount8').alias('total_debt'),
                            col('thstrm_amount10').alias('total_capital'),
                            col('thstrm_amount12').alias('total_sales'),
                            col('thstrm_amount14').alias('operating_income'),
                            col('thstrm_amount16').alias('net_income')
                            )

df_fin.write.jdbc(url, dbtable, "append", properties={"driver": driver, "user": user, "password": password})