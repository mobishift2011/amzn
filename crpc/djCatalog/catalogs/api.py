# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from models import Brand

def JSONResponse(response):
	return HttpResponse(simplejson.dumps(response))

def brands(request):
	brands = Brand.objects(is_delete=False)
	res = {
		'response': [brand.title for brand in brands]
	}
	return JSONResponse(res)

def match(request):
	pass