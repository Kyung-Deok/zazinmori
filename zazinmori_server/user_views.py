from email.policy import default
from time import strftime
from django.shortcuts import render
import bcrypt
import django

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse
from .env_settings import SALT

from .models import *
from .loggers import logging_click

# 마이페이지 초입 페이지
def user_info(request):
    context = {}
    context['user_email'] = request.session.get('user_email', False)
    if context['user_email']:
        user_email = context['user_email']
        user_info = User_info.objects.filter(email = user_email)
        context['user_info'] = user_info.values()[0]
    
    logging_click(request)
    return render(request, 'mypage.html', {'context': context})
  
    
def user_update(request):
    ses_user = request.session.get('user_email', None)
    user_info = User_info.objects.filter(email = ses_user)
    context = {}
    if request.method == "GET":
    # GET 일 때, 회원정보를 우선 띄워준다.
        try : 
            # 세션 email이랑 유저의 email이 맞는지 확인
            # 로그인한 유저가 맞는지 확인
            # 아니라면 로그인 페이지로 리다이렉트
            if user_info.exists() == False :
                print(user_info.exists())
                return redirect('/login/')
            else :
                context['message'] = "success"
                context['user_name'] = user_info.first().name
                context['user_email'] = user_info.first().email
                # context['user_passwd'] = user_info.first().passwd
                context['user_birth'] = user_info.first().birth
                context['user_gender'] = user_info.first().gender
                context['user_phone'] = user_info.first().phone
                context['user_category'] = user_info.first().category
                context['user_area'] = user_info.first().area
                context['user_salary'] = user_info.first().salary            
            #return JsonResponse(context, status=200)    
            logging_click(request)
            return render(request, 'user_update.html', {"context": context})
        except Exception as err : 
            return JsonResponse({'err' : err})
    elif request.method == "POST":
        
        # 비밀번호 일치하는지 확인
        req_passwd = request.POST.get('old_passwd', False)
        user_passwd = user_info.first().passwd
        check_user_passwd = bcrypt.checkpw(req_passwd.encode('utf-8'), user_passwd.encode('utf-8'))
        logging_click(request)
        if not check_user_passwd:
                context['err'] = "비밀번호 정보가 맞지 않습니다."
                return JsonResponse(context)
        # 비밀번호 일치하면 유저 정보 업데이트
        else :
            user_email = request.POST.get('req_email', False)
            new_passwd = request.POST.get('new_passwd', False)
            new_name = request.POST.get('req_name', False)
            new_birth = request.POST.get('req_birth', False)
            new_gender = request.POST.get('req_gender', False)
            new_phone = request.POST.get('req_phone', False)
            new_category = request.POST.get('req_category', False)
            new_area = request.POST.get('req_area', False)
            new_salary = request.POST.get('req_salary', False)
            
            user_info = User_info.objects.filter(email = user_email)
            user_info.update(
                passwd = bcrypt.hashpw(new_passwd.encode('utf-8'), bcrypt.gensalt(SALT)).decode('utf-8'),
                name = new_name,
                birth = new_birth,
                gender = new_gender,
                phone = new_phone,
                category = new_category,
                area = new_area,
                salary = new_salary,
                update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        context['message'] = '회원정보 변경 완료'
        context['user_update_date'] = user_info.first().update_date
        context['user_email'] = user_info.first().email
        logging_click(request)
        request.session.flush()
        
        return JsonResponse(context, status=200)
        # except django.db.utils.OperationalError :
        #         return JsonResponse({'err':"테이블 없음"}, status=400)
        # except Exception as err : 
        #     return JsonResponse({'err' : err})    


# 유저가 스크랩한 채용공고 목록 화면에 보여줌
def user_scrap(request):
    context = {}
    user_email = request.session.get('user_email', False)
    if user_email:
        member_id = User_info.objects.get(email=user_email).member_id
        scraps = User_scrap.objects.filter(member_id=member_id)
        context['scrap_num'] = len(scraps)

        scrap_dict = {}
        for i in range(len(scraps)):
            jobposting_id = scraps[i].jobposting_id
            scrap_dict[f'{i}'] = Jobposting.objects.filter(jobposting_id=jobposting_id).values()[0]
        context['scraps'] = scrap_dict
    else:
        context['scrap_num'] = 0

    logging_click(request)
    return JsonResponse(context, status=200)



# 유저가 작성한 자소서 목록 화면에 보여줌
def user_cvletter(request):
    context = {}
    user_email = request.session.get('user_email', False)
    if user_email:
        member_id = User_info.objects.get(email=user_email).member_id
        cvletters = User_cvletter.objects.filter(member_id=member_id)
        context['cvletter_num'] = len(cvletters)

        cvletter_dict = {}
        for i in range(len(cvletters)):
            ith_cvletter_dict = {}
            #jobs_id->Jobposting_jobs:job, jobposting_id->Jobposting:corp_nm&start_time&end_time
            #User_cvletter->user_cvletter_id&written_date
            ith_cvletter_dict['user_cvletter_id'] = cvletters[i].user_cvletter_id
            ith_cvletter_dict['written_date'] = cvletters[i].written_date
            jobs_id = cvletters[i].jobs_id
            ith_cvletter_dict['job'] = Jobposting_jobs.objects.get(jobs_id=jobs_id).job
            jobposting_id = Jobposting_jobs.objects.get(jobs_id=jobs_id).jobposting_id
            ith_cvletter_dict['corp_nm'] = Jobposting.objects.get(jobposting_id=jobposting_id).corp_nm
            ith_cvletter_dict['start_time'] = Jobposting.objects.get(jobposting_id=jobposting_id).start_time
            ith_cvletter_dict['end_time'] = Jobposting.objects.get(jobposting_id=jobposting_id).end_time
            cvletter_dict[f'{i}'] = ith_cvletter_dict
                        
        context['cvletters'] = cvletter_dict
    else:
        context['cvletter_num'] = 0

    logging_click(request)
    return JsonResponse(context, status=200)



def delete_scrap(request):
    context = {}
    try:
        user_email = request.session.get('user_email', False)
        member_id = User_info.objects.get(email=user_email).member_id
        jobposting_id = request.POST.get('jobposting_id', False)
        User_scrap.objects.filter(member_id=member_id, jobposting_id=jobposting_id).delete()
    except:
        context['err'] = 'err'
        logging_click(request) 
    return JsonResponse(context, status=200)



def delete_cvletter(request):
    context = {}
    try:
        user_cvletter_id = request.POST.get('user_cvletter_id', False)
        User_cvletter.objects.filter(user_cvletter_id=user_cvletter_id).delete()
        User_cvletter_items.objects.filter(user_cvletter_id=user_cvletter_id).delete()
    except:
        context['err'] = 'err'
    logging_click(request)
    return JsonResponse(context, status=200)

  