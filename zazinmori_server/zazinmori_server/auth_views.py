import email
from email.policy import default
from django.shortcuts import render
import bcrypt
import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse, HttpResponse

from .models import Users_info
from .env_settings import SALT 
 
# return JsonResponse()부분을 필요에 따라 render()나 JsonResponse()로 고쳐서 씀.

def index(request):
    context = {}
    # m_id 세션변수 값이 없다면 '' 을 넣어라
    # html 파일에서 {% if request.session %} 로그인이 됐다면 표시할 태그 {% else %} 로그인 안됐을때 표시할거 {% endif %}
    context['hello'] = 'hello'
    context['user_email'] = request.session.get('user_email', False)
    context['user_age'] = request.session.get('user_age', False)
    # if request.session is None :
    #     return redirect('/')
 
    return JsonResponse(context, status=200)
 
 
def register(request):
    context = {}
    if request.method == "GET":
        return JsonResponse({'msg' : 'register'}, status=200)
        # return render(request, '회원가입 템플릿.html')
    elif request.method == "POST":
        try :
            # postman 으로 테스트 시 : x-www-form-urlencoded 로 시행
            req_name = request.POST.get('name', False)
            req_email = request.POST.get("email", False)
            req_birth = request.POST.get('birth',False)
            req_passwd = request.POST.get("passwd", False)
            req_passwd2 = request.POST.get("passwd", False)
            
            print(req_passwd, req_name, req_email, req_birth)
            # 값 전부 썼는지 확인(html input 태그 속성에서 required 태그 쓰면 이거 안해도 됩니다)
            if False in (req_passwd, req_email,req_birth, req_name):
                return JsonResponse({"err" : "모두 정확히 기입해 주세요."}, status=400)
            
            # 회원가입 중복 체크
            user_exist_id = Users_info.objects.filter(email=req_email) # id 중복체크
            if user_exist_id.exists():
                return JsonResponse({"message" : "중복된 이메일 입니다."}, status=400)
            elif req_passwd != req_passwd2 :
                return JsonResponse({"message" : "비밀번호를 정확히 확인해 주세요"}, status=400)
            # 됐다면 유저 저장
            else:
                Users_info.objects.create(
                    passwd=bcrypt.hashpw(req_passwd.encode('utf-8'), bcrypt.gensalt(SALT)).decode('utf-8'),
                    name=req_name,
                    email=req_email, 
                    birth=req_birth,
                    reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), # json은 date 타입 지원x , string으로 변환
                    update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                )
                context['regi_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                context['message'] = req_name + "님 회원가입 되었습니다."
            return JsonResponse(context, status=200,safe=True) # 로그인 화면으로 이동
        
        except django.db.utils.OperationalError as err :
            return JsonResponse({'err':"테이블 없음", "err_detail" : err}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})
 
def login(request):
    context = {}
    if request.method == "GET":
        context['message'] = "login"
        # return render(request, '로그인 템플릿.html')
        return JsonResponse(context, status=200)
    elif request.method == "POST":
        try :
            req_email = request.POST.get('email', False)
            req_passwd = request.POST.get('passwd', False)
            # 로그인 체크하기
            user_email = Users_info.objects.filter(email=req_email).first()
            user_pw = user_email.passwd
            check_user_passwd = bcrypt.checkpw(req_passwd.encode('utf-8'), user_pw.encode('utf-8'))
            #if rs.exists():
            if not user_email : # 비밀번호 검증 추가해야 댐
                return JsonResponse({"err" : "로그인 정보가 맞지 않습니다."}, status=400)
            elif not check_user_passwd :
                return JsonResponse({"err" : "로그인 정보가 맞지 않습니다.pw"}, status=400)
            else :
                # OK - 로그인
                request.session['user_email'] = user_email.email
                request.session['user_age'] = user_email.birth

                context['user_email'] = user_email.email
                context['user_name'] = [user_email.email, request.session['user_age']]
                context['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                context['message'] = user_email.name + "님이 로그인하셨습니다."
                return JsonResponse(context, status=200) # 메인 페이지로 이동

    
        except django.db.utils.OperationalError :
            return JsonResponse({'err':"테이블 없음"}, status=400)
        except Exception as err:
            return JsonResponse({"err": err})
        
def logout(request):
    # 세션 id를 지운다 그리고 메인페이지로 이동
    request.session.flush()
    return redirect('/')
