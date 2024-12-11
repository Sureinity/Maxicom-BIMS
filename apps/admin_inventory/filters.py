from django.db.models import Q

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
        queryset: Filtered queryset of books
    """
    # Apply collection filter if present
    if collection_filter:
        queryset = queryset.filter(col_code=collection_filter)
    
    # Apply Dewey Decimal filter if present
    if decimal_start and decimal_end:
        try:
            start_val = float(decimal_start)
            end_val = float(decimal_end)
            queryset = queryset.filter(
                decimal_part__gte=start_val,
                decimal_part__lte=end_val
            )
        except ValueError:
            pass

    # Apply Copyright Year filter if present
    if year_start and year_end:
        try:
            start_year = int(year_start)
            end_year = int(year_end)
            queryset = queryset.filter(
                copyrightdate__gte=str(start_year),
                copyrightdate__lte=str(end_year)
            )
        except ValueError:
            pass
    
    # Apply search filter if present
    if search_query:
        queryset = queryset.filter(
            Q(item_call_num__icontains=search_query) |
            Q(barcode__icontains=search_query) |
            Q(itype__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(publisher_code__icontains=search_query) |
            Q(isbn__icontains=search_query) |
            Q(subtitle__icontains=search_query)
        )
    
    return queryset
