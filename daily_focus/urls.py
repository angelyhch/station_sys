from django.urls import path
from daily_focus import views


app_name = 'daily_focus'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('upload_focus/', views.upload_focus, name='upload_focus'),
    # path('focus_history/',views.focus_history, name='focus_history'),

]