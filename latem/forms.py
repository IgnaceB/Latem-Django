from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2","username","first_name")

class ItemCreationForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100)
    description = forms.CharField(label="Description", max_length=100,)

class descriptionCreationForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100)
    description = forms.CharField(label="Description", max_length=100)
    description_type = forms.ChoiceField(label="description_type",    choices=(
            ('charac','charac'),
            ('finitions','finitions')
        ), widget=forms.HiddenInput)
    parent_description = forms.IntegerField(label="parent_description_id", required=False, widget=forms.HiddenInput)
    parent_item = forms.IntegerField(label="parent_item_id", widget=forms.HiddenInput)
    apply_on_all_items=forms.BooleanField(required=False, widget=forms.HiddenInput)    
    level = forms.IntegerField(label="level", widget=forms.HiddenInput)

class descriptionSuppressionForm(forms.Form):
    id = forms.CharField(label='id', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class itemSuppressionForm(forms.Form):
    id = forms.CharField(label='id', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class addDescriptionForm(forms.Form):
    description_type = 'charac'
    # parent_devis=forms.IntegerField(label="parent_devis", widget=forms.HiddenInput)
    LignesItemsDevisId=forms.IntegerField(label="parent_item_id", widget=forms.HiddenInput)
    textCustom=forms.CharField(label='textCustom', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class updateDescriptionForm(forms.Form):
    id = forms.CharField(label='id', widget=forms.HiddenInput)
    textCustom=forms.CharField(label='textCustom', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class updateDevisStatusForm(forms.Form):
    id = forms.CharField(label='id', widget=forms.HiddenInput)
    status=forms.ChoiceField(  choices = (
        ('réceptionné', 'Réceptionné'),
        ('devis envoyé', 'Devis envoyé'),
        ('validé par le client', 'Validé par le client'),
        ('payé', 'Payé'),
        ('réalisé', 'Réalisé'),
        ('clôturé', 'Clôturé')
    ),widget=forms.HiddenInput, required=False)
    total=forms.CharField(widget=forms.HiddenInput, required=False)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)
    responsableId = forms.IntegerField(widget=forms.HiddenInput, required=False)

class updateQuantityForm(forms.Form):
    id = forms.IntegerField(label='id', widget=forms.HiddenInput)
    quantity = forms.IntegerField(label='quantity', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class createLineItemForm(forms.Form):
    devisId=forms.IntegerField(label='devisId', widget=forms.HiddenInput)
    textCustom=forms.CharField(label='textCustom', widget=forms.HiddenInput)
    quantity = 0
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)

class deleteDevisForm(forms.Form):
    id = forms.CharField(label='id', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)
    
class sendEmailDevis(forms.Form):
    from_email='from_email@example.com'
    to_emails=forms.CharField(widget=forms.HiddenInput)
    subject='Sending with Twilio SendGrid is Fun'        
    html_content=forms.CharField(widget=forms.HiddenInput)

class createClientForm(forms.Form):
    firstName = forms.CharField(required=False, label='Prénom')
    lastName = forms.CharField(required=False, label='Nom')
    email = forms.CharField(label='Email')
    formulaire_id = forms.CharField(widget=forms.HiddenInput,required=False)
    telephone = forms.CharField(required=False,label='Téléphone')
    isAdmin=False

class createDevisForm(forms.Form):
    clientId = forms.CharField(label='id', widget=forms.HiddenInput)
    formulaire_id = forms.CharField(widget=forms.HiddenInput, required=False)