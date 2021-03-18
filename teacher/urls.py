from django.urls import path
from . import views

urlpatterns = [
    path('',views.teacherIndex,name='teacher_home'),
    path('add_assignment',views.addAssignment,name='add_assignment'),
    path('assignment/<str:slug>',views.assignment,name='assignment'),
    path('assignment_status/<str:slug>',views.assignmentStatus,name='assignment_status'),
    path('update_data',views.updateData,name='update_data'),
    # API urls
    path('delete_assignment/<str:slug>',views.deleteAssignment,name='delete_assignment'),
    path('delete_quetion/<int:id>',views.deleteQuetion,name='delete_quetion'),
    path('delete_file_question/<int:id>',views.deleteFileQuestion,name='delete_file_question'),
    path('update_due_date/<int:id>',views.updateDueDate,name='update_due_date'),
  ]
