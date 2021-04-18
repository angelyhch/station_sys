from django.urls import path
from . import views


app_name = 'craft'

urlpatterns = [
    path('table_display_edit/', views.table_display_edit, name='table_display_edit'),
    path('station_info/<str:station>', views.station_info, name='station_info'),
    path('stations/', views.stations, name='stations'),
    path('table_display/<str:table_name>/', views.table_display, name='table_display'),

    path('home/', views.home, name='home'),
]