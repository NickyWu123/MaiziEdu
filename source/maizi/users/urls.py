#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2015/11/3
@author: yopoing
users模块的url配置。
"""

from django.conf.urls import patterns,url
urlpatterns = patterns('users.views',
    url(r'^login/$','user_login',name='login'),
    url(r'^register/$','user_register',name='register'),
    url(r'^logout/$','user_logout',name='logout'),
    #url(r'^validate_username/$','validate_username',name='validate_username'),
    url(r'^validate_email/$','validate_email',name='validate_email'),
    url(r'^verification_code/$','verification_code',name='verification_code'),
    url(r'^validate_verification_code/$','validate_verification_code',name='validate_verification_code'),
    url(r'^email_activate/$','email_activate',name='email_activate'),
    url(r'^registerorretrieve_sucess/(.+)/$','registerorretrieve_sucess',name='registerorretrieve_sucess'),
    url(r'^email_retrieve/','email_retrieve',name='email_retrieve'),
    url(r'^email_retrieve_password/','email_retrieve_password',name='email_retrieve_password'),
     url(r'^update_user_password/','update_password',name='update_password'),
)
