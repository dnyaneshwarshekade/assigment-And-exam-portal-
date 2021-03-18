from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from .templatetags import extras
from django.contrib import messages
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Student,Teacher,Class
from django.db import IntegrityError
import sys

# Check Exceptions
class PasswordNotMatch(Exception):
  pass

class EmptyControlNumber(Exception):
  pass

class WeakPassword(Exception):
  pass

class EmptyPassword(Exception):
  pass

# Create your views here.
def index(request):
  
  return render(request,'home/index.html')
  
  
def studRegister(request):
  """docstring for studRegister"""
  group = Group.objects.get(name='Student')
  if request.method == 'POST':
    try:
      fname = request.POST['fname']
      lname = request.POST['lname']
      control = request.POST['control']
      email = request.POST['email']
      cont = request.POST['cont']
      dob = request.POST['dob']
      gender = request.POST['gender']
      s_class = request.POST['class']
      roll = request.POST['roll']
      password = request.POST['password']
      con_password = request.POST['con_password']
      if password != con_password:
        raise PasswordNotMatch
      if len(control.replace(" ",""))==0:
        raise EmptyControlNumber
      if len(password)<=6:
        raise WeakPassword
      if len(password.replace(" ",""))<=6:
        raise EmptyPassword
      user_created = False
      
      stud_class = Class.objects.get(class_name=s_class)
      user = User.objects.create_user(control,email,password,first_name=fname,last_name=lname)
      user_created = True
      user.groups.add(group)
      student = Student.objects.create(
        user = user,
        s_roll = roll,
        s_class = stud_class,
        s_dob = dob,
        s_contact = cont,
        s_gender = gender,
        )
    except PasswordNotMatch:
      messages.error(request,'password and confirm password not match')
      
    except EmptyControlNumber:
      messages.error(request,'Control number is Empty')
      
    except WeakPassword:
      messages.error(request,'Password must be greater than 6 characters')
    
    except EmptyPassword:
      messages.error(request,'Password is empty')
    except IntegrityError:
      messages.error(request,'Control number already exists')
    except:
      if user_created:
        user.delete()
      messages.error(request,sys.exc_info()[0])
      
      
    else:
      messages.success(request,'Registration Successfull')
  classes = Class.objects.all()
  params = {
    "classes" : classes,
  }
  return render(request,'home/stud_register.html',params)
  
def teacherRegister(request):
  group = Group.objects.get(name='Teacher')
  if request.method == 'POST':
    try:
      fname = request.POST['fname']
      lname = request.POST['lname']
      control = request.POST['control']
      email = request.POST['email']
      cont = request.POST['cont']
      dob = request.POST['dob']
      gender = request.POST['gender']
      password = request.POST['password']
      con_password = request.POST['con_password']
      if password != con_password:
        raise PasswordNotMatch
      if len(control.replace(" ",""))==0:
        raise EmptyControlNumber
      if len(password)<=6:
        raise WeakPassword
      if len(password.replace(" ",""))<=6:
        raise EmptyPassword
      user_created = False
      user = User.objects.create_user(control,email,password,first_name=fname,last_name=lname)
      user_created = True
      user.groups.add(group)
      group.user_set.add(user)
      teacher = Teacher.objects.create(
        user = user,
        t_dob = dob,
        t_contact = cont,
        t_gender = gender,
        )
    except PasswordNotMatch:
      messages.error(request,'password and confirm password not match')
      
    except EmptyControlNumber:
      messages.error(request,'Control number is Empty')
      
    except WeakPassword:
      messages.error(request,'Password must be greater than 6 characters')
    
    except EmptyPassword:
      messages.error(request,'Password is empty')
    
    except IntegrityError:
      messages.error(request,'Control number already exists')
    
    except:
      if user_created:
        user.delete()
      print(sys.exc_info()[0])
      messages.error(request,sys.exc_info()[0])
    else:
      messages.success(request,'Registration Successfull')
  return render(request,'home/teacher_register.html')
  
  
def studLogin(request):
  if request.user.is_authenticated:
    return redirect('/')
  if request.method == "POST":
    # try:
      control = request.POST['control']
      password = request.POST['password']
      user = authenticate(username=control,password=password)
      if user is not None and extras.has_group(user,'Student'):
        login(request,user)
        messages.success(request,'Welcome '+user.first_name+' '+user.last_name)
        return redirect('student/')
        messages.success(request,'Welcome '+user.first_name+' '+user.last_name)
      else:
        messages.error(request,'Invalid Credentials')
  return render(request,'home/stud_login.html')

def teacherLogin(request):
  if request.user.is_authenticated:
    return redirect('/')
  if request.method == "POST":
    # try:
      control = request.POST['control']
      password = request.POST['password']
      user = authenticate(username=control,password=password)
      if user is not None and extras.has_group(user,'Teacher'):
        login(request,user)
        return redirect('teacher/')
        messages.success(request,'Welcome '+user.first_name+' '+user.last_name)
      else:
        messages.error(request,'Invalid Credentials')
  return render(request,'home/teacher_login.html')

# APIs
def userLogout(request):
  logout(request)
  return redirect('/')

# signals(Triggers)
@receiver(post_delete,sender=Student)
def deleteStudentUser(sender,instance,*args, **kwargs):
  user = User.objects.get(username=instance.user.username).delete()

@receiver(post_delete,sender=Teacher)
def deleteTeacherUser(sender,instance,*args,**kwargs):
  user = User.objects.get(username=instance.user.username).delete()
