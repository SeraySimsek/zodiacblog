from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *
from blog.models import Customer

class RegistrationForm(UserCreationForm):
    name = forms.CharField()
    lastname = forms.CharField()
    email = forms.CharField()
    job = forms.CharField()
    zodiac = forms.CharField()
    gender_choice = (('E', 'Erkek'), ('K', 'Kadın'))
    gender = forms.ChoiceField(choices=gender_choice)
    relationship_choice = (('V', 'Var'), ('Y', 'Yok'))
    relationship = forms.ChoiceField(choices=relationship_choice)

    class Meta:
        model = User
        fields = ['username', 'name', 'lastname', 'email', 'job', 'zodiac', 'gender', 'relationship', 'password1', 'password2' ]
        exclude = ['user']


class Hesabım(forms.ModelForm):
   class Meta:
      model = Customer
      fields = ['name','lastname','zodiac','email']


class PostForm(forms.ModelForm):
   class Meta:
      model = post
      fields = ['title', 'content', 'zodiac_type']
      exclude = ['customer', 'date_added', 'post_type', 'post_for']

class FortuneTellingForm(forms.ModelForm):
    class Meta:
        model = FortuneTelling
        fields = ['pic']
        exclude = ['from_user', 'is_ok', 'to_user', 'date_added', 'date_review']

class ContactForm(ModelForm):
   class Meta:
      model = Contact
      fields = ['comment']
      widgets = {
          'comment': forms.Textarea(attrs={'class': 'form-control'}),
      }