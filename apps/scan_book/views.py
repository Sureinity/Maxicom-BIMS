from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .forms import ManualInputBarcodeForm

from .decorators import redirect_dashboard_if_loggedin, redirect_login_if_not_loggedin, not_authorized

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


@redirect_dashboard_if_loggedin
def ajax_scanner_process_barcode(request):
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
def scanner_process_barcode(request):
    return render(request, "book_details.html", {"scanner_process_barcode": request.session.get('scanned_barcode')})

@redirect_dashboard_if_loggedin
def input_process_barcode(request):
    print(request.path)
    if request.method == "POST":
        barcode = request.POST.get("barcode_manual")
        print(barcode)
    
    return render(request, "book_details.html", {"barcode_result": barcode})

