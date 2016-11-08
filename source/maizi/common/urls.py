#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2019/9/22
@author: 吴甜洋
common模块的url配置。
"""

from django.conf.urls import patterns, url

urlpatterns = patterns('common.views',
    url(r'^$', 'index', name='index'),
)
