from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.core.validators import MaxLengthValidator


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, label="Username", widget=forms.TextInput(
        attrs={'placeholder': 'username'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your Email'}))
    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))
    password2 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(
        attrs={'placeholder': 'password'}))

    aadhar_id = forms.CharField(required=True, validators=[MaxLengthValidator(limit_value=50)], label="Aadhar ID", widget=forms.TextInput(
        attrs={'placeholder': 'Aadhar ID'}))
    annual_income = forms.DecimalField(required=True, label="Annual Income", widget=forms.TextInput(
        attrs={'placeholder': 'Annual Income'}))  

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','aadhar_id', 'annual_income')


class CustomerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

