from django.shortcuts import render,redirect
from .models import User
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request,'index.html')

def home(request):
    if 'email' in request.session:
        current_user=request.session['email']
        param={'current_user': current_user}
        return render(request,'home.html',param)
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        pwd=request.POST.get('password')
        check_user=User.objects.filter(email=email,password=pwd)
        if check_user:
            request.session['email']=email
            return redirect('home')
        else:
            error='Invalid Email id or password'
            return render(request, 'login.html',{'error':error})
    return render(request,'login.html')
    
def signup(request):
    if request.method == "POST":
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email= request.POST.get('email')
        pwd = request.POST.get('password')
        if User.objects.filter(email=email).count()>0:
            error='This Email is already exist'
            return render(request, 'signup.html',{'error':error})
        else:
            user=User(email=email,password=pwd,first_name=fname,last_name=lname)
            user.save()
            messages.success(request, 'Account created successfully.')
            return redirect('login')
    else:
        return render(request, 'Signup.html')

def logout(request):
    try:
        del request.session['email']
    except:
        return redirect('index')
    return redirect('index')
