from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static

from weasyprint import HTML, CSS
from .models import Booklist

def pdf_bookDetails(request, id):
    book = Booklist.objects.get(id=id)
    return render(request, "print_pages/bookDetails_pdf.html", {"data": book})

# def listbook_print(request):
#     books = Booklist.objects.prefetch_related('inventories').all().iterator(chunk_size=1000)
#     um_logo_url = request.build_absolute_uri(static('admin_inventory/assets/um-logo.png'))

#     html_content = render_to_string(
#         "print_pages/list_of_acquisitions_pdf.html",
#         {"data": books, "um_logo_url": um_logo_url}
#     )

#     pdf = HTML(string=html_content).write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="output.pdf"'
#     return response

# def no_barcode_tag_print(request):
#     if request.method == "POST":
#         # No Barcode Tag
#         books = Booklist.objects.prefetch_related('inventories').filter(inventories__status=2).all()
#         um_logo_url = request.build_absolute_uri(static('admin_inventory/assets/um-logo.png'))

#         html_content = render_to_string(
#             "print_pages/no_barcode_tag_pdf.html",
#             {"data": books, "um_logo_url": um_logo_url}
#         )

#         pdf = HTML(string=html_content).write_pdf()

#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename="output.pdf"'
#         return response

# def for_repair_print(request):
#     if request.method == "POST":
#         # For Repair
#         books = Booklist.objects.prefetch_related('inventories').filter(inventories__status=3).all()
#         um_logo_url = request.build_absolute_uri(static('admin_inventory/assets/um-logo.png'))

#         html_content = render_to_string(
#             "print_pages/for_repair_pdf.html",
#             {"data": books, "um_logo_url": um_logo_url}
#         )

#         pdf = HTML(string=html_content).write_pdf()

#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename="output.pdf"'
#         return response

# def for_disposal_print(request):
#     if request.method == "POST":
#         # For Disposal
#         books = Booklist.objects.prefetch_related('inventories').filter(inventories__status=4).all()
#         um_logo_url = request.build_absolute_uri(static('admin_inventory/assets/um-logo.png'))

#         html_content = render_to_string(
#             "print_pages/for_disposal_pdf.html",
#             {"data": books, "um_logo_url": um_logo_url}
#         )

#         pdf = HTML(string=html_content).write_pdf()

#         response = HttpResponse(pdf, content_type='application/pdf')
#         response['Content-Disposition'] = 'inline; filename="output.pdf"'
#         return response