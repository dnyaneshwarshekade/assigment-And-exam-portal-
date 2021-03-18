from django.contrib import admin
from .models import Teacher,Student,Class,Subject
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
  list_filter = [
      's_class'
    ]
  list_display = [
      'pk',
      'name',
      'control_number',
      's_class',
      's_roll',
      'email',
      's_contact',
    ]
  def name(self,obj):
    return obj.user.first_name+' '+obj.user.last_name
  def control_number(self,obj):
    return obj.user.username
  def email(self,obj):
    return obj.user.email
    
class TeacherAdmim(admin.ModelAdmin):
  list_display = [
      'pk',
      'name',
      'control_number',
      'email',
      't_contact'
    ]
  
  def name(self,obj):
    return obj.user.first_name+' '+obj.user.last_name
  def control_number(self,obj):
    return obj.user.username
  def email(self,obj):
    return obj.user.email

class ClassAdmin(admin.ModelAdmin):
  list_display = [
    "pk",
    "class_name",
    "strength",
  ]

class SubjectAdmin(admin.ModelAdmin):
  list_display = [
    "pk",
    "subject_name",
    "class_name"
  ]
  list_filter = [
    "class_name"
  ]

admin.site.register(Student,StudentAdmin)
admin.site.register(Teacher,TeacherAdmim)
admin.site.register(Class,ClassAdmin)
admin.site.register(Subject,SubjectAdmin)

