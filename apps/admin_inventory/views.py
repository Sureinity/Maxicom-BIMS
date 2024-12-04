from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
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
    bookData = Booklist.objects.all()

    page_number = request.GET.get('page')
    items_per_page = request.GET.get('show', 10)
    paginator = Paginator(bookData, items_per_page)
    page_obj = paginator.get_page(page_number)
    
    # if request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
    #     bookData = list(page_obj.object_list.values())
        
    #     return JsonResponse({
    #         "books": bookData,
    #         "has_next": page_obj.has_next(),
    #         "has_previous": page_obj.has_previous(),
    #         "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
    #         "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
    #         "num_pages": paginator.num_pages
    #     })

    context = {
        "bookData": page_obj,
        "page_range": paginator.page_range,
        "current_page": int(page_number) if page_number else 1,
        "total_pages": paginator.num_pages,
    }
    
    return render(request, "pages/listbooks_page.html", context)

@admin_required
def create_listbooks_page(request):
#    if request.method == "POST":
    return redirect("admin_listbooks")


@admin_required
def update_listbooks_page(request, id):
    return redirect("admin_listbooks")

@admin_required
def delete_listbooks_page(request, id):
    book = get_object_or_404(Booklist, id=id)

    if request.method == "POST":
        book.delete()
        messages.success(request, "Fruit succesfully deleted!")
    else:
         messages.error(request, "Deletion error!")


    return redirect("admin_listbooks")

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



