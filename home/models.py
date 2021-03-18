from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Class(models.Model):
  class_name = models.CharField(max_length=50)
  strength = models.IntegerField()
  def __str__(self):
    return str(self.class_name)

class Subject(models.Model):
  class_name = models.ForeignKey(Class,on_delete=models.CASCADE)
  subject_name = models.CharField(max_length=50)
  def __str__(self):
    return self.subject_name
class Student(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  s_roll = models.IntegerField()
  s_class = models.ForeignKey(Class,on_delete=models.CASCADE,null=True,blank=True)
  s_dob = models.DateField(null=True,blank=True)
  s_contact = models.IntegerField(null=True,blank=True)
  s_gender = models.CharField(max_length=50,null=True,blank=True)
  updated = models.BooleanField(null=True,default=True)
  def __str__(self):
    return str(self.pk)
    
class Teacher(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  t_dob = models.DateField(null=True,blank=True)
  t_contact = models.IntegerField(null=True)
  t_gender = models.CharField(max_length=50,null=True)
  updated = models.BooleanField(null=True,default=True)
  def __str__(self):
    return str(self.pk)

