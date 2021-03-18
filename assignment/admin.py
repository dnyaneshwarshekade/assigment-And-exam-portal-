from django.contrib import admin
from .models import Assignment,MCQ,FileUpload
# Register your models here.

class AssignmentAdmin(admin.ModelAdmin):
  list_filters = ['ass_class']
  list_display = [
    'pk',
    'date',
    'subject',
    'teacher_name',
    'ass_type',
  ]
  def teacher_name(self,obj):
      return obj.teacher.first_name +' '+obj.teacher.last_name


admin.site.register(Assignment,AssignmentAdmin)
admin.site.register(MCQ)
admin.site.register(FileUpload)

