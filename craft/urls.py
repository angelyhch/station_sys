from django.urls import path
from . import views


app_name = 'craft'

urlpatterns = [
    path('temp1/', views.temp1, name='temp1'),
    path('temp2/', views.temp2, name='temp2'),
    path('temp3/', views.temp3, name='temp3'),
    path('station_info/<str:station>', views.station_info, name='station_info'),
    path('stations/', views.stations, name='stations'),
    path('table_display/<str:table_name>/', views.table_display, name='table_display'),

    path('<parameter>/', views.home, name='home'),
]