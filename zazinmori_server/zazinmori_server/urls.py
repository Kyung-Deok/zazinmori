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
from . import auth_views, com_views, user_views, cvletter_views

urlpatterns = [
    ###### 유저 가입, 로그인 , 인증 로직 ######
    # admin / qwer1234
    path('admin/', admin.site.urls), #
    path('', auth_views.index, name='mainpage'), # 
    path('signup', auth_views.register, name='register'), #
    path('login/', auth_views.login, name='login'), #
    path('logout/', auth_views.logout, name='logout'), # 
    ###### 기업 검색 로직 ######
    path('companys/', com_views.search_company, name='searchcoms'),#
    path('companys/<int:jobposting_id>/recruits/', com_views.recruit_company, name='recruitcoms'),
    path('companys/<int:jobposting_id>/recruits/detail', com_views.recruit_positions, name='recruitposits'),
    ###### 마이 페이지 로직 ######
    path('info/', user_views.user_info, name='userinfo'), #
    path('info/user/', user_views.user_update, name='userupdate'), #
    path('info/<int:cvl_id>/cvl/', user_views.user_cvletter_update, name='cvlwrite'), #

    ###### 자소서 작성 로직 ######
    # path('api/cvletter/write/<int:member_id>', cvletter_views.cvletter_write, name='writecvl'), 
]