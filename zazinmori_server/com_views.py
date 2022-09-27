from pprint import pprint

import django

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Avg,Q
from elasticsearch import Elasticsearch
from .loggers import logging_search, logging_user_target,logging_click
from .env_settings import ES_ID, ES_URL, ES_PW
from .models import *
from datetime import datetime


def search_company(request):
    context={}
    if request.method == "GET":
        context['message'] = "search company"
        context['user_email'] = request.session.get('user_email', False)
        
        logging_click(request)
        return render(request, 'search.html', {'context':context})
    elif request.method == "POST":
        req_corp_nm = request.POST.get('corp_nm', False)
        logging_search(request, req_corp_nm)
        
        es = Elasticsearch(
        ES_URL,
        basic_auth=(ES_ID, ES_PW)
        )
        resp = es.search(index="corp_total_info", query={"multi_match": {"query": req_corp_nm, "fields": ["corp_nm", "corp_nm_eng"]}})
        resp_list = resp['hits']['hits']
        search_list = []
        # 기초 가공
        for i in resp_list:
            del i['_source']['@timestamp'], i['_source']['@version']
            search_list.append(i['_source'])

        context['corp_result'] = search_list
        context['corp_num'] = len(search_list)
        # from pprint import pprint
        # pprint(context['corp_result'])
        logging_click(request)
        
        return JsonResponse(context,status=200)
     

def company_detail(request):
    context = {}
    # 로그용 쿼리
    user = User_info.objects.filter(user_email=request.session.get("user_email",None)).first()
    req_regi_code = request.POST['regi_code']
    logging_user_target(request, user, com_recruits)

    com_recruits = Jobposting.objects.filter(regi_code=req_regi_code)
    context['recruit_num'] = len(com_recruits)
    recruit_dict = {}
    for i in range(len(com_recruits)):
        recruit_dict[f'{i}'] = com_recruits.values()[i]    
    context['com_recruits'] = recruit_dict
    

    return JsonResponse(context, status=200)
    # except django.db.utils.OperationalError :
    #     return JsonResponse({'err':"테이블 없음"}, status=400)
    # except Exception as err:
    #     return JsonResponse({"err": err})


def recruits(request):
    context={}    
    # post방식으로만 통신
    try:
        jobposting_id = request.POST['jobposting_id']

        jobposting = Jobposting.objects.filter(jobposting_id=jobposting_id) #1개
        jobposting_jobs = Jobposting_jobs.objects.filter(jobposting_id=jobposting_id) #여러개

        context['jobposting_id'] = jobposting[0].jobposting_id
        context['corp_nm'] = jobposting[0].corp_nm
        context['posting_type'] = jobposting[0].posting_type
        
        posting_detail = jobposting[0].posting_detail
        posting_detail = posting_detail[2:]
        posting_detail = posting_detail[:-2]
        context['posting_detail'] = posting_detail
        
        if jobposting[0].posting_type == 'img':
            src_text = jobposting[0].posting_detail
            src_lst = src_text.split("], [")
            context['src_num'] = len(src_lst)
            src_dict = {}
            for j in range(len(src_lst)):
                src_dict[f'{j}'] = src_lst[j].replace('[', '').replace(']', '').replace('"', '').replace("'", "")
            context['src'] = src_dict
            
        context['job_num'] = len(jobposting_jobs)
        jobs_dict = {}       
        for i in range(len(jobposting_jobs)):            
            jobs_dict[f'{i}'] = jobposting_jobs.values()[i]
                
        context['jobs'] = jobs_dict
        logging_click(request)
        return JsonResponse(context, status=200)

    except django.db.utils.OperationalError :
        return JsonResponse({'err':"테이블 없음"}, status=400)
    except Exception as err:
        return JsonResponse({"err": err})

    
    
def scrap(request):
    context = {}
    try:    
        req_jobposting_id = request.POST.get('jobposting_id', False)
        req_email = request.session.get('user_email', False)
        req_member_id = User_info.objects.get(email=req_email).member_id        
        logging_click(request)
        # 이미 스크랩했는지 체크
        scrap_exist = User_scrap.objects.filter(member_id=req_member_id, jobposting_id=req_jobposting_id)
        if scrap_exist.exists():
            context['scrap_chk'] = 1
            return JsonResponse(context, status=200)
        # 기존 스크랩 내역 없으면 스크랩
        else:
            context['scrap_chk'] = 0
            User_scrap.objects.create(
                member_id = req_member_id,
                jobposting_id = int(req_jobposting_id)
            )
        return JsonResponse(context, status=200)
        
    except django.db.utils.OperationalError :
        return JsonResponse({'err':"테이블 없음"}, status=400)
    except Exception as err:
        return JsonResponse({"err": err})



# def recruit_positions(request, jobposting_id): # 수정필요
#     context={}
#     if request.method == "GET":
#         try:
#             req_corp_nm = request.GET.get('corp_nm', None)
#             print(req_corp_nm)
#             if req_corp_nm is None :
#                 return redirect('/')
#             #     return JsonResponse({"err" : "값을 입력해 주세요"}, status=400)
            
#             com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
#             job_postings = Jobposting.objects.filter(jobposting_id=jobposting_id)
#             job_posting_jobs = Jobposting_jobs.objects.filter(jobposting_id=job_postings.first().jobposting_id)
            
#             context['corp_nm'] = com_info.first().corp_nm
#             context['job_postings'] = job_postings.values()[0]
#             context['job_posting_job']=job_posting_jobs.values()[0]
#             return JsonResponse(context, status=200)
#         except django.db.utils.OperationalError :
#             return JsonResponse({'err':"테이블 없음"}, status=400)
#         except Exception as err:
#             return JsonResponse({"err": err})
