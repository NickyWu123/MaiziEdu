# -*- coding: utf-8 -*-
from django import template
register = template.Library()

@register.filter
def email2name(key):
	return key.split('@')[0]