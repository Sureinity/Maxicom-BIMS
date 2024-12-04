from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

from .models import Booklist, Inventory
from .forms import CreateBook
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
    if request.method == "POST":
        try:
            # Extract data from POST request
            barcode = request.POST.get('barcode')
            title = request.POST.get('title')
            subtitle = request.POST.get('subtitle')
            col_code = request.POST.get('col_code')
            author = request.POST.get('author')
            copyrightdate = request.POST.get('copyrightdate')
            date_accessioned = request.POST.get('date_accessioned')
            isbn = request.POST.get('isbn')
            publisher_code = request.POST.get('publisher_code')
            itype = request.POST.get('itype')
            item_call_num = request.POST.get('item_call_num')
            copy_num = request.POST.get('copy_num')
            volume = request.POST.get('volume')
            edition_stmt = request.POST.get('edition_stmt')
            paidfor = request.POST.get('paidfor')
            price = request.POST.get('price')
            bookseller_id = request.POST.get('bookseller_id')

            # Create and save the Booklist object
            book = Booklist(
                barcode=barcode,
                title=title,
                col_code=col_code,
                subtitle=subtitle,
                author=author,
                copyrightdate=copyrightdate,
                date_accessioned=date_accessioned,
                isbn=isbn,
                publisher_code=publisher_code,
                itype=itype,
                item_call_num=item_call_num,
                copy_num=copy_num,
                volume=volume,
                edition_stmt=edition_stmt,
                paidfor=paidfor,
                price=price,
                bookseller_id=bookseller_id
            )

            # Perform clean method validation (optional)
            book.clean()

            # Save the book instance to the database
            book.save()

  # Redirect to a success page or return a success response
        except ValidationError as e:
            # Handle validation error
            return HttpResponse(f"Error: {e.message}", status=400)
    return redirect("admin_listbooks")


@admin_required
def update_listbooks_page(request, id):
    return redirect("admin_listbooks")

@admin_required
def delete_listbooks_page(request, id):
    book = get_object_or_404(Booklist, id=id)
    if request.method == "POST":
        book.delete()

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



