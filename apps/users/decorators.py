from django.shortcuts import redirect, render

def redirect_dashboard_if_loggedin(func):
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect("login")
        return func(request)
    return wrapper
