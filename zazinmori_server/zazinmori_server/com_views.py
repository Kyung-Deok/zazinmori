import json
from pprint import pprint
import django
from time import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Sum, Avg,Q

from .models import *
import datetime

def search_company(request):
    if request.method == "GET":
        return render(request, '기업 상세정보 페이지.html')
    elif request.method == "POST" :
        context={}
        try:
            req_corp_nm = request.POST.get('corp_nm', None)
            if req_corp_nm is None :
                return JsonResponse({"err" : "값을 입력해 주세요"}, status=400)
                # return redirect('/api/companys')
                
            com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
            com_finance = Corp_finance.objects.filter(corp_id = com_info.corp_id)
            com_concept = Concept.objects.filter(corp_id = com_info.corp_id)
            com_recruits= Job_posting.objects.filter(corp_id=com_info.corp_id)
            
            context['com_info']= com_info
            context['com_finance'] = com_finance
            context['com_concept'] = com_concept
            context['recruits'] = com_recruits
            
            return JsonResponse(context, status=200)
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})
        
def recruit_company(request):
    if request.method == "GET":
        return render(request, '채용 공고 정보 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            req_corp_nm = request.POST.get('corp_nm', None)
            if req_corp_nm is None :
                return JsonResponse({"err" : "값을 입력해 주세요"}, status=400)
                # return redirect('/api/companys')
            
            com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
            job_postings = Job_posting.objects.filter(corp_id=com_info.corp_id)
            job_posting_jobs = Jobposting_job.objects.filter(Jobposting_id=job_postings.jobposting_id)
            
            context['job_postings'] = job_postings
            context['job_posting_job']=job_posting_jobs
            
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})

def recruit_positions(request): # 수정필요
    if request.method == "GET":
        return render(request, '채용 상세 정보 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            req_corp_nm = request.POST.get('corp_nm', None)
            if req_corp_nm is None :
                return JsonResponse({"err" : "값을 입력해 주세요"}, status=400)
                # return redirect('/api/companys')
            
            com_info = Corporation.objects.filter(corp_nm=req_corp_nm)
            job_postings = Job_posting.objects.filter(corp_id=com_info.corp_id)
            job_posting_jobs = Jobposting_job.objects.filter(Jobposting_id=job_postings.jobposting_id)
            
            context['job_postings'] = job_postings
            context['job_posting_job']=job_posting_jobs

        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})