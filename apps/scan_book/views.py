from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages

from .forms import ManualInputBarcodeForm
from apps.admin_inventory.models import Booklist, Inventory, InventoryHistory

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

    try:
        book_details = Booklist.objects.get(barcode=barcode)
    except Booklist.DoesNotExist:
        return render(request, "scanner_book_not_found.html")            


    return render(request, "book_details_scanner.html", {
        "scanner_process_barcode": request.session.get('scanned_barcode'),
        "book_details": book_details
    })


@admin_is_not_authorized
@redirect_dashboard_if_loggedin
def input_process_barcode(request):
    if request.method == "POST":
        try:
            barcode = request.POST.get("barcode_manual")
            book_details = Booklist.objects.get(barcode=barcode)
        except Booklist.DoesNotExist:
            messages.error(request, "Book not found.")
            print(f"Book with barcode {barcode} does not exist")
            return redirect("barcode_input")
    
    return render(request, "book_details.html", {"barcode_result": barcode, "book_details": book_details})

def submit_status(request):
    if request.method == "POST":
        user = request.user
        bookState = int(request.POST.get("bookstate"))
        barcode = request.POST.get("barcode")
        book = Booklist.objects.get(barcode=barcode)

        try:
            inventory = Inventory.objects.get(book=book)
            inventory.status = bookState
            inventory.save()
        except Inventory.DoesNotExist:
            Inventory.objects.create(book=book, status=bookState)

        try:
            InventoryHistory.objects.create(inventory=inventory, reviewed_by=user, status=bookState)
        except:
            print("Error creating inventory history")

        if request.path == '/barcode-input/input/book-details/submit/':
            return redirect("barcode_input")
        else:
            return redirect("barcode_scan")

    return render(request, "book_details.html", {"barcode_result": barcode, "book_details": book_details})


