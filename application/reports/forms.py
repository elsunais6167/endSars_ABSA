from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

from .models import *

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AdminForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm Password'
    )

    
    CUSTOM_ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Reporter', 'Reporter'),
    ]

    role = forms.ChoiceField(
        choices=CUSTOM_ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Register User as'
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'role', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class IncidenceForm(ModelForm):
    class Meta:
        model = Incidence
        fields = ['title', 'social_media', 'content', 'gis_location']
        widgets = {
            'social_media': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'gis_location': forms.HiddenInput(),
        }

        labels = {
            'title': 'What Topic is the Post About?',
            'social_media': 'Which Social Media Handle, do you See this Post?',
            'content': 'Type the Content of the Post Here!'
        }

class CategoryForm(ModelForm):
    class Meta:
        model = KnowledgeCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': 'Category Name',
            'description': 'Use one sentence to describe category',
        }

class ExpertForm(ModelForm):
    class Meta:
        model = ExpertKnowledge
        fields = ['title', 'content', 'categories']
        widgets = {
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = KnowledgeComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }

        