from home.models import Student,Teacher
from assignment.models import Assignment
from teacher.models import NotifiacationsForTeacher
from student.models import NotificationForStudent
from home.templatetags import extras

def notifications(request):
    if request.user.is_authenticated:
        if extras.has_group(request.user,'Student'):
            student = Student.objects.get(user=request.user)
            notifications = NotificationForStudent.objects.filter(notify_class=student.s_class).order_by("-date_filled")
            params = {
                'notifications' : notifications,
            }
        elif extras.has_group(request.user,'Teacher'):
            teacher = Teacher.objects.get(user=request.user)
            notifications = NotifiacationsForTeacher.objects.filter(teacher=teacher).order_by("-date_filled")
            params = {"notifications" : notifications}
        else:
            params = {}
    else:
        params = {}
    return params