from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('exit/', views.exit, name='exit'),
    # path('add_friend/<str:username>',views.friend,name='add_friend'),
    path('<str:username>/sign', views.sign, name='sign'),
    path('<str:username>/add/<str:friend>', views.add_friend, name='add'),
    path('<str:username>/refuse/<str:friend>', views.refuse, name='refuse'),
    path('<str:username>/', views.userspace, name='userspace'),
]
