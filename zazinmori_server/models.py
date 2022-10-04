from django.db import models


class Concept(models.Model):
    concept_id = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    concept = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'concept'


class Corp_finance(models.Model):
    finance_id = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    year = models.CharField(max_length=45, blank=True, null=True)
    stock_code = models.CharField(max_length=45, blank=True, null=True)
    total_assets = models.CharField(max_length=45, blank=True, null=True)
    total_debt = models.CharField(max_length=45, blank=True, null=True)
    total_capital = models.CharField(max_length=45, blank=True, null=True)
    total_sales = models.CharField(max_length=45, blank=True, null=True)
    operating_income = models.CharField(max_length=45, blank=True, null=True)
    net_income = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corp_finance'


class Corporation(models.Model):
    regi_code = models.TextField(primary_key=True)
    # regi_code = models.TextField(blank=True, null=True)
    corp_nm = models.TextField(blank=True, null=True)
    corp_nm_eng = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    ceo_nm = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phn_no = models.TextField(blank=True, null=True)
    est_dt = models.TextField(blank=True, null=True)
    stock_code = models.TextField(blank=True, null=True)
    stock_nm = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'corporation'


class Cvletter_items(models.Model):
    items_id = models.TextField(primary_key=True)
    jobs_id = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cvletter_items'



class Failcvletter(models.Model):
    cvletter = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    corp_nm = models.TextField(blank=True, null=True)
    job = models.TextField(blank=True, null=True)
    recruit_date = models.TextField(blank=True, null=True)
    new_or_exp = models.TextField(blank=True, null=True)
    q1 = models.TextField(blank=True, null=True)
    a1 = models.TextField(blank=True, null=True)
    q2 = models.TextField(blank=True, null=True)
    a2 = models.TextField(blank=True, null=True)
    q3 = models.TextField(blank=True, null=True)
    a3 = models.TextField(blank=True, null=True)
    q4 = models.TextField(blank=True, null=True)
    a4 = models.TextField(blank=True, null=True)
    q5 = models.TextField(blank=True, null=True)
    a5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'failcvletter'


class Jobposting(models.Model):
    jobposting_id = models.TextField(primary_key=True)
    regi_code = models.TextField(blank=True, null=True)
    corp_nm = models.TextField(blank=True, null=True)
    period = models.TextField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)
    end_time = models.TextField(blank=True, null=True)
    posting_detail = models.TextField(blank=True, null=True)
    posting_type = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobposting'


class Jobposting_jobs(models.Model):
    jobs_id = models.TextField(primary_key=True)
    jobposting_id = models.TextField(blank=True, null=True)
    job = models.TextField(blank=True, null=True)
    new_or_exp = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'jobposting_jobs'


class Passcvletter(models.Model):
    passcvletter_code = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    corp_nm = models.TextField(blank=True, null=True)
    job = models.TextField(blank=True, null=True)
    recruit_date = models.TextField(blank=True, null=True)
    new_or_exp = models.TextField(blank=True, null=True)
    q1 = models.TextField(blank=True, null=True)
    a1 = models.TextField(blank=True, null=True)
    q2 = models.TextField(blank=True, null=True)
    a2 = models.TextField(blank=True, null=True)
    q3 = models.TextField(blank=True, null=True)
    a3 = models.TextField(blank=True, null=True)
    q4 = models.TextField(blank=True, null=True)
    a4 = models.TextField(blank=True, null=True)
    q5 = models.TextField(blank=True, null=True)
    a5 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passcvletter'


class Topic(models.Model):
    topic_id = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    corp_nm = models.CharField(max_length=45, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=150, blank=True, null=True)
    keyword1 = models.CharField(max_length=45, blank=True, null=True)
    keyword2 = models.CharField(max_length=45, blank=True, null=True)
    keyword3 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic'


# class User_cvletter(models.Model):
#     user_cvletter_id = models.AutoField(primary_key=True)
#     member_id = models.CharField(max_length=45, blank=True, null=True)
#     written_date = models.TextField(blank=True, null=True)
#     q1 = models.TextField(blank=True, null=True)
#     q2 = models.TextField(blank=True, null=True)
#     q3 = models.TextField(blank=True, null=True)
#     q4 = models.TextField(blank=True, null=True)
#     q5 = models.TextField(blank=True, null=True)
#     q6 = models.TextField(blank=True, null=True)
#     q7 = models.TextField(blank=True, null=True)
#     q8 = models.TextField(blank=True, null=True)
#     a1 = models.TextField(blank=True, null=True)
#     a2 = models.TextField(blank=True, null=True)
#     a3 = models.TextField(blank=True, null=True)
#     a4 = models.TextField(blank=True, null=True)
#     a5 = models.TextField(blank=True, null=True)
#     a6 = models.TextField(blank=True, null=True)
#     a7 = models.TextField(blank=True, null=True)
#     a8 = models.TextField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'user_cvletter'
        
class User_cvletter(models.Model):
    user_cvletter_id = models.AutoField(primary_key=True)
    jobs_id = models.CharField(max_length=45, blank=True, null=True)
    member_id = models.CharField(max_length=45, blank=True, null=True)
    written_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_cvletter'
        
        
class User_cvletter_items(models.Model):
    user_cvitems_id = models.AutoField(primary_key=True)
    user_cvletter_id = models.CharField(max_length=45, blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    word = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_cvletter_items'


class User_scrap(models.Model):
    scrap_id = models.AutoField(primary_key=True)
    member_id = models.CharField(max_length=45, blank=True, null=True)
    jobposting_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_scrap'


class User_info(models.Model):
    member_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    passwd = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    birth = models.CharField(max_length=45, blank=True, null=True)
    gender = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    category = models.CharField(max_length=45, blank=True, null=True)
    area = models.CharField(max_length=45, blank=True, null=True)
    salary = models.CharField(max_length=45, blank=True, null=True)
    reg_date = models.CharField(max_length=45, blank=True, null=True)
    update_date = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_info'
        
        
class Board(models.Model):
    post_id = models.AutoField(primary_key=True)
    member_id = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    written_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board'
        
        
class News_result(models.Model):
    news_result_id = models.AutoField(primary_key=True)
    regi_code = models.CharField(max_length=45, blank=True, null=True)
    corp_nm = models.TextField(max_length=45, blank=True, null=True)
    news_title = models.TextField(blank=True, null=True)
    news_sentence = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    keyword1 = models.CharField(max_length=45, blank=True, null=True)
    keyword2 = models.CharField(max_length=45, blank=True, null=True)
    keyword3 = models.CharField(max_length=45, blank=True, null=True)
    keyword4 = models.CharField(max_length=45, blank=True, null=True)
    keyword5 = models.CharField(max_length=45, blank=True, null=True)
    keyword6 = models.CharField(max_length=45, blank=True, null=True)
    keyword7 = models.CharField(max_length=45, blank=True, null=True)
    keyword8 = models.CharField(max_length=45, blank=True, null=True)
    keyword9 = models.CharField(max_length=45, blank=True, null=True)
    keyword10 = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_result'
