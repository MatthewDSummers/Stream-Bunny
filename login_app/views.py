from django.shortcuts import render,redirect,HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
from login_app.models import *


def login_page(request):
    context = {
        "login_page" : True,
    }
    return render(request,"login_page.html",context)

def success(request):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            'user' : User.objects.get(id=user_id)
        }
        return render(request,"success.html",context)
    else:
        return redirect('/stream-bunny')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    request.session['errors'] = errors
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    birthday = request.POST['birthday']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    request.session['first_name'] = first_name
    request.session['last_name'] = last_name
    request.session['birthday'] = birthday
    request.session['email'] = email
    request.session['password'] = password
    request.session['confirm_password'] = confirm_password
    if len(errors) > 0:
        # for key, value in errors.items():
        #     messages.error(request,value)
        return redirect('/stream-bunny/login')
    else:
        request.session.flush()
        password_bcrypt = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name,last_name=last_name,birthday=birthday,email=email,password=password_bcrypt)
        request.session['user_id'] = user.id
        # return redirect('/stream-bunny/login/about_me')
        return redirect('/stream-bunny/login/about_me_test')

def login(request):
    request.session.flush()
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        request.session['errors'] = errors
        request.session['login_email'] = request.POST['login_email']
        request.session['login_password'] = request.POST['login_password']
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/stream-bunny/login')
    else:
        # request.session.flush()
        email = request.POST['login_email']
        # password = request.POST['login_password']
        user = User.objects.filter(email=email)[0]
        request.session['user_id'] = user.id
        # if 'errors' in request.session.keys():
        #     del request.session['errors']
        return redirect('/stream-bunny/user_experience')

def logout(request):
    request.session.flush()
    return redirect('/stream-bunny/login')

def child(request):
    context = {
    }
    return render(request,"child.html",context)

def about_me(request, user_id):
    user = User.objects.get(id=user_id)
    user.about = request.POST['about_me']
    user.save()

    return redirect('/stream-bunny/user_experience/user_info_page')

def about_me_page(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        "user" : user,
    }
    return render(request,"about_me.html",context)

def about_me_save(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    user.about = request.POST['about_me']
    user.save()
    return redirect("/stream-bunny/user_experience")

def about_me_test_page(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        "user" : user,
    }
    return render(request,"about_me_test.html",context)

def about_me_test_save(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    if "image" in request.FILES:
        Image.objects.create(
            image=request.FILES['image'],
            name=request.FILES['image'].name,
            user=user
            )
        if "about_me" in request.POST:
            user.about = request.POST['about_me']
            user.save()
    else:
        user.about = request.POST['about_me']
        user.save()
    return redirect("/stream-bunny/user_experience")
