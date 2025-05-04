from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializer import BookQuerySerializer,  BookFoundAndNotFoundSerializer
from ..models import Booklist, Inventory

@api_view(['GET'])
def book_query(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '').strip()
        if not search_query:
            return Response([], status=status.HTTP_200_OK)

        data = Booklist.objects.values("title","author","subtitle","publisher_code","itype","isbn").filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(subtitle__icontains=search_query) |
            Q(publisher_code__icontains=search_query) |
            Q(itype__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
        print(data)
        serializer = BookQuerySerializer(data, many=True)
        return Response(serializer.data)


INVENTORY_STATUS = [
    Inventory.GOOD_CONDITION,
    Inventory.NO_BARCODE_TAG,
    Inventory.FOR_REPAIR,
    Inventory.FOR_DISPOSAL,
    Inventory.NOT_FOUND,
]

@api_view(['GET'])
def book_not_found(request):
    data = Inventory.objects.all().filter(status=Inventory.NOT_FOUND)
    serializer = BookFoundAndNotFoundSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def book_found(request):
    data = Inventory.objects.all().filter(status__in=INVENTORY_STATUS)
    serializer = BookFoundAndNotFoundSerializer(data, many=True)
    return Response(serializer.data)
