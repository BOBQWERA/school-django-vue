from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='forum_index'),
    path('<str:section>/',views.section,name = 'section'),
    path('<str:section>/send_posting/',views.save,name = 'save_posting'),
    path('<str:section>/write/',views.write,name='write_posting'),
    path('<str:section>/posting/<int:pid>/',views.posting,name = 'posting'),
    path('comment/<int:cid>/delete',views.del_comment,name = 'delete_comment'),
    path('comment/<int:cid>/report',views.rep_comment,name = 'report_comment'),
    path('comment/<int:cid>/pass',views.pass_comment,name='pass_comment'),
]