from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .forms import UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.views.decorators import gzip

# import cv2
import requests
import json
import time

from .serializers import UserSerializer
from .models import Users
from .controlers import *

def home(request) :

	return render(request, 'home.html')

def description_real(request,name) :
	return render(request, f'{name}.html')

def account(request):
	if request.user.is_authenticated:
		if request.user.is_superuser :
			return redirect('dashboard')
		return render(request, 'account.html')
	else :
		return redirect('login')
def param(request):
	if request.user.is_superuser :
		if request.method=='POST' and request.POST['nameElem']:
			data={
				'name':request.POST['nameElem'],
				'description':request.POST['descElem'],
					}
			ITEMS().create(data=data)
			return redirect('param')
		elif request.method=='POST' and request.POST['nameDesc'] :
			

		allItems = ITEMS().readAll()
		allDescription = DESCRIPTION_ITEMS().readAll()
		return render(request, 'param.html', {'items': allItems, 'description' : allDescription})
	else :
		return redirect('home')
def dashboard(request):
	if request.user.is_superuser :
		myId=request.session["id_user"]
		me=USERS().readOne(myId)
		newDevis=DEVIS().getNewDevis()
		myDevis=DEVIS().getMyDevis(myId)
		otherDevis=DEVIS().getOtherDevis(myId)
		return render(request,'dashboard.html',{'newDevis': newDevis, 'myDevis':myDevis, 'otherDevis':otherDevis, 'me':me})
	else : 
		redirect('home')

def log_in(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			request.session["id_user"]=user.first_name
			request.session.save()
			return redirect('account')
		else:
			pass

			return render(request, 'login.html',{'responses':'no'})

	else:
		return render(request, 'login.html')

def log_out(request):
	logout(request)
	return redirect('home')

def signup(request):
	if request.method=='POST':
		# check if the data is viable
		formUserData={
				"email" : request.POST.get('email'),
				"password1" : request.POST.get('password1'),
				"password2" : request.POST.get('password2'),
				"username" : request.POST.get('email'),
				"first_name":'',
				}
		form = UserCreationForm(formUserData)
		if form.is_valid():
			try :
				# create entry in latem.users table 
				userData={
					"email" : request.POST.get('email'),
					"firstName" : request.POST.get('firstName'),
					"lastName" : request.POST.get('lastName'),
					"telephone" : request.POST.get('telephone'),
					"isAdmin":False,
				}

				addUser = USERS().create(data=userData)
				if addUser == 'fail':
					return render(request, 'signup.html')
		
				# Assign the id of the latem.users object to first_name
				newUser = Users.objects.get(email=userData['email'])
				formUserData['first_name']=newUser.id

				# update the formUserData and save the user in the django.user table
				form=UserCreationForm(formUserData)
				if form.is_valid() :
					form.save()
					user = authenticate(request, username=formUserData['email'], password=formUserData['password1'])
				
					if user is not None:
						login(request, user)
						request.session["id_user"]=user.first_name
						request.session.save()
						return redirect('account')
				else : 
					return render(request, 'signup.html', {"message": 'unknown error'})
				

			except Exception as error : 
					print(error)
					return render(request, 'signup.html', {"message": form.errors})
		else : 
			try :
				form.save()
			except Exception as error : 
				return render(request, 'signup.html',{"message": form.errors})
	else : 

		return render(request,'signup.html')