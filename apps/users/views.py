from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

from .forms import CustomUserCreationForm
from .models import User

from .decorators import redirect_dashboard_if_loggedin, redirect_login_if_not_loggedin
# Create your views here.


"""
USER CREATION/AUTHENTICATION W/ SESSION MANAGEMENT

Handles login, signup, and logout with session management. Authenticated users 
are redirected to a specific URL, while expired sessions redirect to login/
"""

@never_cache
def user_login(request):
    if request.user.is_authenticated:
        if request.user.sys_acc_role == 0:
            return redirect('admin_dashboard')
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username)
        print(password)
        if user is not None:
            login(request, user)
            if user.sys_acc_role == 0:
                return redirect('admin_dashboard')
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

@redirect_login_if_not_loggedin
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
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
            form = CustomUserCreationForm(form_data)
        else:
            form = CustomUserCreationForm()

    context = {
        "form": form
    }
    print(form.errors)
    return render(request, "signup.html", context)

def user_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect('login')
