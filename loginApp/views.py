from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import CustomerSignUpForm, CustomerLoginForm
from .models import CustomerSignUp
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .task import *
# Create your views here.


def sign_up_view(request):

    error = ''
    if request.user.is_authenticated:

        return HttpResponseRedirect(reverse('home'))

    form = CustomerSignUpForm()
    if request.method == 'POST':

        form = CustomerSignUpForm(request.POST)
        # print(form.cleaned_data['username'])
        if form.is_valid():


            user = form.save()

            user_profile = CustomerSignUp(user=user, aadhar_id=form.cleaned_data['aadhar_id'],annual_income=form.cleaned_data['annual_income'] )
            print(user_profile)
            user_profile.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            print(username,password1)
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)
                print(user_profile.aadhar_id)
                calculate_credit_score(user_profile.aadhar_id)       
                return HttpResponseRedirect(reverse('home'))

            return HttpResponseRedirect(reverse('login_App:login_customer'))

        else:
            if User.objects.filter(username=request.POST['username']).exists():
                error = 'customer already exists'

            else:
                error = 'Your password is not strong enough or both password must be same'
        

    return render(request, 'loginApp/signup.html', context={'form': form, 'user': "Customer Register", 'error': error})


def login_view(request):
    form = CustomerLoginForm()
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST)
        # username = request.POST['username']
        # password = request.POST['password']
        # print(username, password)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        else:
            return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login", 'error': 'Invalid username or password'})
    return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login"})


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

