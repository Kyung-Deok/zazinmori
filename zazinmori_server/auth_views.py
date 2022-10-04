from django.shortcuts import render
import bcrypt
import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse 
from .loggers import logging_login, logging_click
from .models import User_info
from .env_settings import SALT

 
def index(request):
    context = {}
    # m_id 세션변수 값이 없다면 '' 을 넣어라
    context['hello'] = 'hello'
    context['user_email'] = request.session.get('user_email', False)
    context['user_birth'] = request.session.get('user_birth', False)
    context['user_gender'] = request.session.get('user_gender',False)
    return render(request, 'index.html', {'context': context})
 
def register(request):
    context = {}
    if request.method == "GET":
        context['user_email'] = request.session.get('user_email', False)
        if context['user_email'] :
            return redirect("/")
        logging_click(request)
        return render(request, 'signup.html', {'context': context})
    elif request.method == "POST":
        try :
            # postman 으로 테스트 시 : x-www-form-urlencoded 로 시행
            req_name = request.POST['req_name']
            req_email = request.POST['req_email']
            req_birth = request.POST['req_birth']
            req_passwd = request.POST['req_passwd']
            req_gender = request.POST['req_gender']
            req_phone = request.POST['req_phone']
            req_category = request.POST['req_category']
            req_area = request.POST['req_area']
            req_salary = request.POST['req_salary']

            # 회원가입 중복 체크
            user_exist_id = User_info.objects.filter(email=req_email)
            if user_exist_id.exists():
                context['email_chk'] = 1
                return JsonResponse(context, status=200)
            else:
                context['email_chk'] = 0
                User_info.objects.create(
                    passwd=bcrypt.hashpw(req_passwd.encode('utf-8'), bcrypt.gensalt(SALT)).decode('utf-8'),
                    name=req_name,
                    email=req_email,
                    birth=req_birth,
                    gender=req_gender,
                    phone=req_phone,
                    category=req_category,
                    area=req_area,
                    salary=req_salary,
                    reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                logging_click(request)
                context['message'] = req_name + "님 회원가입 되었습니다."
            return JsonResponse(context, status=200,safe=True) # 로그인 화면으로 이동
        
        except django.db.utils.OperationalError as err :
           return JsonResponse({'err':"테이블 없음", "err_detail" : err}, status=400)
        except Exception as err:
           context['err'] = err
           return JsonResponse(context)


def login(request):
    context = {}
    if request.method == "GET":
        context['user_email'] = request.session.get('user_email', False)
        if context['user_email'] :
            return redirect("/")
        return render(request, 'login.html')
    elif request.method == "POST":
        #try :
        req_email = request.POST['email']
        req_passwd = request.POST['passwd']
        # 로그인 체크하기
        user_email = User_info.objects.filter(email=req_email).first()
        if user_email is None : # 비밀번호 검증 추가해야 댐
            context['err'] = "해당 회원 정보가 없습니다."
            return JsonResponse(context)
        else:
            user_pw = user_email.passwd
            check_user_passwd = bcrypt.checkpw(req_passwd.encode('utf-8'), user_pw.encode('utf-8'))
            if not check_user_passwd:
                context['err'] = "비밀번호 정보가 맞지 않습니다."
                return JsonResponse(context)
            else :
                # OK - 로그인
                request.session['member_id'] = user_email.member_id
                request.session['user_email'] = user_email.email
                request.session['user_birth'] = user_email.birth
                request.session['user_gender'] = user_email.gender
                request.session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                logging_login(request, user_email)
                
                #json 형식으로 저장 불가한 타입
                context['user_email'] = user_email.email
                #context['user_name'] = [user_email.email, request.session['user_age']]
                #josn keyerror
                context['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                context['message'] = user_email.name + "님이 로그인하셨습니다."
                context['err'] = ""
                return JsonResponse(context) # 메인 페이지로 이동
        # except django.db.utils.OperationalError :
        #    context['err'] = "테이블 없음"
        #    return JsonResponse(context, status=400)
        # except Exception as err:
        #    context['err'] = err
        #    return JsonResponse(context)

        
def logout(request):
    user = User_info.objects.filter(email=request.session.get("user_email")).first()
    logging_login(request,user)
    request.session.flush()
    return redirect('/')



