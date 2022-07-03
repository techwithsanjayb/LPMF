from dataclasses import fields
from logging import PlaceHolder
from tkinter import Widget
from django import forms
from .models import User


class ImageForm(forms.ModelForm):
    name = forms.CharField(label="Enter Name", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Enter name"}))
    email = forms.EmailField(label="Enter Email", widget=forms.EmailInput(
        attrs={"class": "form-control", "placeholder": "Enter email"}))
    phone = forms.IntegerField(label="Enter Phone No", widget=forms.NumberInput(
        attrs={"class": "form-control", "placeholder": "Enter phone no"}))
    password = forms.CharField(label="Enter Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter password"}))
    Confirm_password = forms.CharField(label="Enter Confirm Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter confirm password"}))

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'password', 'Confirm_password']
        widget = {
            'password': forms.PasswordInput(),
            'Confirm_password': forms.PasswordInput()
        }


class ServiceForm(forms.Form):
    Language = (('English - Marathi', 'English - Marathi'),
                ('Marathi - English', 'Marathi - English'),)
    Select_Language_Pair = forms.ChoiceField(
        label='Select Language Pair', choices=Language)
    CHOICES = [('Inscript', 'Inscript'),
               ('Transliteration', 'Transliteration')]
    Keyboard = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(attrs={"class": "form-control"}))
    inputText = forms.CharField(label='Enter text', max_length=500, widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter Text"}))


class TTSservice(forms.Form):
    Language = (('Hindi', 'Hindi'), ('Tamil', 'Tamil'), ('Marathi', 'Marathi'), ('Rajasthani', 'Rajasthani'),
                ('Telugu', 'Telugu'), ('Malayalam', 'Malayalam'), ('Bengali', 'Bengali'), ('Kannada', 'Kannada'), ('Odia', 'Odia'))
    Select_Language_Pair = forms.ChoiceField(
        label='Select Language Pair', choices=Language, widget=forms.Select(attrs={'class': 'form-control'}))
    Gernder_Select = (('male', 'Male'), ('female', 'Female'),)
    Gender = forms.ChoiceField(label='Select Gender', choices=Gernder_Select,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    InputText = forms.CharField(label='Enter text', max_length=500, widget=forms.Textarea(
        attrs={"class": "form-control", "placeholder": "Enter Text"}))
