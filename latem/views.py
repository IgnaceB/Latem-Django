from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse, HttpResponseServerError
from django.http import JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.views.decorators import gzip
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import dropbox
from dropbox.exceptions import AuthError, ApiError
import logging

# import cv2
import requests
import json
import time

from .serializers import UserSerializer
from .models import Users
from .controlers import *

import environ
env = environ.Env()
environ.Env.read_env()

def home(request) :

	return render(request, 'home.html')

def description_real(request,name) :
	return render(request, f'{name}.html')

def account(request):
	if request.user.is_authenticated:
		if request.user.is_superuser :
			return redirect('dashboard')
		myId=request.session["id_user"]
		allMyDevis=DEVIS().getMyCustomerDevis(myId)
		dataset=[]
		for devis in allMyDevis :
			print(devis)
			dataset.append(DEVIS().initDevis(devis['id']))
		return render(request, 'account.html', {'listOfData':dataset})
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

def devis(request,id):
	try :
		
		dbx = dropbox.Dropbox(env('DROPBOX_ACCESS_TOKEN'))
		folder_name = f'devis{id}'
		try :
			dbx.files_create_folder('/' + folder_name)
		except ApiError as e:
			print(f"API error: {e}")

		folder_metadata=dbx.files_get_metadata(f'/{folder_name}')
		link = dbx.sharing_create_shared_link(path=f'/{folder_name}', short_url=False)
		dropboxUrl = link.url.replace('?dl=0', '')

	except AuthError as e:
		print(f"Authentication error: {e}")

	if request.method=='POST' :

	# request pour modifier le contenu d'une ligne de description
		match request.POST.get('formulaire_id') :
			case 'modifyDescription' :
				form = updateDescriptionForm(request.POST)
				if form.is_valid():
					print(form.cleaned_data)
					try : 
						LIGNES_DESC_DEVIS().update(objectId=form.cleaned_data['id'],data={'id':form.cleaned_data['id'],'textCustom':form.cleaned_data['textCustom']})
					except Exception as error :
						raise(error)

		# request pour ajouter une ligne de description avec un customText dans le devis	
			case 'addDescription':
				form = addDescriptionForm(request.POST)
				if form.is_valid():
					print(form.cleaned_data)
					try : 
						LIGNES_DESC_DEVIS().create(data=form.cleaned_data)
					except Exception as error :
						print(error)
						raise(error)


		# request pour supprimer une ligne de description
			case 'deleteDescription' :
				form = descriptionSuppressionForm(request.POST)
				if form.is_valid():
					try : 
						LIGNES_DESC_DEVIS().delete(form.cleaned_data['id'])
					except Exception as error :
						print(error)
						raise(error)

		# requset pour supprimer un item et l'ensemble de ces descriptions
			case 'deleteItem' :
				form = itemSuppressionForm(request.POST)
				if form.is_valid():
					
					try : 
						LIGNES_ITEMS_DEVIS().delete(form.cleaned_data['id'])
					except Exception as error :
						print(error)
						raise(error)

		# requset pour update un item => textCustom
			case 'updateStatus' :
				
				form = updateDevisStatusForm(request.POST)
				if form.is_valid():
					print(form.cleaned_data)
					try : 
						DEVIS().update(objectId=form.cleaned_data['id'],data=form.cleaned_data)
					except Exception as error :
						print(error)
						raise(error)

		# requset pour modifier la quantité d'un item 			
			case 'updateQuantity' :
				
				form = updateQuantityForm(request.POST)
				if form.is_valid():
					
					try : 
						LIGNES_ITEMS_DEVIS().update(objectId=form.cleaned_data['id'],data=form.cleaned_data)
					except Exception as error :
						print(error)
						raise(error)
		# requset pour modifier la quantité d'un item 			
			case 'addItem' :
				
				form = createLineItemForm(request.POST)
				if form.is_valid():
					
					try : 
						LIGNES_ITEMS_DEVIS().create(data=form.cleaned_data)
					except Exception as error :
						print(error)
						raise(error)
		# requset pour modifier la quantité d'un item 			
			case 'deleteDevis' :
				
				form = deleteDevisForm(request.POST)

				if form.is_valid():
					print('deletedevis')
					try : 
						DEVIS().delete(form.cleaned_data['id'])
					except Exception as error :
						print(error)
						raise(error)
					return redirect('dashboard')
			case 'sendEmail':
				message = Mail(
				from_email='from_email@example.com',
				to_emails='to@example.com',
				subject='Sending with Twilio SendGrid is Fun',
				html_content='<strong>and easy to do anywhere, even with Python</strong>')
				try:
					sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
					response = sg.send(message)
					print(response.status_code)
					print(response.body)
					print(response.headers)
				except Exception as e:
					print(e.message)
				
	dataset = DEVIS().initDevis(id)
	
	return render(request,'devis.html', {'data' :dataset, 
		'forms':{
		'updateDescriptionForm' : updateDescriptionForm, 
		'descriptionSuppressionForm': descriptionSuppressionForm,
		'addDescriptionForm':addDescriptionForm, 
		'updateDevisStatusForm':updateDevisStatusForm,
		'updateQuantityForm':updateQuantityForm,
		'createLineItemForm':createLineItemForm,
		'deleteDevisForm':deleteDevisForm,
		},
		'dropboxUrl':dropboxUrl})


def configurateur(request):
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
	return render(request, 'configurateur.html', {'items': allItems, 'description' : characDescriptions, 'finitions' : finitionsDescriptions,})
