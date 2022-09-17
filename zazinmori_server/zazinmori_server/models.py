from gc import DEBUG_COLLECTABLE
from unicodedata import category
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.

class User(models.Model):
    # 프라이머리키
    member_id = models.AutoField(db_column='member_id', primary_key=True)
    name = models.CharField(db_column='name', max_length=50)
    email = models.CharField(db_column='email', max_length=50)
    passwd = models.CharField(db_column='passwd', max_length=50)
    birth = models.DateField(db_column='birthday', auto_now_add=False)
    reg_date = models.DateTimeField(db_column='reg_date', auto_now_add=True)
    update_date = models.DateTimeField(db_column='update_date', auto_now_add=True)
 
    class Meta:
        managed = False
        db_table = 'users'
 
    def __str__(self):
        return '이름 : ' + self.name + ", 이메일 : " + self.email
    
class User_scraps(models.Model):
    # 프라이머리키
    scrap_id = models.AutoField(db_column='member_id', primary_key=True)
    member_id = models.IntegerField(db_column='memeber_id', max_length=50)
    jobposting_id = models.CharField(db_column='jobposting_id', max_length=50)
 
    class Meta:
        managed = False
        db_table = 'user_scraps'
    
class Corporation(models.Model):
    # 프라이머리키
    corp_id = models.AutoField(db_column='regi_code', primary_key=True)
    corp_nm = models.CharField(db_column='corp_nm', max_length=45)
    category = models.CharField(db_column='email', max_length=45)
    president = models.CharField(db_column='passwd', max_length=45)
    stock = models.CharField(db_column='stock', max_length=45)
    
    class Meta:
        managed=False
        db_table = 'corporations'

class Corp_finance(models.Model):
    # 프라이머리키
    finance_id = models.AutoField(db_column='regi_code', primary_key=True)
    # 외래키
    corp_id = models.IntegerField(db_column='corp_nm')
    date = models.DateField(db_column='date',auto_now_add=False)
    stock = models.CharField(db_column='stock', max_length=45)
    total_sales = models.FloatField(db_column='total_sales', max_length=100)
    profit = models.FloatField(db_column='profit', max_length=100)
    
    class Meta:
        managed=False
        db_table = 'corp_finances'
        
class Concept(models.Model):
    concept_id = models.AutoField(db_column='concept_id', primary_key=True)
    # 외래키
    corp_id = models.IntegerField(db_column='corp_id')
    date = models.DateField(db_column='date', auto_now_add=False)
    concept = models.CharField(db_column='concept', max_length=45)
    
    class Meta:
        managed=False
        db_table = 'concepts'

class Topic(models.Model):
    topic_id = models.AutoField(db_column='topic_id', primary_key=True)
    corp_id = models.IntegerField(db_column='corp_id')
    corp_nm = models.CharField(db_column='corp_nm', max_length=45)
    date = models.DateField(db_column='date', auto_now_add=False)
    title = models.CharField(db_column='title', max_length=45)
    context = models.TextField(db_column='context')
    url = models.CharField(db_column='url', max_length=45)
    keyword = models.CharField(db_column='keyword', max_length=45)
    
    class Meta:
        managed=False
        db_table = 'topic'

class Job_posting(models.Model):
    jobposting_id = models.AutoField(db_column='jobposting_id', primary_key=True)
    corp_id = models.IntegerField(db_column='corp_id')
    period = models.CharField(db_column='period', max_length=45)
    start_date = models.DateField(db_column='start_date', auto_now_add=False)
    end_date = models.DateField(db_column='end_date', auto_now_add=False)
    posting_detail= models.TextField(db_column='posting_detail')
    
    class Meta:
        managed=False
        db_table = 'job_postings'

class passcvletter(models.Modle):
    cvletter_id = models.AutoField(db_column='cvletter_id',primary_key=True)
    # 외래키
    corp_id = models.IntegerField(db_column='corp_id')
    corp_nm = models.CharField(db_column='corp_nm', max_length=45)
    job = models.CharField(db_column='job', max_length=45)
    employment_date = models.DateField(db_column='employment_date', auto_now_add=False)
    new_or_exp = models.CharField(db_column='new_or_exp', max_length=45)
    question = models.TextField(db_column='question')
    question_type = models.CharField(db_column='question_type', max_length=45)
    answer = models.TextField(db_column='answer')
    class Meta:
        managed=False
        db_table = 'passcvletter'

class Jobposting_job(models.Model):
    jobs_id = models.AutoField(db_column='jobs_id', primary_key=True)
    # 외래키
    jobposting_id = models.IntegerField(db_column='jobposting_id')
    job = models.CharField(db_column='job', max_length=45)
    new_or_exp = models.CharField(db_column='new_or_exp', max_length=45)
    class Meta:
        managed=False
        db_table = 'jobpostiong_job'

class Cvletter_items(models.Model):
    cvletter_items_id = models.AutoField(db_column='cvletter_items_id', primary_key=True)
    # 외래키
    jobs_id = models.IntegerField(db_column='jobs_id')
    question = models.TextField(db_column='question')
    cvletter_itemscol = models.CharField(db_column='cvletter_itemscol', max_length=45)
    
    
class User_cvletter(models.Model) :
    # 프라이머리키
    user_cvletter_id = models.AutoField(db_column='user_cvletter_id', primary_key = True)
    # 외래키
    member_id = models.CharField(db_column='memeber_id', max_length=45)
    written_name = models.CharField(db_column='written_name', max_length=200)
    written_date = models.DateField(db_column='written_date', auto_now_add=False)
    update_date = models.DateField(db_column='written_date', auto_now_add=False)
    q1 = models.TextField(db_column='q1')
    a1 = models.TextField(db_column='a1')
    q2 = models.TextField(db_column='q2')
    a2 = models.TextField(db_column='a2')
    q3 = models.TextField(db_column='q3')
    a3 = models.TextField(db_column='a3')
    q4 = models.TextField(db_column='q4')
    a4 = models.TextField(db_column='a4')
    q5 = models.TextField(db_column='q5')
    a5 = models.TextField(db_column='a5')
    q6 = models.TextField(db_column='q6')
    a6 = models.TextField(db_column='a6')
    q7 = models.TextField(db_column='q7')
    a7 = models.TextField(db_column='a7')
    q8 = models.TextField(db_column='q8')
    a8 = models.TextField(db_column='a8')