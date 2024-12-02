from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Booklist, Inventory
from apps.users.models import User
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
    # Overview
    bookCount = Booklist.objects.count()
    bookScanned = Inventory.objects.count()
    bookUnscanned = bookScanned - Inventory.objects.exclude(status__in=[1, 2, 3, 4]).count()
    totalUsers = User.objects.exclude(sys_acc_role=0).count()

    # Book states
    goodCondition= Inventory.objects.filter(status=1).count()
    noBarcodeTag = Inventory.objects.filter(status=2).count()
    forRepair = Inventory.objects.filter(status=3).count()
    forDisposal = Inventory.objects.filter(status=4).count()

    context = {
        # Overview
        "bookCount": bookCount,
        "bookScanned": bookScanned,
        "bookUnscanned": bookUnscanned,
        "totalUsers": totalUsers,

        # Book states
        "goodCondition": goodCondition,
        "noBarcodeTag": noBarcodeTag,
        "forRepair": forRepair,
        "forDisposal": forDisposal
    }
    # if request.method == "GET" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
    #     return JsonResponse({
    #         # Overview
    #         "bookCount": bookCount,
    #         "bookScanned": bookScanned,
    #         "bookUnscanned": bookUnscanned,
    #         "totalUsers": totalUsers,
    #
    #         # Book states
    #         "goodCondition": goodCondition,
    #         "noBacodeTag": noBacodeTag,
    #         "forRepair": forRepair,
    #         "forDisposal": forDisposal
    #     })
    return render(request, "pages/dashboard_page.html", context)

@admin_required
def listbooks_page(request):
    book_list = Booklist.objects.all()
    
    # Get the page number from the query parameters, default to 1
    page_number = request.GET.get('page', 1)
    
    # Number of items per page (matches your dropdown options: 10, 20, 30, 40)
    items_per_page = request.GET.get('show', 10)
    
    # Create a paginator object
    paginator = Paginator(book_list, items_per_page)
    
    # Get the page object
    page_obj = paginator.get_page(page_number)
    
    context = {
        "bookData": page_obj,
        "page_range": paginator.page_range,
        "current_page": int(page_number),
        "total_pages": paginator.num_pages,
    }
    
    return render(request, "pages/listbooks_page.html", context)

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



