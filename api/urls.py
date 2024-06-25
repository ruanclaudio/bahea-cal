from django.urls import path
from api import views

urlpatterns = [
    path('v1/calendar/init/', views.calendar_init_view, name='calendar_init'),
    path('v1/calendar/token/', views.calendar_token, name='calendar_token'),
    path('v1/user/return', views.user_json_return, name='test_user_return'),
]