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

from django.core.mail import send_mail
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
			
			if form.is_valid():
				
				ITEMS().delete(form.cleaned_data['id'])
				return redirect('param')
			else : 
				return HttpResponse("Invalid request or form not valid.")

		elif request.method=='POST' and request.POST.get('formulaire_id')=="deleteDescription" :
			
			form = descriptionSuppressionForm(request.POST)
			
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
		
		if request.method=='POST' and request.POST['formulaire_id'] == 'devis':
			form = createDevisForm(request.POST)
			if form.is_valid():
				
				try : 
					DEVIS().create(data=form.cleaned_data)
					
				except Exception as error :
					raise(error)
		elif request.method=='POST' and request.POST['formulaire_id'] == 'client':
			form = createClientForm(request.POST)
			if form.is_valid():
				
				try : 
					USERS().create(data=form.cleaned_data)
					
				except Exception as error :
					raise(error)
		myId=request.session["id_user"]
		me=USERS().readOne(myId)
		newDevis=DEVIS().getNewDevis()
		myDevis=DEVIS().getMyDevis(myId)
		otherDevis=DEVIS().getOtherDevis(myId)
		clients = USERS().readAll()
		return render(request,'dashboard.html',{'clients':clients,'newDevis': newDevis, 'myDevis':myDevis, 'otherDevis':otherDevis, 'me':me,
			'forms':{
			'createClientForm' : createClientForm,
			'createDevisForm' : createDevisForm,
			}})
	else : 
		redirect('home')

def archives(request):
	if request.user.is_superuser :

		myId=request.session["id_user"]
		me=USERS().readOne(myId)
		archives=DEVIS().getArchivedDevis()
		return render(request,'archives.html',{'archives': archives,})
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
	if request.user.is_superuser :
		if request.method=='POST' :

		# request pour modifier le contenu d'une ligne de description
			match request.POST.get('formulaire_id') :
				case 'modifyDescription' :
					form = updateDescriptionForm(request.POST)
					if form.is_valid():
						try : 
							LIGNES_DESC_DEVIS().update(objectId=form.cleaned_data['id'],data={'id':form.cleaned_data['id'],'textCustom':form.cleaned_data['textCustom']})
						except Exception as error :
							raise(error)

			# request pour ajouter une ligne de description avec un customText dans le devis	
				case 'addDescription':
					form = addDescriptionForm(request.POST)
					if form.is_valid():
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
						
						try : 
							DEVIS().delete(form.cleaned_data['id'])
						except Exception as error :
							
							raise(error)
						return redirect('dashboard')
				case 'sendEmail':
					print('email')
				case 'dropbox' :
					dataset = DEVIS().initDevis(id)
					try :
						params = {
						'grant_type': 'refresh_token',
						'refresh_token': env('DROPBOX_REFRESH_TOKEN'),
						'client_id': env('DROPBOX_KEY').strip(),
						'client_secret': env('DROPBOX_SECRET'),
						}
						# CODE A GARDER, RECUPERE REFRESH TOKEN A L'AIDE DU CODE GENERE SUR : 
						# https://www.dropbox.com/oauth2/authorize?client_id=<API_ACCESS_KEY>&token_access_type=offline&response_type=code
						# url = "https://api.dropbox.com/oauth2/token"
						# data = {
						#     'grant_type': 'authorization_code',
						#     'code': 'Vvzmc0OTWPMAAAAAAAFa1dpap8NNT8Nf0cdN05UG0Uk',
						#     'client_id': env('DROPBOX_KEY').strip(),
						#     'client_secret': env('DROPBOX_SECRET'),

						# }

						# response = requests.post(url, data=data)
						# access_token = response.json()["access_token"]
						# refresh_token = response.json()["refresh_token"]
						# print(f'refresh : {refresh_token}')

						response = requests.post('https://api.dropbox.com/oauth2/token', data=params)
						response_data = response.json()
						access_token=response_data["access_token"]
						dbx = dropbox.Dropbox(access_token)
						folder_name = f'devis{id}'

						try :
							folder_metadata=dbx.files_get_metadata(f'/{folder_name}')
						except ApiError as e:
							dbx.files_create_folder('/' + folder_name)
							print(f"API error: {e}")

						link = dbx.sharing_create_shared_link(path=f'/{folder_name}', short_url=False)
						
						dropboxUrl = link.url[:len(link.url)-5]
						
						return render(request,'devis.html', {'data' :dataset, 
						'forms':{
						'updateDescriptionForm' : updateDescriptionForm, 
						'descriptionSuppressionForm': descriptionSuppressionForm,
						'addDescriptionForm':addDescriptionForm, 
						'updateDevisStatusForm':updateDevisStatusForm,
						'updateQuantityForm':updateQuantityForm,
						'createLineItemForm':createLineItemForm,
						'deleteDevisForm':deleteDevisForm,
						}, 'dropboxUrl':dropboxUrl,})

					except AuthError as e:
						print(f"Authentication error: {e}")


					
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
			}, 'dropboxUrl':'',})
	else : 
		return redirect('home')

def contact(request):
	if request.method=="POST":
		form = contactForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			# Process the form data
		# 	send_mail(
		#     form.cleaned_data['subject'],
		#     f'<h6>{form.cleaned_data["email"]}</h6><hr/><p>{form.cleaned_data["message"]}</p>',
		#     env('EMAIL_SENDER'),
		#     ["ignaceberard@hotmail.com"],
		#     fail_silently=False,
		# )
			message = Mail(
		    from_email=env('EMAIL_SENDER'),
		    to_emails='ignacebernard@hotmail.com',
		    subject=form.cleaned_data['subject'],
		    html_content = f'<h6>{form.cleaned_data["email"]}</h6><hr/><p>{form.cleaned_data["message"]}</p>')
			try:
				print(env('SENDGRID_API_KEY'))
				print(message)
				sg = SendGridAPIClient(env('SENDGRID_API_KEY'))
				response = sg.send(message)
				print(response.status_code)
				print(response.body)
				print(response.headers)
			except Exception as e:
				print("SendGrid API Error:", e)
		else:
			return HttpResponse(400)

	return render(request,'contact.html',{'contactForm':contactForm})

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
