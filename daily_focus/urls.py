from django.urls import path
from daily_focus import views


app_name = 'daily_focus'
urlpatterns = [
    path('home/', views.home, name='home'),

]