from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm,UserCreationForm
from .models import CustomUser
from django.forms.widgets import FileInput


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class NicknameChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('nickname',)

class EmailChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = CustomUser
        fields = ('email',)

class EditCustomUserForm(UserChangeForm):
    
    password = None
    email = None

    biogram = forms.CharField(widget=forms.Textarea(attrs={ 
        'cols': 200,
        'rows': 3,
        'style': 'resize: none; width: 100%',     
    }))

    job = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    own_website_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    linkedin_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    github_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    facebook_url = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))


    class Meta:
        model = CustomUser
        widgets = {
         'profile_picture': FileInput(),
        }
        fields = ('biogram','job','own_website_url','linkedin_url','github_url','facebook_url','profile_picture',)
        
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2',)
