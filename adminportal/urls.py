from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminIndex,name='adminportal'),
    path('admin_login',views.adminLogin,name='admin_login'),
    path('save_student/<int:id>',views.saveStudent,name='save_student'),
    path('save_teacher/<int:id>',views.saveTeacher,name='save_teacher'),
    path('save_class/<int:id>',views.saveClass,name='save_class'),
    path('save_subject/<int:id>',views.saveSubject,name='save_subject'),
    # APIs
    path('admin_logout',views.adminLogout,name='admin_logout'),
    path('delete_student/<int:id>',views.deleteStudent,name='delete_student'),
    path('delete_teacher/<int:id>',views.deleteTeacher,name='delete_teacher'),
    path('delete_class/<int:id>',views.deleteClass,name='delete_class'),
    path('delete_subject/<int:id>',views.deleteSubject,name='delete_subject'),
    path('add_student',views.addStudent,name='add_student'),
    path('add_teacher',views.addTeacher,name='add_teacher'),
    path('add_class',views.addClass,name='add_class'),
    path('add_subject',views.addSubject,name='add_subject'),

  ]