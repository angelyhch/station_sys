from django.urls import path
from . import views


app_name = 'craft'

urlpatterns = [
    path('daily_foucs', views.daily_foucs, name='daily_foucs'),
    path('foucs_add/', views.foucs_add, name='foucs_add'),
    path('part_info/<str:lingjianhao>/', views.part_info, name='part_info'),
    path('table_display_insert/', views.table_display_insert, name='table_display_insert'),
    path('table_display_edit/', views.table_display_edit, name='table_display_edit'),
    path('table_display_user/<str:table_name>/', views.table_display_user, name='table_display_user'),
    path('station_info/<str:station>', views.station_info, name='station_info'),
    path('stations/', views.stations, name='stations'),
    path('table_display/<str:table_name>/', views.table_display, name='table_display'),

    path('home/', views.home, name='home'),
]