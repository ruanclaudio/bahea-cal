# Pip imports
from django.urls import path

# Internal imports
from api import views


urlpatterns = [
    path("v1/calendar/init/", views.calendar_init_view, name="calendar_init"),
    path("v1/calendar/token/", views.calendar_token, name="calendar_token"),
    path("v1/user/return/", views.user_json_return, name="test_user_return"),
    path("v1/user/info/", views.user_info_view, name="user_info"),
    path("v1/check/loggedin/", views.check_user_is_loggedin, name="check_user_loggedin"),
]
