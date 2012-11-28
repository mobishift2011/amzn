# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import Brand, Fail

def JSONResponse(response):
	return HttpResponse(simplejson.dumps(response))

def brands(request):
	brands = Brand.objects(is_delete=False)
	res = {
		'response': [brand.title for brand in brands]
	}
	return JSONResponse(res)

@csrf_exempt
def brandFailHandle(request):
	if request.method == 'GET':
		params = request.GET
		fails = Fail.objects(**params)

		if params.get('format', '').lower() == 'json':
			return JSONResponse({
				'response': [fail.to_json() for fail in fails]
			})
		else:
			return render(request, 'fails.html', {'fails': [fail.to_json() for fail in fails]}) 

	elif request.method == 'POST':
		params = request.POST
		site = params.get('site')
		doctype = params.get('doctype')
		key = params.get('key')
		title = params.get('title')
		model = params.get('model')   # Brand, Dept, Tag
		content = params.get('content') # The content of failure such as the brand name that can'be extacted.
		url = params.get('url')
		
		try:
			fail, is_new = Fail.objects.get_or_create(site=site, doctype=doctype, key=key)
		except Exception, e:
			return  JSONResponse({
					'code': 1,
					'response': None,
					'message': str(e)
				})

		fail.title = title
		fail.model = model
		fail.content = content
		fail.url = url
		try:
			fail.save()
		except Exception, e:
			return JSONResponse({
					'code': 1,
					'response': None,
					'message': str(e)
				})

		return  JSONResponse({
				'code': 0,
				'response': None,
				'message': 'fail info created'
			})

def match(request):
	pass