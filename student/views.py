from django.shortcuts import render,redirect
from home.models import Student,Class
from assignment.models import Assignment,MCQ,FileUpload
from teacher.models import AssignmentsLog
from .models import MCQResult,AttempQuestion,File
from django.contrib.auth.models import User
from home.templatetags import extras
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date
from django.utils import timezone
from home.views import PasswordNotMatch
# Create your views here.



def studIndex(request):
  if request.user.is_authenticated:
    if extras.has_group(request.user,'Student'):
      assignment = []
      student = Student.objects.get(user=request.user)
      if student.updated:
        ass = Assignment.objects.filter(ass_class=student.s_class).order_by("-date")
        for i in ass:
          if i.last_date>date.today():
            assignment.append(i)
        
        params = {
          'student':student,
          'assignments':assignment
        }
      else:
        return redirect('/student/update_data')
    else:
      return redirect('/')  
  else:
    return redirect('/')
  return render(request,'student/index.html',params)
  
def updateData(request):
  if request.user.is_authenticated:
    if extras.has_group(request.user,'Student'):
      student = Student.objects.get(user=request.user)
      if not student.updated:
        classes = Class.objects.all().order_by("class_name")
        if request.method == "POST":
          try:
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            control = request.POST.get('control')
            class_name = Class.objects.get(class_name=request.POST['class'])
            roll_no = request.POST['roll']
            email = request.POST['email']
            contact = request.POST['cont']
            dob = request.POST['dob']
            gender = request.POST['gender']
            cur_password = request.POST['current-password']
            new_password = request.POST['password']
            confirm_password = request.POST['con_password']    
            if new_password.replace(" ","") != confirm_password.replace(" ",""):
              raise PasswordNotMatch
            if request.user.check_password(cur_password):
              user = User.objects.get(username=request.user)
              user.first_name = first_name
              user.last_name = last_name
              user.email = email
              user.set_password(new_password)
              student.s_class = class_name
              student.s_roll = roll_no
              student.s_contact = contact
              student.s_dob = dob
              student.s_gender = gender
              student.updated = True
              user.save()
              student.save()
              messages.success(request,"Succesfully data updated")
            else:
              messages.error(request,"Invalid Current Password")
          except PasswordNotMatch:
            messages.error(request,'Password and Confirm Password should be same!')
        params = {
          'student' : student,
          'classes' : classes,
        }
        return render(request,'student/update_data.html',params)
      else:
        return redirect('/student')  
    else:
      return redirect('/')  
  else:
    return redirect('/')
def assignment(request,slug):
  if request.user.is_authenticated:
    if extras.has_group(request.user,'Student'):
      assignment = Assignment.objects.get(slug = slug)
      mcqs = MCQ.objects.filter(assignment=assignment)
      file_ass = FileUpload.objects.filter(assignment=assignment)
      params = {
        'assignment':assignment,
        'mcqs':mcqs,
        'file_ass':file_ass,
      }
    else:
      return redirect('/')
  else:
    return redirect('/')
  return render(request,'student/assignment.html',params)
  
def mcqResult(request,slug):
  if request.user.is_authenticated:
    if extras.has_group(request.user,'Student'):
      correct = 0
      attemp = 0
      assignment = Assignment.objects.get(slug=slug)
      mcq = MCQ.objects.filter(assignment=assignment)
      total_quetions = len(mcq)
      AttempQuestion.objects.all().delete()
      if request.method == 'POST':
        for i in mcq:
          ans = request.POST.get("ans"+str(i.pk))
          if ans != None:
            attemp += 1
            if str(ans).replace(" ","") == str(i.ans).replace(" ",""):
              correct += 1
            attemp_que = AttempQuestion.objects.create(
              student = request.user,
              mcq = i,
              s_ans = ans,
            )
          else:
            continue
        try:
          res = MCQResult.objects.get(student=request.user,assignment=assignment)
          res.attemp = attemp
          res.total_que = total_quetions
          res.correct = correct
          res.marks = correct
          res.save()
        except MCQResult.DoesNotExist:
          res = MCQResult.objects.create(
            assignment = assignment,
            student = request.user,
            total_que = total_quetions,
            attemp = attemp,
            correct = correct,
            marks = correct,
          )
      attemp_questions = AttempQuestion.objects.filter(student=request.user)
      
      
      params = {
        "assignment" : assignment,
        "attemp_questions" : attemp_questions,
        "res" : res,
      }  
      
      
      return render(request,"student/mcq_result.html",params)
    else:
      return redirect("/")
  else:
    return redirect("/")
  


def fileSubmit(request,slug):
  if request.user.is_authenticated:
    if extras.has_group(request.user,'Student'):
      assignment = Assignment.objects.get(slug=slug)
      questions = FileUpload.objects.filter(assignment = assignment)
      try:
        log = AssignmentsLog.objects.get(student=request.user,assignment=assignment)
        log.submit_on = timezone.now()
      except AssignmentsLog.DoesNotExist:
        log = AssignmentsLog.objects.create(
          student=request.user,
          assignment=assignment,
        )
      if request.method == "POST":
          for i in questions:
            try:
              file = request.FILES.get("file"+str(i.pk))
              if file is not None:
                file_upload = File.objects.get(
                  student=request.user,
                  assignment=assignment,
                  question=i.desc,
                )
                file_upload.file.delete(save=True)
                file_upload.file = file
                file_upload.save()
              else:
                continue
            except File.DoesNotExist:
              if file is not None:
                file_upload = File.objects.create(
                  student = request.user,
                  assignment=assignment,
                  question = i.desc,
                  file = file,
                )
              else:
                continue
            else:
              messages.success(request,"File uploaded!")
      return redirect("/student")
    else:
      return redirect("/")
  else:
    return redirect("/")
      
  

# signals (Triggers)
@receiver(post_save,sender=MCQResult)
def addLog(sender,instance,created,**kwargs):
  if created:
    log = AssignmentsLog.objects.create(
      assignment = instance.assignment,
      student = instance.student,
      result = instance,
    )
  else:
    try:
      log = AssignmentsLog.objects.get(assignment=instance.assignment,student=instance.student)
      log.submit_on = timezone.now()
      log.result = instance
      log.save()
    except AssignmentsLog.DoesNotExist:
      log = AssignmentsLog.objects.create(
      assignment = instance.assignment,
      student = instance.student,
      result = instance,
    )

      
    