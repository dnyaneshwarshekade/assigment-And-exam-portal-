from django.contrib import admin
from .models import MCQResult,AttempQuestion,File,NotificationForStudent
# Register your models here.

class AttempQuestionAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "control_no",
        "s_ans",
        "answer",
    ]
    def name(self,obj):
        return obj.student.first_name+' '+obj.student.last_name
    def control_no(self,obj):
        return obj.student.username
    def answer(self,obj):
        return obj.mcq.ans
admin.site.register(MCQResult)
admin.site.register(File)
admin.site.register(AttempQuestion,AttempQuestionAdmin)
admin.site.register(NotificationForStudent)