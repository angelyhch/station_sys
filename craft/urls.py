from django.urls import path
from . import views


app_name = 'craft'

urlpatterns = [
    path('', views.home, name='home'),
    path('temp1/', views.temp1, name='temp1'),
    path('temp2/', views.temp2, name='temp2'),
    path('temp3/', views.temp3, name='temp3'),

]