from django.urls import path
from . import views, export, print

urlpatterns = [
    # Admin menus
    path("dashboard/", views.dashboard_page, name="admin_dashboard"),
    path("list-books/", views.listbooks_page, name="admin_listbooks"),
    path("inventory/", views.inventory_page, name="admin_inventory"),
    path("book-collections/", views.bookcollections_page, name="admin_collections"),
    path("manage-user/", views.user_management_page, name="admin_manageuser"),
    path("settings/", views.admin_settings, name="admin_settings"),


    
    # listbooks_page CRUD
    path("list-books/create", views.create_listbooks_page, name="create_listbooks"),
    path("list-books/<int:id>/update", views.update_listbooks_page, name="update_listbooks"),
    path("list-books/<int:id>/delete", views.delete_listbooks_page, name="delete_listbooks"),

    # usersettings_page CRUD
    path("user-settings/<int:id>/delete", views.delete_user_page, name="admin_delete_user"),

    # Exportation
    path("export/", export.export_books_to_excel, name="admin_exportbooks"),

    # Generate PDF report
    path("print/", print.listbook_print, name="print_listbooks"),
    path("print/no-barcode-tag", print.no_barcode_tag_print, name="no_barcode_tag_print"),
    path("print/for-repair", print.for_repair_print, name="for_repair_print"),
    path("print/for-disposal", print.for_disposal_print, name="for_disposal_print"),
    path("print/<int:id>", print.bookDetails_print, name="print_bookDetails"), # For Book Details
]
