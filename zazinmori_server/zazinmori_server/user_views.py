from django.shortcuts import render
import bcrypt
import django

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse

from .models import *

# 마이페이지 초입 페이지
def user_info(request):
    if request.method == "GET":
        try : 
            context = {}
            # 세션 email이랑 유저의 email이 맞는지 확인
            # 로그인한 유저가 맞는지 확인
            ses_user = request.session.get('user_email', None)
            user_info = User.objects.get(email = ses_user)
            # 아니라면 로그인 페이지로 리다이렉트
            if not user_info :
                redirect('login/')
            else : 
                # 맞다면 정보 보여주기 : 유저 기본 정보, 스크랩한 공고, 쓴 자소서들
                scraps = User_scraps.objects.get(memeber_id = user_info.memeber_id)
                scrap_postings = Job_posting.objects.filter(jobposting_id = scraps.jobposting_id) 
                written_cvletters = User_cvletter.objects.get(member_id = user_info.member_id)
                
                context['user_info'] = user_info
                context['scraps'] = list(scrap_postings)
                context['wriiten_cvletters'] = list(written_cvletters.written_name)
                context['message'] = 'success'
            return render(request, '마이 페이지.html', context)
        except django.db.utils.OperationalError :
                return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
                return JsonResponse({"err": err})

        
def user_update(request):
    ses_user = request.session.get('user_email', None)
    user_info = User.objects.get(email = ses_user)
    context = {}
    if request.method == "GET":
    # GET 일 때, 회원정보를 우선 띄워준다.    
        try : 
            # 세션 email이랑 유저의 email이 맞는지 확인
            # 로그인한 유저가 맞는지 확인
            # 아니라면 로그인 페이지로 리다이렉트
            if not user_info :
                redirect('login/')
            else :
                context['user_name'] = user_info.name
                context['user_email'] = user_info.email
                context['user_passwd'] = user_info.passwd
                context['user_birth'] = user_info.birth                
            return render(request, '회원정보 수정.html', context)
        except Exception as err : 
            return JsonResponse({'err' : err})    
    elif request.method == "POST":
        re_passwd = request.POST.get('user_passwd')
        re_passwd2 = request.POST.get('user_passwd2')
        re_birth = request.POST.get('user_birth')
        try:
            if re_passwd != re_passwd2 : 
                return JsonResponse({"err": "비밀번호가 서로 일치하지 않습니다"}, status=400)
            
            else : 
                # 맞다면..
                User.objects.update(
                    passwd = re_passwd,
                    birth = re_birth,
                    update_date = datetime.now()
                )
                context['message'] = '회원정보 변경 완료'
                return JsonResponse(context, status=200)
        except django.db.utils.OperationalError :
                return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err : 
            return JsonResponse({'err' : err})    
# 유저 자소서 정보 편집 - 일단 삭제만 가능    
def user_cvletter_update(request):
    ses_user = request.session.get('user_email', None)
    user_info = User.objects.get(email = ses_user)
    user_cvletters = User_cvletter.objcets.filter(member_id=user_info.member_id)
    context = {}
    if request.method == "GET":
    # GET 일 때, 회원정보를 우선 띄워준다.    
        try : 
            # 세션 email이랑 유저의 email이 맞는지 확인
            # 로그인한 유저가 맞는지 확인
            # 아니라면 로그인 페이지로 리다이렉트
            if not user_info :
                redirect('login/')
            else :
                user_cvletters = User_cvletter.objects.get(member_id=user_info.member_id)
                context['cvletter_written_name'] = user_cvletters.written_name
                context['cvletter_written_date'] = user_info.written_date
                context['cvletter_q1'] = user_info.q1
                context['cvletter_a1'] = user_info.q1
                context['cvletter_q2'] = user_info.q2
                context['cvletter_a2'] = user_info.q2
                context['cvletter_q3'] = user_info.q3
                context['cvletter_a3'] = user_info.q3
                context['cvletter_q4'] = user_info.q4
                context['cvletter_a4'] = user_info.q4
                context['cvletter_q5'] = user_info.q5
                context['cvletter_a5'] = user_info.q5
                context['cvletter_q6'] = user_info.q6
                context['cvletter_a6'] = user_info.q6
                context['cvletter_q7'] = user_info.q7
                context['cvletter_a7'] = user_info.q7
                context['cvletter_q8'] = user_info.q8
                context['cvletter_a8'] = user_info.q8       
            return render(request, '자소서 수정 페이지.html', context)
        except Exception as err : 
            return JsonResponse({'err' : err})
    elif request.method == "POST":
        re_q1 = request.POST.get('user_q1')
        re_a1 = request.POST.get('user_a1')
        re_q2 = request.POST.get('user_q2')
        re_a2 = request.POST.get('user_a2')
        re_q3 = request.POST.get('user_q3')
        re_a3 = request.POST.get('user_a3')
        re_q4 = request.POST.get('user_q4')
        re_a4 = request.POST.get('user_a4')
        re_q5 = request.POST.get('user_q5')
        re_a5 = request.POST.get('user_a5')
        re_q6 = request.POST.get('user_q6')
        re_a6 = request.POST.get('user_a6')
        re_q7 = request.POST.get('user_q7')
        re_a7 = request.POST.get('user_a7')
        re_q8 = request.POST.get('user_q8')
        re_a8 = request.POST.get('user_a8')
        try:
            user_cvletters.update(
                q1 = re_q1,
                a1 = re_a1,
                q2 = re_q2,
                a2 = re_a2,
                q3 = re_q3,
                a3 = re_a3,
                q4 = re_q4,
                a4 = re_a4,
                q5 = re_q5,
                a5 = re_a5,
                q6 = re_q6,
                a6 = re_a6,
                q7 = re_q7,
                a7 = re_a7,
                q8 = re_q8,
                a8 = re_a8,
                
                update_date = datetime.now()
            )
            context['update_date'] = user_cvletters.update_date
            context['message'] = '자소서 변경 완료'
            return JsonResponse(context, status=200)
        except django.db.utils.OperationalError :
                return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err : 
            return JsonResponse({'err' : err})
        
# 삭제는 요청을 받으면(버튼을 누르면) 해당 자소서 삭제 후, 리다이렉트로 마이페이지   
def user_cvletter_delete(request):
    pass
'''
회원 탈퇴 : 추후 구현 예정

def user_delete(request):
    if request.method == "GET":
        return render(request, '마이 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            pass
        except:
            pass
'''     
