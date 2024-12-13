from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static

from weasyprint import HTML, CSS
from .models import Booklist

def listbook_print(request):
    books = Booklist.objects.prefetch_related('inventories').all()[:10].iterator(chunk_size=1000)
    
    um_logo_url = request.build_absolute_uri(static('admin_inventory/assets/um-logo.png'))
    bims_logo_url = request.build_absolute_uri(static('admin_inventory/assets/logo-bims.png'))

    html_content = render_to_string(
        "print_pages/list_of_acquisitions_pdf.html",
        {"data": books, "um_logo_url": um_logo_url, "bims_logo_url": bims_logo_url}
    )

    css_url = static('admin_inventory/styles.css')
    css_absolute_path = request.build_absolute_uri(css_url)

    pdf = HTML(string=html_content).write_pdf(stylesheets=[CSS(css_absolute_path)])

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    return response

def bookDetails_print(request, id):
    book = Booklist.objects.get(id=id)
    return render(request, "print_pages/bookDetails_pdf.html", {"data": book})
