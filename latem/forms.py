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