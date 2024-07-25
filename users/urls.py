# Pip imports
from django.contrib.auth.views import auth_login, logout_then_login
from django.urls import path

# Internal imports
from users import views


urlpatterns = [
    path("login/", auth_login, name="login"),
    path("logout/", logout_then_login, {"login_url": "/"}, name="logout"),
    path("confirm/", views.confirm),
]
