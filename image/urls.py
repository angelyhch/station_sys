from django.urls import  path
from . import views


app_name = 'image'
urlpatterns = [
    path('list_images/', views.list_images, name='list_images'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('del_image/', views.del_image, name='del_image'),

]