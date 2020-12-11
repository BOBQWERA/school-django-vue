from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='tools_index'),
    path('upload/',views.upload,name = 'upload'),
    path('download/<str:urlname>/',views.download,name='download'),
    path('md5/',views.md5,name='md5'),
    path('base64/',views.base64,name='base64'),
]