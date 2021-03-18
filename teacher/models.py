from django.db import models
from django.contrib.auth.models import User
from assignment.models import Assignment
from student.models import MCQResult
from home.models import Teacher
from django.utils import timezone

# Create your models here.
class AssignmentsLog(models.Model):
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  student = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  submit_on = models.DateTimeField(default=timezone.now)
  result = models.ForeignKey(MCQResult,on_delete=models.CASCADE,null=True,blank=True)
  def __str__(self):
    return str(self.pk)


class NotifiacationsForTeacher(models.Model):
  date_filled = models.DateTimeField(default=timezone.now)
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  student = models.ForeignKey(User,on_delete=models.CASCADE)
  teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True,blank=True)
  def __str__(self):
    return str(self.pk)
