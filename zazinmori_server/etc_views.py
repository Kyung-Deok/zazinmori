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


def community(request):
    context ={}
    context['user_email'] = request.session.get('user_email', False)
    
    post_all = Board.objects.all().order_by('-post_id')
    # 한 페이지에 게시글 10개씩 출력
    paginator = Paginator(post_all, 10)
    page_num = request.GET.get('page', '1')
    page_obj = paginator.get_page(page_num)
    context['page_obj'] = page_obj
    logging_click(request) 
    return render(request, 'community.html', {'context': context})



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
    
    
    
def post_detail(request, post_id):
    context = {}
    user_email = request.session.get('user_email', False)
    context['user_email'] = user_email
    user_info = User_info.objects.filter(email = user_email)
    post = Board.objects.filter(post_id = post_id)
    
    context['name'] = user_info[0].name
    context['title'] = post[0].title
    context['content'] = post[0].content
    logging_click(request)
    return render(request, 'post_detail.html', {'context': context})

