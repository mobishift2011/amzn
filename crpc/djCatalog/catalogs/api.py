# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import Brand, BrandTask

def JSONResponse(response):
	return HttpResponse(simplejson.dumps(response))

def brands(request):
	brands = Brand.objects(is_delete=False)
	res = {
		'response': [brand.title for brand in brands]
	}
	return JSONResponse(res)

@csrf_exempt
def brandTasksHandle(request):
	if request.method == 'GET':
		params = request.GET
		brand_complete = params.get('brand_complete')
		if brand_complete =='True':
			tasks = BrandTask.objects(brand_complete=True)
			tab = 'extracted'
		else:
			tasks = BrandTask.objects(brand_complete=False)
			tab = 'unextracted'

		if params.get('format', '').lower() == 'json':
			return JSONResponse({
				'response': [task.to_json() for task in tasks]
			})
		else:
			return render(request, 'brandtask.html', {'tasks': [task.to_json() for task in tasks], 'tab': tab}) 

@csrf_exempt
def brandTaskHandle(request, task_id):
	if request.method == 'POST':
		task = BrandTask.objects.get(pk=task_id)
		if task:
			params = request.POST
			brand_complete = params.get('brand_complete', task.brand_complete)
			is_checked = params.get('is_checked', task.is_checked)
			task.brand_complete = True if brand_complete == 'True' or brand_complete == True else False
			task.is_checked = True if is_checked == 'True' or is_checked == True else False
			task.save()
			return  JSONResponse({
					'code': 0,
					'response': None,
					'message': 'updated successfully!'
				})
		else:
			return  JSONResponse({
					'code': 1,
					'response': None,
					'message': 'object does not exist!'
				})

def test(request):
	return render(request, 'index.html')