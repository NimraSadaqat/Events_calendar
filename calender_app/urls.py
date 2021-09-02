from django.urls import path
from . import views

app_name = 'calendar_app'

urlpatterns = [
    # path('', views.index, name='main-view'),
    path('', views.CalendarView.as_view(), name='calendars'),
    path('week/', views.WeekView.as_view(), name='weekcalendars'),
    path('agenda/', views.AgendaListView.as_view(), name='agenda'),
]
