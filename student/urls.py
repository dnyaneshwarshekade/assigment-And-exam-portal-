from django.urls import path
from . import views

urlpatterns = [
    path('',views.studIndex,name='stud_home'),
    path('assignment/<str:slug>',views.assignment,name='assignment'),
    path('mcq_result/<str:slug>',views.mcqResult,name="mcq_result"),
    path('file_upload/<str:slug>',views.fileSubmit,name="file_upload"),
    path('update_data',views.updateData,name='update_data'),
  ]