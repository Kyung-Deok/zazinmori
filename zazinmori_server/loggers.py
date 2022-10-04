'''
=================Loggers===================
'''
# 1. 유저가 로그인 하면 시간을 표시해서 유저가 얼마나 자주 드나드는지 확인해보겠다.
# 2. 유저/비유저가 가장 많이 검색한 키워드를 뽑아내겠다.(인기 검색어, 추후 검색엔진 보완용)
# 2-1. 유저/비유저가 가장 많이 검색한 기업을 집계해서 표시하겠다.( 회사명만 집계)
# 3. 유저가 스크랩을 가장 많이 한 기업을 표시하겠다. ( 이건 db)

# 4. 관심업종을 같은 곳으로 저장해둔 유저가 가장 검색을 많이 한 기업
# 5. 희망 근무지로 같은 곳을 저장해둔 유저 중 가장 검색을 많이 한 기업

# 4,5 번 하나 로거로 동작 / 집계는 필터

import logging
from pprint import pprint
from datetime import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def logging_login(request, user) :
    # request : 요청, user : 유저정보
    logger_login = logging.getLogger("zazinmori_server.login")
    user_birth =request.session.get('user_birth', datetime.now().strftime("%Y-%m-%d"))
    user_year = datetime.strptime(user_birth, "%Y-%m-%d") # string -> datetime
    login_time = datetime.strptime(request.session.get("login_time",None),"%Y-%m-%d %H:%M:%S")
    stay = datetime.now() - login_time
    data={
        #'server_num' : 1,
        'request_user' : user.member_id, # DB에 저장되었는지 확인하기 위해
        'user_gender' : user.gender,
        'user_age' : int(datetime.now().strftime("%Y")) - user_year.year + 1,
        'client_ip' : get_client_ip(request),
        'login_time' : request.session.get("login_time", "no_user"),
        'stay_time' : int(stay.total_seconds())
    }
    pprint(data)
    logger_login.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), extra=data)

# 유저가 클릭한 것들을 표시
def logging_click(request) :
    # request : 요청, user : 유저 정보, 
    # 유저번호, 유저 성별, 유저 나이, 유저가 요청한 주소, 요청 시간
    logger_click = logging.getLogger("zazinmori_server.click")
    user_birth =request.session.get('user_birth', datetime.now().strftime("%Y-%m-%d"))
    user_year = datetime.strptime(user_birth, "%Y-%m-%d")
    # 로그인한 사람(요청한 유저 정보)의 클릭 로그 수집
    data = {
        #'server_num' : 1,
        'request_user' : request.session.get('member_id', "no_user"), # 유저 id, 없으면 no_user
        'user_gender' : request.session.get('user_gender',"no_user"), # 유저 성별, 없으면 no_user
        'user_age' : int(datetime.now().strftime("%Y")) - user_year.year + 1,  # 유저 나이, 없으면 1
        'client_ip' : get_client_ip(request), # 유저 ip
        'request_path' : request.path, # 요청 path
        'request_method' : request.method, # 요청 full path, 쿼리스트링 까지
    }
    pprint(data)
    logger_click.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), extra=data)


def logging_search(request, keyword) :
    # 유저번호, 유저 성별, 유저 나이,검색 요청 시간, 검색 키워드

    logger_search = logging.getLogger("zazinmori_server.search")
    user_birth =request.session.get('user_birth', datetime.now().strftime("%Y-%m-%d"))
    user_year = datetime.strptime(user_birth, "%Y-%m-%d")
    data = {
        #'server_num' : 1,
        'request_user' : request.session.get('member_id', "no_user"),
        'user_gender' : request.session.get('user_gender', "no_user"),
        'user_age' : int(datetime.now().strftime("%Y")) - user_year.year + 1, # 만약 나이가 1이면 No user
        'client_ip' : get_client_ip(request),
        'keyword' : keyword,
    }
    pprint(data)
    logger_search.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), extra=data)
    return



def logging_user_target(request, user, com_name) :
    # 유저가 클릭한 회사
    logger_search = logging.getLogger("zazinmori_server.user_target")
    user_birth =request.session.get('user_birth', datetime.now().strftime("%Y-%m-%d"))
    user_year = datetime.strptime(user_birth, "%Y-%m-%d")
    data = {
        #'server_num' : 1,
        'request_user' : request.session.get("member_id", "no_user"),
        'user_gender' : request.session.get('user_gender', "no_user"),
        'user_age' : int(datetime.now().strftime("%Y")) - user_year.year + 1,
        "user_like_job" : user.category,
        "user_like_workzone" :user.area,
        'client_ip' : get_client_ip(request),
        # "result_regi_code" : request.POST.get("regi_code", False),
        "result_corp_nm" : com_name.first().corp_nm,
        "result_corp_addr" : com_name.first().address
    }
    pprint(data)
    logger_search.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), extra=data)
    return


'''
=================Loggers===================
'''
