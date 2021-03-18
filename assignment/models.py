from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from home.models import Class,Subject

# Create your models here.

class Assignment(models.Model):
  date = models.DateTimeField(default=timezone.now)
  teacher = models.ForeignKey(User,on_delete=models.CASCADE)
  ass_class = models.ForeignKey(Class,on_delete=models.CASCADE,null=True)
  subject = models.ForeignKey(Subject,on_delete=models.CASCADE,null=True)
  last_date = models.DateField(null=True)
  ass_type = models.CharField(max_length=30)
  slug = models.CharField(max_length=80,null=True)
  
  def __str__(self):
    return str(self.pk)
    
class MCQ(models.Model):
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  que = models.TextField(max_length=3000)
  opt1 = models.CharField(max_length=30)
  opt2 = models.CharField(max_length=30)
  opt3 = models.CharField(max_length=30)
  opt4 = models.CharField(max_length=30)
  ans = models.CharField(max_length=30)
  def __str__(self):
    return str(self.pk)
    
    
class FileUpload(models.Model):
  assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE)
  desc = models.TextField(max_length=3000)
  def __str__(self):
    return str(self.pk)
    


