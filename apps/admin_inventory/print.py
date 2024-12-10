from .models import Booklist, Inventory, InventoryHistory
from django.shortcuts import render

def listbook_print(request):
    return render(request, "print_pages/listbooks_pdf.html")
