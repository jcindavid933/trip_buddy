from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt
from django.core import serializers
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage
import imghdr

def index(request):
    return render(request, 'login_register/index.html')

def success(request):
    if "login_id" not in request.session:
        return redirect ('/')
    return render(request, 'travel/index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    elif request.method == 'POST':
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], age=request.POST['age'], password=hashpw.decode())
        request.session['login_id'] = user.id
        request.session['name'] = user.first_name
        request.session['count'] = 0
    return redirect('/travels/')

def email(request):
    error = User.objects.email_validator(request.POST)
    if error:
        context = {
            'email': error['email'],
            # 'email_exist': error['email_exists']
        }
        return render(request, 'login_register/validation.html', context)
    pass

def age(request):
    error_age = User.objects.age_validator(request.POST)
    if error_age:
        for error in error_age:
            messages.error(request, error_age[error])
        return render(request, 'login_register/validation.html')
    pass

def password(request):
    error = User.objects.pass_validator(request.POST)
    if error:
        context = {
            'password': error['password'],
        }
        return render(request, 'login_register/validation.html', context)
    pass

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect('/')
    elif request.method == 'POST':
        user = User.objects.filter(email=request.POST['login_email'])
        request.session['login_id'] = user[0].id
        request.session['name'] = user[0].first_name
        request.session['count'] = 1
    return redirect('/travels/')

def login_page(request):
    return render (request, 'login_register/login.html')

def reset(request):
    request.session.clear()
    return redirect('/')
