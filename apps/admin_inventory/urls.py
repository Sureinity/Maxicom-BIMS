from django.urls import path
from . import views, export, print

urlpatterns = [
    # Admin menus
    path("dashboard/", views.dashboard_page, name="admin_dashboard"),
    path("list-books/", views.listbooks_page, name="admin_listbooks"),
    path("inventory/", views.inventory_page, name="admin_inventory"),
    path("book-collections/", views.bookcollections_page, name="admin_collections"),
    path("user-settings/", views.user_management_page, name="admin_usersettings"),
    
    # listbooks_page CRUD
    path("list-books/create", views.create_listbooks_page, name="create_listbooks"),
    path("list-books/<int:id>/update", views.update_listbooks_page, name="update_listbooks"),
    path("list-books/<int:id>/delete", views.delete_listbooks_page, name="delete_listbooks"),

    # usersettings_page CRUD
    path("user-settings/<int:id>/delete", views.delete_usersettings_page, name="delete_usersettings"),

    # Exportation (TEST)
    path("export/", export.export_books_to_excel, name="admin_exportbooks"),

    # Print (TEST)
    path("print/", print.listbook_print, name="print_listbooks"),
    path("print/<int:id>", print.bookDetails_print, name="print_bookDetails"),
]
