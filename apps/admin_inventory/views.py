from django.shortcuts import render
from django.core.paginator import Paginator

from .decorators import admin_required

"""
ADMIN SIDE | INVENTORY

Description is yet to come...
"""
# Create your views here.
@admin_required
def admin_page(request):    # This view is for rendering the main container of admin dasboard page
    return render(request, "admin_main.html")

@admin_required
def dashboard_page(request):
    return render (request, "pages/dashboard_page.html")

@admin_required
def listbooks_page(request):
    data = range(1, 101)  # Example data: numbers from 1 to 100
    paginator = Paginator(data, 10)  # 10 items per page

    # Get the current page number from the request, default to the first page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)  # Automatically handles invalid page numbers

    return render(request, "pages/listbooks_page.html", {'page_obj': page_obj})

@admin_required
def inventory_page(request):
    return render (request, "pages/inventory_page.html")

@admin_required
def usersettings_page(request):
    return render (request, "pages/usersettings_page.html")


# Hamburger pages
@admin_required
def goodcon_page(request):
    return render (request, "pages/goodcon_page.html")

@admin_required
def nobarcode_page(request):
    return render (request, "pages/nobarcode_page.html")

@admin_required
def forrepair_page(request):
    return render (request, "pages/forrepair_page.html")

@admin_required
def fordisposal_page(request):
    return render (request, "pages/fordisposal_page.html")



