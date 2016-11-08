#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2016/9/22
@author: 吴甜洋
Common模块View业务处理。
"""

from django.shortcuts import render

# 首页
def index(request):
    return render(request, "common/index.html", locals())
