from django.shortcuts import render
import bcrypt
import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse

from .models import User
from env_settings import SALT 
 
def index(request):
    context = {}
    # m_id 세션변수 값이 없다면 '' 을 넣어라
    context['user_email'] = request.session.get('user_email', '')
    context['user_age'] = request.session.get('user_age', '')
    # username = request.COOKIES.get('username')
    # password = request.COOKIES.get('password')

    # if request.session is None :
    #     return redirect('/')
 
    return JsonResponse(context, status=200)
 
 
def register(request):
    if request.method == "GET":
        return render(request, '회원가입 템플릿.html')
    elif request.method == "POST":
        context = {}
        try : 
            req_passwd = request.POST.get("passwd", None)
            req_name = request.POST.get("name", None)
            req_email = request.POST.get("email", None)
            req_birth = request.POST.get('birth', None)
            
            # 값 전부 썼는지 확인
            if req_passwd | req_name | req_email | req_birth is None :
                return JsonResponse({"err" : "모두 정확히 기입해 주세요."}, status=400)
            
            # 회원가입 중복 체크
            user_exist_id = User.objects.filter(email=req_email)[0]
            if user_exist_id.exists():
                return JsonResponse({"message" : "중복된 이메일 입니다."}, status=400)

            # 됐다면 유저 저장
            else:
                User.objects.create(
                    passwd=bcrypt.hashpw(req_passwd.encode('utf-8'), bcrypt.gensalt(SALT)),
                    name=req_name,
                    email=req_email, 
                    birth=req_birth,
                    reg_date=datetime.now(), 
                    update_date=datetime.now()
                )
                context['regi_time'] = datetime.now()
                context['message'] = req_name + "님 회원가입 되었습니다."
                return JsonResponse(context, status=200) # 로그인 화면으로 이동
        
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})
 
def login(request):
    if request.method == "GET":
        return render(request, '로그인 템플릿.html')
    elif request.method == "POST":
        context = {}
        try :
            req_email = request.POST.get('email', None)
            req_passwd = request.POST.get('passwd', None)
 
            # 로그인 체크하기
            user_email = User.objects.get(email=req_email).first()[0]
            user_pw = user_email.passwd
            check_user_passwd = bcrypt.checkpw(user_pw.encode('utf-8'), req_passwd)
            print(user_email + '/' + check_user_passwd)
            
            #if rs.exists():
            if not user_email | check_user_passwd :
                return JsonResponse ({"err" : "로그인 정보가 맞지 않습니다."}, status=400)
            else :
                # OK - 로그인
                request.session['user_email'] = user_email.email
                request.session['user_age'] = user_email.birth

                context['user_email'] = user_email.email, request.session['user_email']
                context['user_name'] = user_email.name
                context['login_time'] = datetime.now()
                context['message'] = user_email.name + "님이 로그인하셨습니다."
                return JsonResponse(context, status=200) # 메인 페이지로 이동

    
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})
        
def logout(request):
    request.session.flush()
    return redirect('/')
