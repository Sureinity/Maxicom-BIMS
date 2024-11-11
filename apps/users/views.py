from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.cache import never_cache

from  django.contrib.auth.forms import UserCreationForm
from .forms import ManualInputBarcodeForm

from django.contrib.auth.decorators import login_required
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

@redirect_login_if_not_loggedin
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

def user_logout(request):
    if request.method == "POST":
        logout(request)
    return render(request, 'index.html')


"""
BARCODE SCANNING/INPUT

Two methods are implemented: Camera scanning and manual input.
Scanning uses QuaggaJS library with AJAX for backend integration.
"""

@redirect_dashboard_if_loggedin
def dashboard(request):
    return render(request, "mainpage.html")

@redirect_dashboard_if_loggedin
def barcode_scan(request):
    return render(request, "barcode_scanner.html")

@redirect_dashboard_if_loggedin
def barcode_input(request):
    form = ManualInputBarcodeForm()
    return render(request, "barcode_input.html")


# TODO: There is a slight conflict in URL naming that causes 'scanner_process_barcode' to redirect to 'input_process_barcode'. Might check the affected templates later.
@redirect_dashboard_if_loggedin
def scanner_process_barcode(request):
    if request.method == "POST":
        barcode = request.POST.get('barcode')
        print(f"Received barcode: {barcode}")
        
        redirect_url = reverse('scanner_process_barcode')
        print(f"Redirect URL: {redirect_url}")

        #Uses session to retrieve barcode as input value on template
        request.session["scanned_barcode"] = barcode
        
        return JsonResponse({
            'success': True,
            'message': f'Barcode processed: {barcode}',
            'redirect_url': redirect_url
        })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

@redirect_dashboard_if_loggedin
def input_process_barcode(request):
    if request.method == "POST":
        barcode = request.POST.get("barcode_manual")
        print(barcode)
    
    return render(request, "book_details.html", {"barcode_result": barcode})

        



    
