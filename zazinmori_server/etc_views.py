from django.shortcuts import render, redirect
import bcrypt
import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse
from django.core.paginator import Paginator
from .loggers import logging_click
from .models import *
from django.db.models import Sum, Count, Model

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search, Q



def community(request):
    context ={}
    user_email = request.session.get('user_email', False)
    context['user_email'] = user_email
    
    if request.method == 'GET':
        post_all = Board.objects.all().order_by('-post_id')
        # 한 페이지에 게시글 10개씩 출력
        paginator = Paginator(post_all, 10)
        page_num = request.GET.get('page', '1')
        page_obj = paginator.get_page(page_num)
        context['page_obj'] = page_obj
        logging_click(request) 
        return render(request, 'community.html', {'context': context})

    else:
        user_info = User_info.objects.filter(email=user_email)
        
        if len(user_info) == 0:
            context['user_exists'] =0
        else :                
            user_area = user_info[0].area
            user_category = user_info[0].category
            context['user_area'] = user_area
            context['user_category'] = user_category
            
            try:
                corp_rank = search_corp_rank()
                job_rank = rank_by_job(user_category)
                area_rank = rank_by_region(user_area)
                context['corp_rank'] = corp_rank
                context['job_rank'] = job_rank
                context['area_rank'] = area_rank
                
                scrap_rank = User_scrap.objects.values('jobposting_id').annotate(cnt=Count('jobposting_id')).order_by('cnt')
                scrap_lst = []
                for i in range(len(scrap_rank), len(scrap_rank)-5, -1):
                    jobposting_id = scrap_rank.values()[i]['jobposting_id']
                    jobposting = Jobposting.objects.filter(jobposting_id=jobposting_id)
                    corp_nm = jobposting[0].corp_nm
                    start_time = jobposting[0].start_time[:10]
                    end_time = jobposting[0].end_time[:10]
                                        
                    scrap_dict = {}
                    scrap_dict['corp_nm'] = corp_nm
                    scrap_dict['start_time'] = start_time
                    scrap_dict['end_time'] = end_time
                    scrap_lst.append(scrap_dict)
                context['scrap_rank'] = scrap_lst
                    
            except:
                context['user_exists'] = 'err'
        
        
        return JsonResponse(context, status=200)



def write_post(request):
    context = {}
    user_email = request.session.get('user_email', False)
    context['user_email'] = user_email
    user_info = User_info.objects.filter(email = user_email)
    
    if request.method == 'GET':
        context['name'] = user_info[0].name
        logging_click(request) 
        return render(request, 'write_post.html', {'context': context})
    
    else:
        try:
            member_id = user_info[0].member_id
            name = user_info[0].name
            title = request.POST.get('title', False)
            content = request.POST.get('content', False)
            
            Board.objects.create(
                member_id = member_id,
                name = name,
                title = title,
                content = content,
                written_date = datetime.now().strftime('%Y-%m-%d')
            )
        except:
            context['err'] = 'err'
        logging_click(request) 
        return JsonResponse(context, status=200)
   
    
    
def delete_post(request):
    context = {}
    user_email = request.session.get('user_email', False)
    user_info = User_info.objects.filter(email = user_email)    
    member_id = user_info[0].member_id
    
    post_id = request.POST['post_id']
    post_member_id =  Board.objects.filter(post_id=post_id).first().member_id

    if member_id == post_member_id:    
        Board.objects.filter(post_id=post_id).delete()
        context['user_chk'] = 1
    else :
        context['user_chk'] = 0

    logging_click(request) 
    return JsonResponse(context, status=200)
    
    
    
def post_detail(request, post_id):
    context = {}
    user_email = request.session.get('user_email', False)
    context['user_email'] = user_email
    user_info = User_info.objects.filter(email = user_email)
    post = Board.objects.filter(post_id = post_id)
    
    context['name'] = post[0].name
    context['title'] = post[0].title
    context['content'] = post[0].content
    context['post_id'] = post_id
    
    logging_click(request)
    return render(request, 'post_detail.html', {'context': context})




# 밑의 세 함수에 공통으로 들어가는 내용을 따로 빼놓은 것임
# 각 함수에 변수로 할당해서 사용하기 때문에 views.py에 같이 들어가야함
def elastic_client_set():
    # elasticsearch와 연결
    client = connections.create_connection(hosts=['http://220.86.100.9:9200'], http_auth=('elastic', 'votmdnjem'))
    s = Search(using=client)

    # 유저가 상세정보를 확인한 기업명 기준으로 grouping
    body = {"size": 0, "aggs": {"by_corp": {"terms": {"field": "result_corp_nm.keyword", "size": 5},
                                            "aggs": {"addrs": {"top_hits": {"_source": ['result_corp_addr']}}}
                                            }}}

    # 1주일 간의 데이터로 시간 범위 설정 / targetlog-* 인덱스에서 로그데이터 가져옴
    s = Search.from_dict(body).filter("range", **{"@timestamp": {"gte": "now-7d", "lte": "now"}})
    s = s.index("targetlog-*")
    s = s.doc_type("target_log")

    return s

# 일주일 간 이용자(회원+비회원)이 가장 많이 검색한 기업
# 기업 상세 정보 확인(클릭)까지 이루어 졌을 경우를 유효값으로 카운팅(이하 동일)
def search_corp_rank():
    t = elastic_client_set().execute()
    corp_rank_list = []
    for item in t.aggregations.by_corp.buckets:
        dic = {}
        dic['corp_nm'] = item.key
        addr_split = item.addrs.hits.hits[0]._source.result_corp_addr.split(' ')
        dic['addr'] = addr_split[0] + " " + addr_split[1]
        corp_rank_list.append(dic)

    # 이름은 list지만, list안에 dictionary가 들어간 json 양식임(이하 동일)
    return corp_rank_list

# 일주일 간 희망업종이 같은 지원자(회원)들이 가장 많이 검색한 기업
def rank_by_job(request):
    # 희망지원업종으로 필터링
    # job 변수에 들어갈 값은 reqeust로 회원 정보에 있는 희망지원업종을 받아서 입력
    # ex. job = request.GET.get()
    s = elastic_client_set()
    q_by_job = Q("bool", must=[Q("match", user_like_job=request)])
    s = s.query(q_by_job)
    t = s.execute()
    
    # 반복문 걸어서 필요 필드 가져 오기
    favorite_job_list = []
    for item in t.aggregations.by_corp.buckets:
        dic = {}
        dic['corp_nm'] = item.key
        addr_split = item.addrs.hits.hits[0]._source.result_corp_addr.split(' ')
        dic['addr'] = addr_split[0] + " " + addr_split[1]
        favorite_job_list.append(dic)

    return favorite_job_list

# 일주일 간 희망근무지가 같은 지원자(회원)이 가장 많이 검색한 기업
def rank_by_region(request):
    # 희망 근무지로 필터링
    # region 변수에 들어갈 값은 reqeust로 회원 정보에 있는 희망근무지를 받아서 입력
    # ex. region = request.GET.get()
    s = elastic_client_set()
    q_by_region = Q("bool", must=[Q("match", user_like_workzone=request)])
    s = s.query(q_by_region)
    t = s.execute()

    # 반복문 걸어서 필요한 필드 가져오기
    favorite_region_lst = []
    for item in t.aggregations.by_corp.buckets:
        dic = {}
        dic['corp_nm'] = item.key
        addr_split = item.addrs.hits.hits[0]._source.result_corp_addr.split(' ')
        dic['addr'] = addr_split[0] + " " + addr_split[1]
        favorite_region_lst.append(dic)

    return favorite_region_lst

