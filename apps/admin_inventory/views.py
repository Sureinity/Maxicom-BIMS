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
    
    # Start with all books
    bookData = Booklist.objects.all()
    
    # Helper function to extract decimal number
    def extract_decimal(call_num):
        try:
            parts = call_num.split()
            if len(parts) >= 2:
                return float(parts[1])
            return None
        except (ValueError, IndexError):
            return None
    
    # Track if we're using filtered lists
    using_filtered_list = False
    
    # Apply collection filter if present
    if collection_filter:
        bookData = bookData.filter(col_code=collection_filter)
    
    # Apply Dewey Decimal filter
    if decimal_start and decimal_end:
        try:
            start_val = float(decimal_start)
            end_val = float(decimal_end)
            bookData = [
                book for book in bookData
                if extract_decimal(book.item_call_num) is not None
                and start_val <= extract_decimal(book.item_call_num) <= end_val
            ]
            using_filtered_list = True
        except ValueError:
            pass

    # Apply Copyright Year filter
    if year_start and year_end:
        try:
            start_year = int(year_start)
            end_year = int(year_end)
            if using_filtered_list:  # If already using a filtered list
                bookData = [
                    book for book in bookData
                    if book.copyrightdate and start_year <= int(book.copyrightdate) <= end_year
                ]
            else:  # If still using queryset
                bookData = bookData.filter(
                    copyrightdate__gte=str(start_year),
                    copyrightdate__lte=str(end_year)
                )
                using_filtered_list = True
        except ValueError:
            pass
    
    # Apply search filter if present
    if search_query:
        if using_filtered_list:  # If using any filtered list
            bookData = [
                book for book in bookData
                if any(search_query.lower() in str(getattr(book, field)).lower() 
                    for field in ['item_call_num', 'barcode', 'title', 'author', 
                                'publisher_code', 'isbn', 'subtitle'])
            ]
        else:  # If still using queryset
            bookData = bookData.filter(
                Q(item_call_num__icontains=search_query) |
                Q(barcode__icontains=search_query) |
                Q(itype__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(publisher_code__icontains=search_query) |
                Q(isbn__icontains=search_query) |
                Q(subtitle__icontains=search_query)
            )

    # Convert to list if still a queryset
    if not isinstance(bookData, list):
        bookData = list(bookData)

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



