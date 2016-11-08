from django.test import TestCase
from maizi.users.utils import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maizi_website.settings")
# Create your tests here.
from urllib import urlencode

mail_activate_info={
             'email':'Nicky1Wu',
             'verify_code': str(code_encrypt(random_str(4)))
         }
print code_encrypt('10755696650@qq.com')

print code_decrypt('MTA3NTU2OTY2NTBAcXEuY29t')

print code_decrypt('Z2M5cg==')

print code_encrypt('user123')

print code_decrypt('dXNlcjEyMw==')