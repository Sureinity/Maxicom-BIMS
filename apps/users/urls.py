from django.urls import path
from . import views

urlpatterns = [
    #User Authentication
    path("login/", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("dashboard/", views.dashboard, name="dashboard"),
    
    #User side: Barcode Input
    path("scan/", views.barcode_scan, name="barcode_scan"),
    path("scan/process-barcode/", views.process_barcode, name="process_barcode"),
    path("scan/input/", views.barcode_input, name="barcode_input"),

]
