from .models import Booklist, Inventory, InventoryHistory
from django.shortcuts import render
from .models import Booklist, Inventory

# Testing...
def listbook_print(request):
    books = Booklist.objects.all()[:5000].iterator(chunk_size=1000)
    return render(request, "print_pages/listbooks_pdf.html", {"data": books})

def bookDetails_print(request, id):
    book = Booklist.objects.get(id=id)
    return render(request, "print_pages/bookDetails_pdf.html", {"data": book})
