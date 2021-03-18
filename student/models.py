from django.db import models
from django.contrib.auth.models import User
from assignment.models import Assignment,MCQ
from home.models import Class
from django.utils import timezone
# Create your models here.

class MCQResult(models.Model):
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  student = models.ForeignKey(User,on_delete=models.CASCADE)
  total_que = models.IntegerField()
  attemp = models.IntegerField()
  correct = models.IntegerField()
  marks = models.IntegerField()
  def __str__(self):
    return str(self.pk)
 
class AttempQuestion(models.Model):
  student = models.ForeignKey(User,on_delete=models.CASCADE)
  #assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  mcq = models.ForeignKey(MCQ,on_delete=models.CASCADE)
  s_ans = models.CharField(max_length=30)
  def __str__(self):
    return str(self.pk)

class File(models.Model):
  student = models.ForeignKey(User,on_delete=models.CASCADE)
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  question = models.TextField(max_length=300,null=True)
  def student_name(obj, filename):
    return str("assignments/"+obj.assignment.subject.subject_name+"/"+obj.student.username+"/"+filename)
  file = models.FileField(upload_to=student_name,null=True)

class NotificationForStudent(models.Model):
  date_filled = models.DateTimeField(default=timezone.now)
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  notify_class = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
  def __str__(self):
    return str(self.pk)