from django.shortcuts import render

# Create your views here.
def admin_page(request):    # This view is for rendering the main container of admin dasboard page.
    return render(request, "admin_main.html")

def dashboard_page(request):
    return render (request, "pages/dashboard_page.html")

def listbooks_page(request):
    return render (request, "pages/listbooks_page.html")

def inventory_page(request):
    return render (request, "pages/inventory_page.html")

def usersettings_page(request):
    return render (request, "pages/usersettings_page.html")


# Hamburger pages
def goodcon_page(request):
    return render (request, "pages/goodcon_page.html")

def nobarcode_page(request):
    return render (request, "pages/nobarcode_page.html")

def forrepair_page(request):
    return render (request, "pages/forrepair_page.html")

def fordisposal_page(request):
    return render (request, "pages/fordisposal_page.html")



