from django.shortcuts import redirect, render

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        # If user is not authenticated, redirect to login
        if not request.user.is_authenticated:
            return redirect('login')
        # If user is authenticated but not admin, redirect to dashboard
        if request.user.sys_acc_role != 0:
            return render(request, 'http_errors/401.html', status=401)
        # If user is admin, allow access to the view
        return view_func(request, *args, **kwargs)
    return wrapper
