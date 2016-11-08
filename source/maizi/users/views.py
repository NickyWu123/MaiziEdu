#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render
import logging
from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.db.models import Count
#from forms import *
from common.models import UserProfile,EmailVerifyRecord
from .utils import *
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login
# Create your views here
#验证码
def verification_code(request):
    rand_str,buf=generate_verification_code()
    request.session['verification_code']=rand_str
    return HttpResponse(buf.getvalue(), 'image/jpeg')

#验证邮箱唯一性
@csrf_exempt
def validate_email(request):
    msg={}
    try:
        validate_email=str(json.loads(request.body)['email'])
        emaillist = UserProfile.objects.filter(email=validate_email)
        if emaillist:
            msg['is_only']='NotOnly'
        else:
            msg['is_only']='Only'
    except Exception,e:
        return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    return HttpResponse(json.dumps(msg), content_type="application/json")
#验证验证码
@csrf_exempt
def validate_verification_code(request):
    msg={}
    try:
        verification_code_in_session=str(request.session['verification_code'])
        verification_code=str(json.loads(request.body)['verification_code'])
        if verification_code.lower() == verification_code_in_session.lower():
            msg['is_verification_right']=True
        else:
            msg['is_verification_right']=False
    except Exception,e:
        return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    return HttpResponse(json.dumps(msg), content_type="application/json")
#注册
@csrf_exempt
def user_register(request):
    msg={}
    try:
        body=json.loads(request.body)
        register_email=body[u'registerEmail'].encode('utf-8')
        register_username=register_email.split('@')[0]
        register_password=body[u'registerPassword'].encode('utf-8')
        register_code=body[u'registerCode'].encode('utf-8')
        mail_activate_info={
                'email':code_encrypt(register_email),
                'verify_code':code_encrypt(random_str(4))
            }
        url=url_covenrt(request=request,dict=mail_activate_info,path='users/email_activate')
        password=make_password(register_password, None, 'pbkdf2_sha256')
        user=UserProfile(email=register_email,password=password,username=register_username,is_active=False,is_staff=False)
        user.email_user('激活你的用户','请点击链接:'+url,'1075569650@qq.com')
        request.session['email_activate'] = mail_activate_info['email']
        request.session['verify_code_activate']=mail_activate_info['verify_code']
        user.save()
        msg['isSuccess']=True
    except Exception,e:
        return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    return HttpResponse(json.dumps(msg),content_type="application/json")
#注册成功或注册邮箱发送后回执
def registerorretrieve_sucess(request,param):
    msg={}
    try:
        method=param.split('/')[0]
        email=param.split('/')[1]
        user=UserProfile.objects.get(email=email)
        if method=='register':
            msg['info']='register'
        elif method=='retrieve':
            msg['info']='retrieve'
        else:
            msg['info']='nomethod'
    except Exception:
        return render(request, 'user/ErrorUrl.html.html',{'error':'此链接已失效'})
    msg['error']=False
    return render(request, 'user/RegitserorRetrieveSuccess.html',locals())

def email_activate(request):
    b64_verify_code = request.GET.get('verify_code', None)
    b64_email = request.GET.get('email', None)
    try:
        email=code_decrypt(b64_email)
        code_record=EmailVerifyRecord.objects.filter(code=b64_verify_code,type=0,email=email)
        if  len(code_record)!=0:
            return render(request, 'user/EmailLinkInvalid.html',{'error':'此链接已失效'})
        elif request.session.get('verify_code_activate')!=b64_verify_code or request.session.get('email_activate')!=b64_email:
            return render(request, 'user/EmailLinkInvalid.html',{'error':'此链接已失效'})
        else:
            user=UserProfile.objects.get(email=email)
            user.is_active=True
            user.valid_email=True
            code_record_user=EmailVerifyRecord(code=b64_verify_code,type=0,email=email)
            code_record_user.save()
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,user)
    except Exception,e:
        return render(request, 'user/EmailLinkInvalid.html',{'error':'此链接异常'})
    return render(request, 'user/EmailRegisterSuccess.html')

@csrf_exempt
def user_login(request):
    msg={}
    try:
        body=json.loads(request.body)
        email=body[u'email'].encode('utf-8')
        password=body[u'password'].encode('utf-8')
        user=authenticate(email=email, password=password)

        if user:
            print user.is_active
            if user.is_active==False:
                msg['isSuccess']=False
                msg['is_NotActive']=True
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
                msg['isSuccess']=True
        else:
            msg['isSuccess']=False
            msg['isNotActive']=False
    except Exception,e:
         return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    return HttpResponse(json.dumps(msg),content_type="application/json")

def user_logout(request):
    logout(request)
    return redirect('/')

@csrf_exempt
def email_retrieve(request):
    msg={}
    try:
        body=json.loads(request.body)
        email=body[u'email'].encode('utf-8')
        user=UserProfile.objects.get(email=email)
        if user==None:
            msg['isSuccess']=False
        else:
            mail_retrieve_info={
                'email':code_encrypt(email),
                'verify_code':code_encrypt(random_str(4))
            }
            url=url_covenrt(request=request,dict=mail_retrieve_info,path='users/email_retrieve_password')
            user.email_user('修改你的用户密码','请点击链接:'+url,'1075569650@qq.com')
            request.session['email_retrieve'] = mail_retrieve_info['email']
            request.session['verify_code_retrieve']=mail_retrieve_info['verify_code']
            msg['isSuccess']=True
    except Exception,e:
        return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    # user=UserProfile.objects.get(email=email)
    return HttpResponse(json.dumps(msg),content_type="application/json")

def email_retrieve_password(request):
    b64_verify_code = request.GET.get('verify_code', None)
    b64_email = request.GET.get('email', None)
    try:
        email=code_decrypt(b64_email)
        code_record=EmailVerifyRecord.objects.filter(code=b64_verify_code,type=1,email=email)
        if  len(code_record)!=0:
            return render(request, 'user/EmailLinkInvalid.html',{'error':'该链接已失效，请重新找回密码！'})
        elif request.session.get('verify_code_retrieve')!=b64_verify_code or request.session.get('email_retrieve')!=b64_email:
            return render(request, 'user/EmailLinkInvalid.html',{'error':'该链接已失效，请重新找回密码！'})
        else:
            return render(request, 'user/UpdateUserPassword.html')
    except Exception,e:
        return render(request, 'user/EmailLinkInvalid.html',{'error':'此链接异常'})

@csrf_exempt
def update_password(request):
    msg={}
    try:
        body=json.loads(request.body)
        password=body[u'password'].encode('utf-8')
        email=code_decrypt(request.session.get('email_retrieve'))
        b64_verify_code=request.session.get('verify_code_retrieve')

        user=UserProfile.objects.get(email=email)
        user.password=make_password(password, None, 'pbkdf2_sha256')
        user.save()
        code_record_user=EmailVerifyRecord(code=b64_verify_code,type=1,email=email)
        code_record_user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)
        msg['isSuccess']=True
    except Exception,e:
        return render(request, 'user/ErrorUrl.html',{'error':'此地址异常'})
    return HttpResponse(json.dumps(msg),content_type="application/json")