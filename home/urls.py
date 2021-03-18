from django.urls import path
from . import views
urlpatterns = [
  path('',views.index,name='index'),
  path('stud_register',views.studRegister,name='stud_register'),
  path('teacher_register',views.teacherRegister,name='teacher_register'),
  path('stud_login',views.studLogin,name='stud_login'),
  path('teacher_login',views.teacherLogin,name='teacher_login'),
  path('logout',views.userLogout,name='logout'),
  
]
