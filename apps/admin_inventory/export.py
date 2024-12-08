import openpyxl
from django.http import HttpResponse
from apps.admin_inventory.models import Booklist, Inventory

def export_books_to_excel(request):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Report"

    headers = [
        "itemcallnumber", "ccode", "itype", "title", "subtitle", 
        "author", "copyrightdate", "publishercode", "barcode", 
        "isbn", "dateaccessioned", "copynumber", "volume", 
        "editionstatement", "paidfor", "price", "booksellerid",
        "bookstate"
    ]
    sheet.append(headers)

    books = Booklist.objects.all()
    book_status = Inventory.objects.select_related("book").all()
    for book in books:
        sheet.append([
            book.item_call_num,   # itemcallnumber
            book.col_code,        # ccode
            book.itype,           # itype
            book.title,           # title
            book.subtitle,        # subtitle
            book.author,          # author
            book.copyrightdate,   # copyrightdate
            book.publisher_code,  # publishercode
            book.barcode,         # barcode
            book.isbn,            # isbn
            book.date_accessioned, # dateaccessioned
            book.copy_num,        # copynumber
            book.volume,          # volume
            book.edition_stmt,    # editionstatement
            book.paidfor,         # paidfor
            book.price,           # price
            book.bookseller_id,    # booksellerid
          #  status.status,        # book status
        ])

    # Response headers for downloading the file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = "attachment; filename=report.xlsx"

    workbook.save(response)
    return response

