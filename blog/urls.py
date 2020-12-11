from django.urls import path

from . import views
urlpatterns = [
    path('',views.index,name = 'blog'),
    path('write/',views.write,name = 'write_blog'),
    path('send_article/',views.save,name = 'save_article'),
    path('all/',views.all_blog,name='all_blog'),
    path('article/<int:aid>/',views.article,name = 'article'),
    path('article/<int:aid>/success',views.success,name='pass_blog'),
    path('article/<int:aid>/like',views.like,name='like_blog'),
    path('article/<int:aid>/report',views.report,name='report_blog'),
    path('article/<int:aid>/delete',views.delete,name='delete_blog'),
]