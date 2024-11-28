from django.shortcuts import redirect, render

def redirect_dashboard_if_loggedin(func):
    def wrapper(request):
        if not request.user.is_authenticated:
            return redirect("login")
        return func(request)
    return wrapper

def redirect_login_if_not_loggedin(func):
    def wrapper(request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return func(request)
    return wrapper

def admin_is_not_authorized(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.sys_acc_role == 0:  # 0 is ADMIN role
            return render(request, 'http_errors/401.html', status=401)
        return func(request, *args, **kwargs)
    return wrapper
