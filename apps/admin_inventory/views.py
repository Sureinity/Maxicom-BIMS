from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q, Count
from django.views.decorators.cache import never_cache
from django.db import IntegrityError
from django.views.decorators.cache import cache_page
from django.contrib.auth import authenticate, login

from .models import Booklist, Inventory, InventoryHistory
from apps.users.models import User
from .decorators import admin_required
from .filters import apply_book_filters

"""
ADMIN SIDE | INVENTORY

Description is yet to come...
"""

@never_cache
@admin_required
def dashboard_page(request):
    # Overview
    bookCount = Booklist.objects.count()
    bookScanned = Inventory.objects.filter(status__in=[1, 2, 3, 4]).count()
    bookUnscanned = bookCount - bookScanned
    totalUsers = User.objects.exclude(sys_acc_role=0).exclude(sys_status=1).count()

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

@never_cache
@admin_required
def listbooks_page(request):
    search_query = request.GET.get('search', '')
    collection_filter = request.GET.get('book-collections', '')
    decimal_start = request.GET.get('item-decimal-start', '')
    decimal_end = request.GET.get('item-decimal-end', '')
    year_start = request.GET.get('year-start', '')
    year_end = request.GET.get('year-end', '')
    
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

@never_cache
@admin_required
def create_listbooks_page(request):
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

        try:
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
            
            book.clean()
            book.save()
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                messages.success(request, 'Book created successfully.')
                return JsonResponse({
                    'success': True,
                    'messages': [{'message': m.message, 'tags': m.tags} for m in messages.get_messages(request)]
                })
            return redirect("admin_listbooks")
            
        except IntegrityError as e:
            messages.error(request, 'This data already exists in the database.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Either the ISBN, barcode, or item call number already exists in the database.',
                    'messages': [{'message': m.message, 'tags': m.tags} for m in messages.get_messages(request)]
                })
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request method'})
    return redirect("admin_listbooks")

@never_cache
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

@never_cache
@admin_required
def delete_listbooks_page(request, id):
    book = get_object_or_404(Booklist, id=id)
    if request.method == "POST":
        book.delete()

    return redirect("admin_listbooks")

@never_cache
@admin_required
def inventory_page(request):
    # Fetch filter parameters from request
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    # Start with all inventory items, excluding books with NOT_FOUND status
    inventoryData = Inventory.objects.select_related('book').exclude(status=5)
    inventoryHistoryData = InventoryHistory.objects.all()
    
    # Apply status filter if present
    if status_filter:
        try:
            status_int = int(status_filter)
            if status_int in [1, 2, 3, 4]:
                inventoryData = inventoryData.filter(status=status_int)
        except ValueError:
            pass
    
    # Apply search filter if present
    if search_query:
        inventoryData = inventoryData.filter(
            Q(book__barcode__icontains=search_query) |
            Q(book__col_code__icontains=search_query) |
            Q(book__title__icontains=search_query) |
            Q(book__author__icontains=search_query)
        )

    # Pagination
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('show', 10)
    paginator = Paginator(inventoryData, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "inventoryData": page_obj,
        "page_range": paginator.page_range,
        "current_page": int(page_number) if page_number else 1,
        "total_pages": paginator.num_pages,
        "search_query": search_query,
        "status_filter": status_filter,
        "inventoryHistoryData": inventoryHistoryData
    }
    
    return render(request, "pages/inventory_page.html", context)

