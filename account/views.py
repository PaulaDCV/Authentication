from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from account.models import Account
from account.forms import RegistrationForm, AuthenticateUsersForm, ReCAPTCHAForm
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import PasswordChangeForm
import urllib
import json
from websiteapp import settings
# Create your views here.
def homeView(request):
    context = {}
    users = Account.objects.all()
    context["accounts"] = users
    return render(request, "home.html", context)

def registerView(request):
    context= {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("customer_email")
            raw_password=form.cleaned_data.get("password1")
            us = authenticate(customer_email = email,password =raw_password)
            login(request,us)
            return redirect("successR")
        else:
            context["registration_form"]= form
    else:
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "register.html",context)


def loginView(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = AuthenticateUsersForm(request.POST)
        if form.is_valid():
            #Validation Captcha
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            #end validation

            email = request.POST['customer_email']
            password = request.POST['password']
            user = authenticate(customer_email=email, password=password)
            if user and result["success"]:
                messages.success(request, "logged in user successfully ")
                login(request, user)
                return redirect("successL")
    else:
        form = AuthenticateUsersForm()
    context['login_form'] = form
    context['captcha'] = ReCAPTCHAForm()
    return render(request, "login.html", context)

def logoutView(request):
    logout(request)
    return redirect("home")

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():

            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('successP')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {
        'form': form
    })

