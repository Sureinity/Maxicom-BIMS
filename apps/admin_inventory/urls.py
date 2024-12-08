from django.urls import path
from . import views, export

urlpatterns = [
    # Admin menus
    path("dashboard/", views.dashboard_page, name="admin_dashboard"),
    path("list-books/", views.listbooks_page, name="admin_listbooks"),
    path("inventory/", views.inventory_page, name="admin_inventory"),
    path("book-collections/", views.bookcollections_page, name="admin_collections"),
    path("user-settings/", views.usersettings_page, name="admin_usersettings"),
    
    # listbooks_page CRUD
    path("list-books/create", views.create_listbooks_page, name="create_listbooks"),
    path("list-books/<int:id>/update", views.update_listbooks_page, name="update_listbooks"),
    path("list-books/<int:id>/delete", views.delete_listbooks_page, name="delete_listbooks"),

    # Exportation (TEST)
    path("export/", export.export_books_to_excel, name="admin_exportbooks"),
]
