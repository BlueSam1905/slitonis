from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from posts.models import Post




class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Enter Username",
        'class':"form-control form-control-lg"
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Enter Password",
        'class':"form-control form-control-lg"
        }))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",'password1','password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Enter Username",
        'class':"form-control form-control-lg"
        }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "placeholder":"Enter Email",
        'class':"form-control form-control-lg"
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Enter Password",
        'class':"form-control form-control-lg"
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder":"Enter Password again",
        'class':"form-control form-control-lg"
        }))


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content')
