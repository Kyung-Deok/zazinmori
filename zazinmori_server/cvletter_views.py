from unittest import result
from django.shortcuts import render
# import bcrypt
# import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .loggers import logging_click
from datetime import datetime
from django.http import JsonResponse
import json
import requests

from .models import *

def doc2vec_call(corp_nm) :
    results={}
    #res = requests.post('http://localhost:8988/prediction/cvl_corp_nm', json={"corp_nm" : request.POST.get("corp_nm", '현대자동차')})
    res = requests.post('http://35.79.77.17:8988/prediction/cvl_corp_nm/', json={"corp_nm" : corp_nm})
    results['results'] = res.json()
    return results


# 자소서 문항 텍스트 입력하면 질문유형(int, text) 반환하는 함수
def qtype(question):
    category0 = ['사회', '이슈', '뉴스'] #5
    category1 = ['성장', '학창', '대학', '가족'] #2
    category2 = ['성격', '장점', '단점', '보완'] #4
    category3 = ['핵심', '역량', '특별', '직무와'] #3
    category4 = ['갈등', '경험', '해결', '노력'] #1
    category5 = ['지원', '동기', '목표', '포부'] #0    
    result = {}
    for i in range(6):
        for word in category0:
            if question.find(word) >= 0:
                result['int'], result['text'] = 5, '사회이슈'
                return result
        for word in category1:
            if question.find(word) >= 0:
                result['int'], result['text'] = 2, '성장과정'
                return result
        for word in category2:
            if question.find(word) >=0:
                result['int'], result['text'] = 4, '성격유형'
                return result
        for word in category3:
            if question.find(word) >=0:
                result['int'], result['text'] = 3, '직무역량'
                return result
        for word in category4:
            if question.find(word) >=0:
                result['int'], result['text'] = 1, '갈등해결'
                return result
        for word in category5:
            if question.find(word) >=0:
                result['int'], result['text'] = 0, '지원동기'
                return result
    result['int'], result['text'] = 6, '기타'
    return result




