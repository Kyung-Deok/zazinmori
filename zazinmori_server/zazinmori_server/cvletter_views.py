from django.shortcuts import render
import bcrypt
import django
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.http import JsonResponse

from .models import *

def cvletter_write(request):
    if request.method == "GET":
        return render(request, '자소서 작성 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            pass
        except:
            pass
        
def cvletter_updates(request):
    if request.method == "GET":
        return render(request, '자소서 작성 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            pass
        except:
            pass
        
def cvletter_read(request):
    if request.method == "GET":
        return render(request, '자소서 작성 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            pass
        except:
            pass

        
def cvletter_delete(request):
    if request.method == "GET":
        return render(request, '자소서 작성 페이지.html')
    elif request.method == "POST":
        context={}
        try:
            pass
        except:
            pass