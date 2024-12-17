from django.urls import path
from . import views

urlpatterns = [
    #User side: Barcode Input
    path("dashboard/", views.dashboard, name="dashboard"),
    path("scan/", views.barcode_scan, name="barcode_scan"),  #Scanner barcode URL 
    path("scan/process-barcode/", views.ajax_scanner_process_barcode, name="ajax_scanner_process_barcode"),
    path("scan/book-details/", views.scanner_process_barcode, name="scanner_process_barcode"),
    path("input/", views.barcode_input, name="barcode_input"), #Manual input barcode URL
    path("input/book-details/", views.input_process_barcode, name="input_process_barcode"),

    # Submit status
    path("input/book-details/submit/", views.submit_status, name="input_submit_status"),
    path("scan/book-details/submit/", views.submit_status, name="scanner_submit_status"),
]