def cvletter_write(request, jobs_id):
    context = {}
    user_email = request.session.get('user_email', False)
    context['user_email'] = user_email
    context['jobs_id'] = jobs_id
    
    if request.method == "GET":
        cvletter_items = Cvletter_items.objects.filter(jobs_id=jobs_id)
        job = Jobposting_jobs.objects.filter(jobs_id=jobs_id)[0].job
        context['job'] = job
        jobposting_id = Jobposting_jobs.objects.filter(jobs_id=jobs_id)[0].jobposting_id
        jobposting = Jobposting.objects.filter(jobposting_id=jobposting_id)[0]
        corp_nm = jobposting.corp_nm
        start_time = jobposting.start_time
        end_time = jobposting.end_time
        context['corp_nm'] = corp_nm
        context['start_time'] = start_time[:10]
        context['end_time'] = end_time[:10]
        context['regi_code'] = jobposting.regi_code
                
        items = []
        logging_click(request)
        for i in range(len(cvletter_items)):
            item = {}
            question = cvletter_items[i].question.split('\\')[0]
            item['question'] = question
            item['qtype_text'] = qtype(question)['text']
            item['word'] = cvletter_items[i].word
            item['num'] = i
            
            # 모델 결과 리스트에 추가
            try:
                jobposting_id = Jobposting_jobs.objects.filter(jobs_id=jobs_id).first().jobposting_id
                corp_nm = Jobposting.objects.filter(jobposting_id=jobposting_id).first().corp_nm
                model_result = doc2vec_call(corp_nm)
                type_num = qtype(question)['int']
                keys = list(model_result['results'].keys())
                item['corp1'] = model_result['results'][keys[type_num]][0][0]
                item['corp2'] = model_result['results'][keys[type_num]][1][0]
                item['corp3'] = model_result['results'][keys[type_num]][2][0]
                item['corp4'] = model_result['results'][keys[type_num]][3][0]
                item['corp5'] = model_result['results'][keys[type_num]][4][0]             
            except:
                item['corp1'] = '데이터부족'
                item['corp2'] = '데이터부족'
                item['corp3'] = '데이터부족'
                item['corp4'] = '데이터부족'
                item['corp5'] = '데이터부족'
                
            items.append(item)
        context['items'] = items 
        
        return render(request, 'writing.html', {'context': context})
    
    else:
        user_info = User_info.objects.filter(email=user_email)
        member_id = user_info[0].member_id
        req_data = json.loads(request.body)
        jobs_id = req_data['jobs_id']
        item_num = req_data['item_num']
        q_dict = req_data['q_dict']
        a_dict = req_data['a_dict']
        w_dict = req_data['w_dict']
        
        User_cvletter.objects.create(
            member_id = member_id,
            jobs_id = jobs_id,
            written_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        user_cvletter = User_cvletter.objects.filter(member_id=member_id).order_by('user_cvletter_id')
        user_cvletter_id = user_cvletter.last().user_cvletter_id
        
        for i in range(item_num):
            key = str(i)
            User_cvletter_items.objects.create(
                user_cvletter_id=user_cvletter_id,
                question=q_dict[f'{key}'],
                answer=a_dict[f'{key}'],
                word=w_dict[f'{key}']
            )        
        
        context['user_cvletter_id'] = 'user_cvletter_id'
        logging_click(request)

        return JsonResponse(context, status=200)
    
    
    

def user_cvletter_update(request, cvl_id):
    user_email = request.session.get('user_email', False)
    context = {}
    context['user_email'] = user_email
    
    if request.method == "GET":
    # GET 일 때, 회원정보를 우선 띄워준다.    
        try : 
            # 세션 email이랑 유저의 email이 맞는지 확인
            # 로그인한 유저가 맞는지 확인
            # 아니라면 로그인 페이지로 리다이렉트
            login_member_id = User_info.objects.filter(email = user_email).first().member_id
            cvletter_member_id = User_cvletter.objects.filter(user_cvletter_id=cvl_id).first().member_id
            jobs_id = User_cvletter.objects.filter(user_cvletter_id=cvl_id).first().jobs_id
            
            job = Jobposting_jobs.objects.filter(jobs_id=jobs_id)[0].job
            context['job'] = job
            jobposting_id = Jobposting_jobs.objects.filter(jobs_id=jobs_id)[0].jobposting_id
            jobposting = Jobposting.objects.filter(jobposting_id=jobposting_id)[0]
            corp_nm = jobposting.corp_nm
            start_time = jobposting.start_time
            end_time = jobposting.end_time
            context['corp_nm'] = corp_nm
            context['start_time'] = start_time[:10]
            context['end_time'] = end_time[:10]
            context['regi_code'] = jobposting.regi_code
            
            if int(login_member_id) != int(cvletter_member_id) :
                return redirect('/login/')
            else :                
                user_cvletter_items = User_cvletter_items.objects.filter(user_cvletter_id=cvl_id)
                if not user_cvletter_items.exists() :
                    context['err'] = "해당 자소서가 없습니다."
                    return JsonResponse(context, status=400)
                else :
                    items = []
                    for i in range(len(user_cvletter_items)):
                        item = {}
                        question = user_cvletter_items[i].question
                        item['question'] = question
                        item['qtype_text'] = qtype(question)['text']
                        item['word'] = user_cvletter_items[i].word
                        item['answer'] = user_cvletter_items[i].answer
                        item['user_cvitems_id'] = user_cvletter_items[i].user_cvitems_id
                        item['num'] = i
                        
                        # 모델 결과 리스트에 추가
                        try:
                            jobposting_id = Jobposting_jobs.objects.filter(jobs_id=jobs_id).first().jobposting_id
                            corp_nm = Jobposting.objects.filter(jobposting_id=jobposting_id).first().corp_nm
                            model_result = doc2vec_call(corp_nm)
                            type_num = qtype(question)['int']
                            keys = list(model_result['results'].keys())
                            item['corp1'] = model_result['results'][keys[type_num]][0][0]
                            item['corp2'] = model_result['results'][keys[type_num]][1][0]
                            item['corp3'] = model_result['results'][keys[type_num]][2][0]
                            item['corp4'] = model_result['results'][keys[type_num]][3][0]
                            item['corp5'] = model_result['results'][keys[type_num]][4][0]             
                        except:
                            item['corp1'] = '데이터부족'
                            item['corp2'] = '데이터부족'
                            item['corp3'] = '데이터부족'
                            item['corp4'] = '데이터부족'
                            item['corp5'] = '데이터부족'
                        
                        items.append(item)
                    context['items'] = items
                    logging_click(request)
                    return render(request, 'cvletter_update.html', {'context': context})
        except Exception as err : 
            return JsonResponse({'err' : err}, status=500)
        
    else :
        
        req_data = json.loads(request.body)
        item_num = req_data['item_num']
        id_dict = req_data['id_dict']
        a_dict = req_data['a_dict']
        
        for i in range(item_num):
            key = str(i)
            user_cvitems_id = id_dict[f'{key}']
            cvletter_items = User_cvletter_items.objects.filter(user_cvitems_id = user_cvitems_id)
            cvletter_items.update(
                answer = a_dict[f'{key}']
            )
            
            user_cvletter_id = cvletter_items[0].user_cvletter_id
            cvletters = User_cvletter.objects.filter(user_cvletter_id = user_cvletter_id)
            cvletters.update(
                written_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        
        context['message'] = '자소서 수정 완료'
        logging_click(request)
        return JsonResponse(context, status=200)