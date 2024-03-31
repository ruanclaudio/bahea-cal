from django.contrib.auth.views import auth_login, auth_logout, logout_then_login
from django.urls import path

from users import views

urlpatterns = [
    path("login/", auth_login, name="login"),
    path("logout/", logout_then_login, {"login_url": "/"}, name="logout"),
    path("confirm/", views.confirm),
]
