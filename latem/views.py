from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .forms import *
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
		allItems = ITEMS().readAll()
		allDescriptionData = DESCRIPTION_ITEMS().getAllOrderedByLevel()
		maxLevel=DESCRIPTION_ITEMS().getMaxLevel()
		
		characDescriptions = []
		finitionsDescriptions= []
		if maxLevel:
			for x in range(maxLevel+1):
				characDescriptions.append([])
		if allDescriptionData :	
			for desc_data in allDescriptionData:
				desc_item= {
				'id':desc_data['id'],
				'name':desc_data['name'],
				'description':desc_data['description'],
				'apply_on_all_items':desc_data['apply_on_all_items'],
				'parent_item':desc_data['parent_item'],
				'description_type':desc_data['description_type'],
				'parent_description':desc_data['parent_description'],
				'level':desc_data['level'],
				}
				if desc_data['description_type']=='charac':
					characDescriptions[desc_item['level']].append(desc_item)
				elif  desc_data['description_type']=='finitions':
					finitionsDescriptions.append(desc_item)
		
		if request.method=='POST' and 'parent_item' in request.POST:
			form=descriptionCreationForm(request.POST)
			if form.is_valid():
			
				tryCreate = DESCRIPTION_ITEMS().create(data=form.cleaned_data)
				if tryCreate != 'ok':
					
					return render(request, 'param.html', {'items': allItems, 'description' : characDescriptions, 'finitions' : finitionsDescriptions, 
				'ItemCreationForm': ItemCreationForm, 'descriptionCreationForm':descriptionCreationForm, 'formErrors' : tryCreate,
				'itemSuppressionForm' : itemSuppressionForm, 'descriptionSuppressionForm': descriptionSuppressionForm,})
				
				else : 
					return redirect('param')
			else : 
				return render(request, 'param.html', {'items': allItems, 'description' : characDescriptions, 'finitions' : finitionsDescriptions, 
				'ItemCreationForm': ItemCreationForm, 'descriptionCreationForm':descriptionCreationForm, 'formErrors' : form.errors,
				'itemSuppressionForm' : itemSuppressionForm, 'descriptionSuppressionForm': descriptionSuppressionForm,
				})

		elif request.method=='POST' and 'name' in request.POST:
			form = ItemCreationForm(request.POST)
			if form.is_valid():
				ITEMS().create(data=form.cleaned_data)
				return redirect('param')
			else : 
				return render(request, 'param.html', {'items': allItems, 'description' : characDescriptions, 'finitions' : finitionsDescriptions, 
				'ItemCreationForm': ItemCreationForm, 'descriptionCreationForm':descriptionCreationForm, 'formErrors' : form.errors,
				'itemSuppressionForm' : itemSuppressionForm, 'descriptionSuppressionForm': descriptionSuppressionForm,})
		
		elif request.method=='POST' and request.POST.get('formulaire_id')=="deleteItem" :

			form = itemSuppressionForm(request.POST)
			print(form)
			if form.is_valid():
				
				ITEMS().delete(form.cleaned_data['id'])
				return redirect('param')
			else : 
				return HttpResponse("Invalid request or form not valid.")

		elif request.method=='POST' and request.POST.get('formulaire_id')=="deleteDescription" :
			
			form = descriptionSuppressionForm(request.POST)
			print(form)
			if form.is_valid():
				
				DESCRIPTION_ITEMS().delete(form.cleaned_data['id'])
				return redirect('param')
			else : 
				return HttpResponse("Invalid request or form not valid.")


		else : 
		
			return render(request, 'param.html', {'items': allItems, 'description' : characDescriptions, 'finitions' : finitionsDescriptions, 
				'ItemCreationForm': ItemCreationForm, 'descriptionCreationForm':descriptionCreationForm,
				'itemSuppressionForm' : itemSuppressionForm, 'descriptionSuppressionForm': descriptionSuppressionForm,})
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