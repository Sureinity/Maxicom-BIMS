from django.urls import path
from . import views

urlpatterns = [
    #User Authentication
    path("", views.user_login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
]
