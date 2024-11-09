from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.cache import never_cache

from  django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from .decorators import redirect_dashboard_if_loggedin
# Create your views here.

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            request.session['form_data'] = {'username': username}
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    
    else:
        # Get stored form data if it exists
        pass
        form_data = request.session.pop('form_data', None)
        username = form_data.get('username', '') if form_data else ''
        
    return render(request, 'index.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            print("error")
            request.session['form_data'] = request.POST
            return redirect('signup')
    else:
        form_data = request.session.pop('form_data', None)
        if form_data:
            form = UserCreationForm(form_data)
        else:
            form = UserCreationForm()

    context = {
        "form": form
    }

    return render(request, "signup.html", context)

@redirect_dashboard_if_loggedin
def dashboard(request):
    return render(request, "mainpage.html")

@redirect_dashboard_if_loggedin
def barcode_scan(request):
    return render(request, "barcode_scanner.html")
    
