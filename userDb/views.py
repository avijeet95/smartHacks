from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import Person
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
# Create your views here.

@csrf_exempt
@require_POST
def login(request):
	response_data = {}
	print request
	input = request.POST
	print input

	try :
		obj = Person.objects.get(uid=input['uid'])
		

	except Person.DoesNotExist:
		name = Person.objects.create(uid=input['uid'],fname=input['fname'],lname=input['lname'],email=input['email'],gender=input['gender'],address=input['address'],aadhar=input['aadhar'],credit=input['credit'],isWorker=False)
		response_data['success'] ='1'
		response_data['new-user']='1'
		print response_data
		return JsonResponse(response_data)
	else:
		response_data['success'] = '1'
		response_data['new-user'] = '0'
		print response_data
		return JsonResponse(response_data)
@csrf_exempt
@require_POST
def updateCredit(request):
	response_data = {}
	uid = request.POST["uid"]

	try:
		obj = Person.objects.get(uid=uid)
		obj.credit = request.POST['credit']
		obj.save()
	except:
		response_data["success"] = "0"
		return JsonResponse(response_data)
	else:
		response_data["success"]="1"
		return JsonResponse(response_data)

@csrf_exempt
@require_GET
def fetchUser(request):
	response_data ={}
	input = request.GET
	print input['uid']
	try:
		obj = Person.objects.get(uid=input['uid'])
		print obj
		response_data["user"] = serializers.serialize('json', [ obj, ])
	except:
		response_data["success"] = "0"
		return JsonResponse(response_data)
	else:
		response_data["success"] = "1"
		return JsonResponse(response_data)
# @csrf_exempt
# @require_POST




