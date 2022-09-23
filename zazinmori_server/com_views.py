from pprint import pprint
import django
from time import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Avg,Q

from .models import *
import datetime

# 기업 검색 결과 : 기업 기본정보, 재무정보, 현재 채용 정보
def search_company(request):
    context={}
    if request.method == "GET":
        context['message'] = "search company"
        context['user_email'] = request.session.get('user_email', '')
        return render(request, 'search.html', {'context':context})
    elif request.method == "POST" :
        #try:
        req_corp_nm = request.POST.get('corp_nm', False)
        com_info = Corporation.objects.filter(corp_nm__contains=req_corp_nm)
        context['corp_num'] = len(com_info)
        corps = {}
        for i in range(len(com_info)):
            corp_dict = {}
            corp_dict['corp_nm'] = com_info[i].corp_nm
            corp_dict['regi_code'] = com_info[i].regi_code
            corp_dict['address'] = com_info[i].address
            corp_dict['ceo_nm'] = com_info[i].ceo_nm
            corp_dict['est_dt'] = com_info[i].est_dt
            corp_dict['category'] = com_info[i].category
            corps[f'{i}'] = corp_dict
        context['corps'] = corps

        return JsonResponse(context, status=200)



def company_detail(request):
    context = {}

    req_regi_code = request.POST['regi_code']

    com_info = Corporation.objects.filter(regi_code=req_regi_code)
    context['com_info'] = com_info.values()[0]

    try:
        com_finance = Corp_finance.objects.filter(regi_code=req_regi_code)
        context['com_finance'] = com_finance.values()[0]
    except:
        context['com_finance'] = ''

    com_recruits = Jobposting.objects.filter(regi_code=req_regi_code)
    context['recruit_num'] = len(com_recruits)
    for i in range(len(com_recruits)):
        recruit_dict = {}
        recruit_dict[f'{i}'] = com_recruits.values()[i]    
    context['com_recruits'] = recruit_dict
    

    return JsonResponse(context, status=200)
    # except django.db.utils.OperationalError :
    #     return JsonResponse({'err':"테이블 없음"}, status=400)
    # except Exception as err:
    #     return JsonResponse({"err": err})


def recruit_company(request, jobposting_id):
    context={}
    if request.method == "GET":
        # return render(request, '채용 공고 정보 페이지.html')
        try:
            context['message'] = f"채용 공고 정보 페이지 {jobposting_id}번 회사 채용공고"
            req_corp_nm = request.GET.get('corp_nm', None)
            
            if req_corp_nm is None :
                return redirect('/')
            
            com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
            # job_postings = Job_posting.objects.filter(corp_id=com_info.corp_id)
            # job_posting_jobs = Jobposting_job.objects.filter(Jobposting_id=job_postings.jobposting_id)
            job_postings = Jobposting.objects.filter(jobposting_id=jobposting_id)
            job_posting_jobs = Jobposting_jobs.objects.filter(jobposting_id=jobposting_id)

            context['corp_nm'] = com_info.first().corp_nm
            context['job_postings'] = job_postings.values()[0]
            context['job_posting_job']=job_posting_jobs.values()[0]
            return JsonResponse(context, status=200)

        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})


def recruit_positions(request, jobposting_id): # 수정필요
    context={}
    if request.method == "GET":
        try:
            req_corp_nm = request.GET.get('corp_nm', None)
            print(req_corp_nm)
            if req_corp_nm is None :
                return redirect('/')
            #     return JsonResponse({"err" : "값을 입력해 주세요"}, status=400)
            
            com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
            job_postings = Jobposting.objects.filter(jobposting_id=jobposting_id)
            job_posting_jobs = Jobposting_jobs.objects.filter(jobposting_id=job_postings.first().jobposting_id)
            
            context['corp_nm'] = com_info.first().corp_nm
            context['job_postings'] = job_postings.values()[0]
            context['job_posting_job']=job_posting_jobs.values()[0]
            return JsonResponse(context, status=200)
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})