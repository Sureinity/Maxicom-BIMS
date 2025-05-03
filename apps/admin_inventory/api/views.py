from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializer import BookQuerySerializer
from ..models import Booklist

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
        serializer = BookQuerySerializer(data, many=True)
        return Response(serializer.data)
