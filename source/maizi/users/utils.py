#!/usr/bin/env python
# -*- coding: utf-8 -*-
#业务处理工具及数据模块
import base64
from urllib import urlencode
from random import Random
from PIL import Image, ImageDraw, ImageFont
import cStringIO, string, os, random
from django.conf import settings
import hashlib
#验证码生成
def generate_verification_code():
    image = Image.new('RGB', (147, 49), color = (255, 255, 255))
    font_file = os.path.join(settings.BASE_DIR, 'static/fonts/Arial.ttf')
    font = ImageFont.truetype(font_file, 47)
    draw = ImageDraw.Draw(image)
    rand_str = ''.join(random.sample(string.letters + string.digits, 4))
    draw.text((7, 0), rand_str, fill=(0, 0, 0), font=font)
    del draw
    buf = cStringIO.StringIO()
    image.save(buf, 'jpeg')
    return rand_str,buf
#url转化
def url_covenrt(request,dict,path):
    host=request.get_host()
    dict2path=urlencode(dict)
    return 'http://'+str(host)+'/'+path+'?'+dict2path

#随机生成编码
def random_str(randomlength=4):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
#base64加密
def code_encrypt(str):
    return base64.b64encode(str)
#base64解密
def code_decrypt(str):
    return base64.b64decode(str)

def md5_encrypt(str):
    h=hashlib.md5()
    h.update(str)
    return h.hexdigest()