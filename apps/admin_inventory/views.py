from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import Booklist, Inventory
from .forms import CreateBook
from apps.users.models import User
from .decorators import admin_required
from .filters import apply_book_filters

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

    return render(request, "pages/dashboard_page.html", context)

@admin_required
def listbooks_page(request):
    search_query = request.GET.get('search', '')
    collection_filter = request.GET.get('book-collections', '')
    decimal_start = request.GET.get('item-decimal-start', '')
    decimal_end = request.GET.get('item-decimal-end', '')
    year_start = request.GET.get('year-start', '')
    year_end = request.GET.get('year-end', '')
    
    # Apply filters using the reusable function
    bookData = apply_book_filters(
        Booklist.objects.all(),
        search_query=search_query,
        collection_filter=collection_filter,
        decimal_start=decimal_start,
        decimal_end=decimal_end,
        year_start=year_start,
        year_end=year_end
    )

    # Pagination
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('show', 10)
    paginator = Paginator(bookData, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "bookData": page_obj,
        "page_range": paginator.page_range,
        "current_page": int(page_number) if page_number else 1,
        "total_pages": paginator.num_pages,
        "search_query": search_query,
        "collection_filter": collection_filter,
        "decimal_start": decimal_start,
        "decimal_end": decimal_end,
        "year_start": year_start,
        "year_end": year_end,
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
    book = Booklist.objects.get(id=id)
    if request.method == "POST":
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

        book.barcode = barcode
        book.title = title
        book.col_code = col_code
        book.subtitle = subtitle
        book.author = author
        book.copyrightdate = copyrightdate
        book.date_accessioned = date_accessioned
        book.isbn = isbn
        book.publisher_code = publisher_code
        book.itype = itype
        book.item_call_num = item_call_num
        book.copy_num = copy_num
        book.volume = volume
        book.edition_stmt = edition_stmt
        book.paidfor = paidfor
        book.price = price
        book.bookseller_id = bookseller_id

        book.save()

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
