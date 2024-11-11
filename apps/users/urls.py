from django.urls import path
from . import views

urlpatterns = [
    #User Authentication
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    
    #User side: Barcode Input
    path("dashboard/", views.dashboard, name="dashboard"),
    path("scan/", views.barcode_scan, name="barcode_scan"),  #Scanner barcode URL 
    path("scan/process-barcode/", views.scanner_process_barcode, name="scanner_process_barcode"),
    path("input/", views.barcode_input, name="barcode_input"), #Manual input barcode URL
    path("input/process-barcode/", views.input_process_barcode, name="process_barcode"),
]
