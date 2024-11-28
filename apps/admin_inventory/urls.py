from django.urls import path
from . import views

urlpatterns = [
    # Admin menus
    path("", views.admin_page, name="admin_main"),
    path("dashboard/", views.dashboard_page, name="admin_dashboard"),
    path("list-books/", views.listbooks_page, name="admin_listbooks"),
    path("inventory/", views.inventory_page, name="admin_inventory"),
    path("user-settings/", views.usersettings_page, name="admin_usersettings"),


    # Inventory Hamburger
    path("inventory-goodcon/", views.goodcon_page, name="admin_inventory_goodcon"),
    path("inventory-nobarcode/", views.nobarcode_page, name="admin_inventory_nobarcode"),
    path("inventory-forrepair/", views.forrepair_page, name="admin_inventory_forrepair"),
    path("inventory-fordisposal/", views.fordisposal_page, name="admin_inventory_fordisposal"),


]
