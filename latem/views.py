from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login
# from .forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views.decorators import gzip

# import cv2
import requests
import json
import time

# def login(request):
# 	if request.method == 'POST':

# 		email = request.POST['username']
# 		password = request.POST['password']
# 		user = authenticate(request, username=email, password=password)
# 		if user is not None:
# 			login(request, user)
# 			request.session["id_user"]=user.id
# 			return redirect('home')
# 		else:
# 			print(Exception)
# 			return render(request, 'login.html',{'responses':'no'})

# 	else:
# 		return render(request, 'login.html')

# def signup(request):
# 	if request.method == 'POST' : 
# 		form = UserCreationForm(request.POST)
# 		userData={
# 				"username" : request.POST.get('email'),
# 				"email" : request.POST.get('email'),
# 				"password1" : request.POST.get('password1'),
# 				"password2" : request.POST.get('password2'),
# 				"first_name" : data.get('id'),
# 				}
# 		if form.is_valid():
# 			try:
# 				serializer = UserSerializer(data=userData)
# 				if serializer.is_valid():
# 					serializer.save()
					
# 				value = requests.post(url, request.POST)
# 				data = json.loads(value.text)
			
# 				userData={
# 				"username" : request.POST.get('email'),
# 				"email" : request.POST.get('email'),
# 				"password1" : request.POST.get('password1'),
# 				"password2" : request.POST.get('password2'),
# 				"first_name" : data.get('id'),
# 				}

# 				form = UserCreationForm(userData)
# 				form.save()
				
# 				user = authenticate(request, username=userData.get('username'), password=userData.get('password1'), id=data.get('id'))
# 				print(user)
# 				if user is not None:
	
# 					login(request, user)
# 					request.session["id_user"]=user.first_name


# 					return redirect('main')
# 				else : 
# 					return redirect('login')

# 			except Exception as error : 
# 				return render(request, 'signup.html', {"message": form.errors})
# 		else:

# 			try :
# 				form.save()
# 			except Exception as error : 
# 				return render(request, 'signup.html',{"message": form.errors})
# 	else : 
# 		return render(request, 'signup.html')
from .serializers import UserSerializer
from .models import Users

def test(request) :
	data = {
		'name' : 'testJEan',
		'email':'test@jean'
	}
	serializer = UserSerializer(data=data)
	if serializer.is_valid() :
		serializer.save()
	return render(request, 'home.html')

def description_real(request,name) :
	return render(request, f'{name}.html')
