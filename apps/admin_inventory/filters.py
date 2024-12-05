from django.db.models import Q

def extract_decimal(call_num):
    """Helper function to extract decimal number from call number"""
    try:
        parts = call_num.split()
        if len(parts) >= 2:
            return float(parts[1])
        return None
    except (ValueError, IndexError):
        return None

def apply_book_filters(queryset, search_query='', collection_filter='', decimal_start='', 
                      decimal_end='', year_start='', year_end=''):
    """
    Apply filters to a Booklist queryset
    
    Args:
        queryset: Initial queryset to filter
        search_query (str): Search term to filter across multiple fields
        collection_filter (str): Collection code to filter by
        decimal_start (str): Starting Dewey decimal number
        decimal_end (str): Ending Dewey decimal number
        year_start (str): Starting copyright year
        year_end (str): Ending copyright year
    
    Returns:
        list: Filtered list of books
    """
    bookData = queryset
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
            if using_filtered_list:
                bookData = [
                    book for book in bookData
                    if book.copyrightdate and start_year <= int(book.copyrightdate) <= end_year
                ]
            else:
                bookData = bookData.filter(
                    copyrightdate__gte=str(start_year),
                    copyrightdate__lte=str(end_year)
                )
                using_filtered_list = True
        except ValueError:
            pass
    
    # Apply search filter if present
    if search_query:
        if using_filtered_list:
            bookData = [
                book for book in bookData
                if any(search_query.lower() in str(getattr(book, field)).lower() 
                    for field in ['item_call_num', 'barcode', 'title', 'author', 
                                'publisher_code', 'isbn', 'subtitle'])
            ]
        else:
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
        
    return bookData
