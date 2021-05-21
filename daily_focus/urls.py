from django.urls import path
from daily_focus import views


app_name = 'daily_focus'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('upload_focus/', views.upload_focus, name='upload_focus'),
    path('focus_list/', views.focus_list, name='focus_list'),
    path('focus_detail/<focus_id>/', views.focus_detail, name='focus_detail'),
    path('focus_record/<focus_id>/', views.focus_record, name='focus_record'),
    path('focus_today/', views.focus_today, name='focus_today'),
    path('delete_focus_image/', views.delete_focus_image, name='delete_focus_image'),
    path('delete_focus_after_image/', views.delete_focus_after_image, name='delete_focus_after_image'),
    path('record_add_focus/', views.record_add_focus, name='record_add_focus'),
    path('upload_image/', views.upload_image, name='upload_image'),

]