@never_cache
@admin_required
def bookcollections_page(request):
    # Fetch filter parameters from request
    search_query = request.GET.get('search', '')
    collection_filter = request.GET.get('book-collections', '')
    decimal_start = request.GET.get('item-decimal-start', '')
    decimal_end = request.GET.get('item-decimal-end', '')
    year_start = request.GET.get('year-start', '')
    year_end = request.GET.get('year-end', '')
    status_filter = request.GET.get('status', 'found')
    
    # Start with all books and prefetch related inventory data
    base_queryset = Booklist.objects.prefetch_related('inventories').all()
    
    # Apply non-status filters
    filtered_queryset = apply_book_filters(
        base_queryset,
        search_query=search_query,
        collection_filter=collection_filter,
        decimal_start=decimal_start,
        decimal_end=decimal_end,
        year_start=year_start,
        year_end=year_end
    )

    # Calculate counts from filtered queryset before applying status filter
    annotated_queryset = filtered_queryset.annotate(
        found_books=Count('inventories', filter=Q(inventories__status__in=[
            Inventory.GOOD_CONDITION, 
            Inventory.NO_BARCODE_TAG, 
            Inventory.FOR_REPAIR, 
            Inventory.FOR_DISPOSAL
        ])),
        not_found_books=Count('inventories', filter=Q(inventories__status=Inventory.NOT_FOUND))
    )

    # Tabs
    total_books = annotated_queryset.count()
    total_found = sum(book.found_books for book in annotated_queryset)
    total_not_found = sum(book.not_found_books for book in annotated_queryset)

    # Apply status filter if present
    if status_filter == 'found':
        annotated_queryset = annotated_queryset.filter(found_books__gt=0)
    elif status_filter == 'not_found':
        annotated_queryset = annotated_queryset.filter(not_found_books__gt=0)

    # Pagination
    page_number = request.GET.get('page', 1)
    items_per_page = request.GET.get('show', 10)
    paginator = Paginator(annotated_queryset, items_per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        "bookData": page_obj,
        "page_range": paginator.page_range,
        "current_page": int(page_number) if page_number else 1,
        "total_pages": paginator.num_pages,
        "total_books": total_books,
        "found_books": total_found,
        "not_found_books": total_not_found,
        "search_query": search_query,
        "collection_filter": collection_filter,
        "decimal_start": decimal_start,
        "decimal_end": decimal_end,
        "year_start": year_start,
        "year_end": year_end,
        "status_filter": status_filter,
    }
    
    return render(request, "pages/book_collection_page.html", context)

@never_cache
@admin_required
def user_management_page(request):
    search_query = request.GET.get('search', '')
    show = request.GET.get('show', '10')
    
    users = User.objects.exclude(sys_acc_role=0).exclude(sys_status=1)
    if search_query:
        users = users.filter(
            Q(sys_firstname__icontains=search_query) |
            Q(sys_lastname__icontains=search_query)
        )

    paginator = Paginator(users, int(show))
    page = request.GET.get('page', 1)
    users = paginator.get_page(page)
    
    context = {
        'users': users,
    }
    return render(request, 'pages/user_management_page.html', context)

@never_cache
@admin_required
def delete_user_page(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.sys_status = 1
        user.save()

    return redirect("admin_manageuser")

@never_cache
@admin_required
def admin_settings(request):
    return render(request, "pages/settings_page.html")

@never_cache
@admin_required
def admin_edit_account(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # Case 1: Passwords do not match
        if password != password2:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'error': 'Passwords do not match.',
                    'messages': [{'message': m.message, 'tags': m.tags} for m in messages.get_messages(request)]
                })

        # Case 2: Both passwords are empty (no password update)
        elif password == "" and password2 == "":
            # Update user details without changing password
            user = User.objects.get(id=request.user.id)
            user.sys_firstname = firstname
            user.sys_lastname = lastname
            user.sys_username = username
            user.save()
        else:
            # Case 3: Update password and user details
            user = User.objects.get(id=request.user.id)
            user.sys_firstname = firstname
            user.sys_lastname = lastname
            user.sys_username = username
            user.set_password(password)
            user.save()

            userAuth = authenticate(request, username=username, password=password)
            if userAuth:
                login(request, userAuth)

            print(f"Updated Password Hash: {user.password}")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'messages': [{'message': m.message, 'tags': m.tags} for m in messages.get_messages(request)]
            })

        return redirect("admin_settings")

@never_cache
@admin_required
def admin_edit_profile_picture(request):
    if request.method == "POST":
        removeImage = request.POST.get('removeImage')
        user = User.objects.get(id=request.user.id)
        if removeImage == "remove":
            user.profile_picture = "profile_pictures/profile.png"
            user.save()
        else:
            if "profile_picture" in request.FILES:
                profilePicture = request.FILES["profile_picture"]
                print(profilePicture)
                user = User.objects.get(id=request.user.id)
                user.profile_picture = profilePicture
                user.save()

    return redirect("admin_settings")
