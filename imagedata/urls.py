from django.urls import path

from . import views

urlpatterns = [
    path('image/<str:imgname>',views.get_image,name = 'get_image'),
    path('<str:filename>',views.get_file,name = 'get_file'),
]