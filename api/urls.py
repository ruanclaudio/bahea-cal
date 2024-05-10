from django.urls import path
from api import views

urlpatterns = [
    path('v1/calendar/init/', views.calendar_init_view, name='calendar_init'),
    path('v1/calendar/flow/', views.calendar_flow_view, name='calendar_flow'),
]