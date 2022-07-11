from dataclasses import fields
from logging import PlaceHolder
from tkinter import Widget
from xml.dom import ValidationErr
from django import forms
from django.core import validators


'''
    AUTHOR NAME      : Shweta Patil
    CREATED DATE     : 05-07-2022
    MODEL NAME       : Registration And login
'''
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, UsernameField
from django.core.validators import RegexValidator


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


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        max_length=60,
        required=True,
        help_text='Enter First Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    middle_name = forms.CharField(
        max_length=60,
        required=True,
        help_text='Enter Middle Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Middle Name'})
    )

    last_name = forms.CharField(
        max_length=60,
        required=True,
        help_text='Enter Last Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )

    email = forms.EmailField(
        max_length=60,
        required=True,
        help_text='Enter Email Address',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )

    username = forms.CharField(
        max_length=60,
        required=True,
        help_text='Enter Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(
        help_text='Enter Phone Number',
        validators=[phone_regex],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Phone Number'})

        # max_length=17,
    )  # Validators should be a list

    address = forms.CharField(
        max_length=200,
        required=True,
        help_text='Enter Address',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Address'})
    )

    password1 = forms.CharField(
        max_length=30,
        help_text='Enter Password',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )

    password2 = forms.CharField(
        max_length=30,
        required=True,
        help_text='Enter Password Again',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
    )

    CHOICES = [('Individual', 'Individual'),
               ('Organization', 'Organization'),
               ('DomainExpert', 'DomainExpert')]

    User_Type = forms.ChoiceField(required=True, help_text='Select User Type', choices=CHOICES,
                                  widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select User Type'}))

    check = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'username', 'phone_number', 'password1', 'password2', 'check',
        ]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        ))

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',

            }
        ))


class TranslationQuoteForm(forms.Form):
    url = forms.URLField(validators=[validators.MaxLengthValidator(200), validators.URLValidator(
    )], required=True, widget=forms.URLInput(attrs={'class': 'form-control trans_url', 'placeholder': 'Enter URL'}))

    languages = [('hindi', 'Hindi'), ('marathi', 'Marathi'), ('tamil', 'Tamil'), ('bengali', 'Bengali'), ('gujarati','Gujarati'),('telugu','Telugu')]
    language = forms.ChoiceField(validators=[validators.MaxLengthValidator(20)], required=True, help_text='Select Language',
                                 choices=languages, widget=forms.Select(attrs={'type': 'date', 'class': 'form-select trans_language'}),)

    types = [('transport', 'Transport'), ('medical', 'Medical'), ('travel', 'Travel and Tourism'), ('educational','Educational'),('ecommerce','E-Commerce')]
    website_type = forms.ChoiceField(validators=[validators.MaxLengthValidator(
        30)], required=True, choices=types, widget=forms.Select(attrs={'type': 'date', 'class': 'form-select trans_type'}),)

    delivery_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'class': 'form-control trans_date'}), required=True)
