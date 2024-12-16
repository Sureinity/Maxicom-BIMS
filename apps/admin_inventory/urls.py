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

    # Edit Admin Account
    path("settings/edit-account", views.admin_edit_account, name="admin_edit_account"),
    path("settings/edit-profile-picture", views.admin_edit_profile_picture, name="admin_edit_profile_picture"),

    # listbooks_page CRUD
    path("list-books/create", views.create_listbooks_page, name="create_listbooks"),
    path("list-books/<int:id>/update", views.update_listbooks_page, name="update_listbooks"),
    path("list-books/<int:id>/delete", views.delete_listbooks_page, name="delete_listbooks"),

    # usersettings_page CRUD
    path("user-settings/<int:id>/delete", views.delete_user_page, name="admin_delete_user"),

    # Exportation
    path("export/list-of-acquisitions", export.export_listOfAcquisitions, name="export_list_of_acquisitions"),
    path("export/no-barcode-tag", export.export_noBarcodeTag, name="export_no_barcode_tag"),
    path("export/for-repair", export.export_forRepair, name="export_for_repair"),
    path("export/for-disposal", export.export_forDisposal, name="export_for_disposal"),
    path("export/not-found", export.export_notFound, name="export_not_found"),

    # Generate PDF report
    path("pdf/<int:id>", print.pdf_bookDetails, name="pdf_bookDetails"), # For Book Details
]
