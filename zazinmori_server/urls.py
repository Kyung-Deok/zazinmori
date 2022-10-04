"""zazinmori_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import auth_views, com_views, user_views, cvletter_views, etc_views

urlpatterns = [
    ###### 유저 가입, 로그인 , 인증 로직 ######
    path('', auth_views.index, name='mainpage'),
    path('signup/', auth_views.register, name='register'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    # admin / qwer1234
    path('admin/', admin.site.urls), #
    path('', auth_views.index, name='mainpage'), # 
    path('register/', auth_views.register, name='register'), #
    path('login/', auth_views.login, name='login'), #
    path('logout/', auth_views.logout, name='logout'), #
    ###### 기업 검색 로직 ######
    path('company/', com_views.search_company, name='searchcoms'),#
    path('company/company_detail/', com_views.company_detail, name='detailcoms'),#
    #path('company/<int:jobposting_id>/recruits/', com_views.recruit_company, name='recruitcoms'),
    path('company/recruits/', com_views.recruits, name='recruits'),
    path('company/scrap/', com_views.scrap, name='scrap'),
    ###### 마이 페이지 로직 ######
    path('mypage/', user_views.user_info, name='userinfo'), #
    path('mypage/user_update/', user_views.user_update, name='userupdate'), #
    path('mypage/scrap/', user_views.user_scrap, name='userscrap'), #
    path('mypage/delete_scrap/', user_views.delete_scrap, name='deletescrap'), #
    path('mypage/cvletter/', user_views.user_cvletter, name='usercvletter'), #
    path('mypage/delete_cvletter/', user_views.delete_cvletter, name='deletescrap'), #
    #path('mypage/<int:cvl_id>/cvl/', user_views.user_cvletter_update, name='cvlwrite'), #
    ###### 자소서 작성 로직 ######
    path('cvletter/write/<int:jobs_id>', cvletter_views.cvletter_write, name='writecvl'),
    path('cvletter/update/<int:cvl_id>', cvletter_views.user_cvletter_update, name='updatecvl'), #
    ###### 기타 기능 ######
    path('community/', etc_views.community, name='community'),
    path('community/write/', etc_views.write_post, name='writepost'),
    path('community/post_detail/<int:post_id>', etc_views.post_detail, name='postdetail'),
    path('community/delete_post/', etc_views.delete_post, name='deletepost')
]