from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .forms import ManualInputBarcodeForm
from apps.admin_inventory.models import Booklist

from .decorators import redirect_dashboard_if_loggedin, redirect_login_if_not_loggedin, admin_is_not_authorized

"""
BARCODE SCANNING/INPUT

Two methods are implemented: Camera scanning and manual input.
Scanning uses QuaggaJS library with AJAX for backend integration.
"""

@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def dashboard(request):
    return render(request, "mainpage.html")

@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def barcode_scan(request):
    return render(request, "barcode_scanner.html")

@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def barcode_input(request):
    form = ManualInputBarcodeForm()
    return render(request, "barcode_input.html")

@admin_is_not_authorized
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

@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def scanner_process_barcode(request):
    barcode = request.session.get('scanned_barcode')
    book_details = Booklist.objects.get(barcode=barcode)

    return render(request, "book_details_scanner.html", {
        "scanner_process_barcode": request.session.get('scanned_barcode'),
        "book_details": book_details
    })


@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def input_process_barcode(request):
    print(request.path)
    if request.method == "POST":
        barcode = request.POST.get("barcode_manual")
        book_details = Booklist.objects.get(barcode=barcode)
        print(barcode)
    
    return render(request, "book_details.html", {"barcode_result": barcode, "book_details": book_details})

