from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2","username","first_name")

class ItemCreationForm(forms.Form):
    name = forms.CharField(label="name", max_length=100)
    description = forms.CharField(label="description", max_length=100,)

class descriptionCreationForm(forms.Form):
    name = forms.CharField(label="name", max_length=100)
    description = forms.CharField(label="description", max_length=100)
    description_type = forms.ChoiceField(label="description_type",    choices=(
            ('charac','charac'),
            ('finitions','finitions')
        ))
    parent_description = forms.IntegerField(label="parent_description_id")
    parent_item = forms.IntegerField(label="parent_item_id")
    apply_on_all_items=forms.BooleanField(required=False)    
    level = forms.IntegerField(label="level")
