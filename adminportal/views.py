from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User,Group
from home.models import Student,Teacher,Class,Subject
import sys

# Create your views here.
def adminIndex(request):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            students = Student.objects.all().order_by("s_class")
            teachers = Teacher.objects.all().order_by("user")
            classes = Class.objects.all().order_by("class_name")
            subjects = Subject.objects.all().order_by("class_name")
            if request.GET.get('filter-students') is not None and request.GET.get('filter-students')!="All":
                class_name = request.GET.get('filter-students')
                s_class = Class.objects.get(class_name=class_name)
                students = Student.objects.filter(s_class = s_class).order_by("user")
            if request.GET.get('filter-subjects') is not None and request.GET.get('filter-subjects') != "All":
                class_name = request.GET.get('filter-subjects')
                s_class = Class.objects.get(class_name=class_name)
                subjects = Subject.objects.filter(class_name=s_class).order_by("subject_name")

            if request.GET.get('search-student') is not None:
                querry = request.GET.get('search-student')
                users = User.objects.filter(
                    Q(first_name__icontains=querry) | Q(last_name__icontains=querry) | Q(username__icontains=querry)
                )
                students = Student.objects.filter(user__in=users)

            if request.GET.get('search-teacher') is not None:
                querry = request.GET.get('search-teacher')
                users = User.objects.filter(
                    Q(first_name__icontains=querry) | Q(last_name__icontains=querry) | Q(username__icontains=querry)
                )
                teachers = Teacher.objects.filter(user__in=users)

            if request.GET.get('search-class') is not None:
                querry = request.GET.get('search-class')
                classes = Class.objects.filter(
                    Q(class_name__icontains=querry) | Q(strength__icontains=querry)
                )
                

            if request.GET.get('search-subject') is not None:
                querry = request.GET.get('search-subject')
                subjects = Subject.objects.filter(subject_name__icontains=querry)

            params = {
                'students':students,
                'teachers':teachers,
                'classes' :classes,
                'subjects':subjects,
            }
            return render(request,'adminportal/index.html',params)
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def saveStudent(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                student = Student.objects.get(pk=id)
                user = User.objects.get(username=student.user.username)
                class_name = Class.objects.get(class_name=request.POST['class'+str(student.pk)])
                user.first_name = request.POST['first-name']
                user.last_name = request.POST['last-name']
                student.s_roll = request.POST['roll-no']
                student.s_class = class_name
                user.username = request.POST['control']
                student.s_dob = request.POST['dob']
                student.s_contact = request.POST['contact']
                user.email = request.POST['email']
                student.s_gender = request.POST['gender'+str(student.pk)]
                student.save()
                user.save()
                messages.success(request,"Save Successfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def saveTeacher(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                teacher = Teacher.objects.get(pk=id)
                user = User.objects.get(username=teacher.user.username)
                user.first_name = request.POST['first-name']
                user.last_name = request.POST['last-name']
                user.username = request.POST['control']
                teacher.t_dob = request.POST['dob']
                teacher.t_contact = request.POST['contact']
                user.email = request.POST['email']
                teacher.t_gender = request.POST['gender'+str(teacher.pk)]
                teacher.save()
                user.save()
                messages.success(request,"save succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def saveClass(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                cls = Class.objects.get(pk=id)
                cls.class_name = request.POST['class-name']
                cls.strength = request.POST['strength']
                cls.save()
                messages.success(request,"Save Successfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def saveSubject(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                subject = Subject.objects.get(pk=id)
                class_name = Class.objects.get(class_name=request.POST['class'+str(subject.pk)])
                Subject.subject_name = request.POST['subject-name']
                subject.class_name = class_name
                subject.save()
                messages.success(request,"save succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")
    

def adminLogin(request):
    if request.method == "POST":
        control = request.POST['control']
        password = request.POST['password']
        user = authenticate(username=control,password=password)
        if user is not None:
            if user.is_superuser or user.username == "T-502480":
                login(request,user)
                return redirect('/adminportal')
            else:
                messages.error(request,"Not Admin User")
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,"adminportal/login.html")

# APIs for admin
def adminLogout(request):
    logout(request)
    return redirect('/adminportal/admin_login')

def addStudent(request):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                first_name = request.POST['first-name'].replace(" ","")
                last_name = request.POST['last-name'].replace(" ","")
                roll_no = request.POST['roll-no'].replace(" ","")
                class_name = Class.objects.get(class_name=request.POST['class'])
                control = request.POST['control'].replace(" ","")
                password = first_name.capitalize()+"@"+control
                try:
                    user_created = False
                    group = Group.objects.get(name = "Student")
                    user = User.objects.create_user(
                        username = control,
                        password = password,
                        first_name = first_name,
                        last_name = last_name
                    )
                    user_created = True
                    user.groups.add(group)
                    student = Student.objects.create(
                        user = user,
                        s_roll = roll_no,
                        s_class = class_name,
                        updated = False
                    )
                except:
                    if user_created:
                        user.delete()
                    messages.error(request,sys.exc_info()[0])
                messages.success(request,"Add Student successully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def addTeacher(request):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                first_name = request.POST['first-name'].replace(" ","")
                last_name = request.POST['last-name'].replace(" ","")
                control = request.POST['control'].replace(" ","")
                password = first_name.capitalize()+"@"+control
                try:
                    user_created = False
                    group = Group.objects.get(name = "Teacher")
                    user = User.objects.create_user(
                        username = control,
                        password = password,
                        first_name = first_name,
                        last_name = last_name
                    )
                    user_created = True
                    user.groups.add(group)
                    teacher = Teacher.objects.create(
                        user = user,
                        updated = False
                    )
                except:
                    if user_created:
                        user.delete()
                    messages.error(request,sys.exc_info()[0])
                messages.success(request,"Add Student successully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def addClass(request):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                class_name = request.POST['class-name']
                strength = request.POST['strength']
                Class.objects.create(
                    class_name = class_name,
                    strength = strength
                )
                messages.success(request,"Add Class Succesfull")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def addSubject(request):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            if request.method == "POST":
                subject_name = request.POST['subject-name']
                class_name = Class.objects.get(class_name=request.POST['class'])
                Subject.objects.create(
                    subject_name = subject_name,
                    class_name = class_name
                )
                messages.success(request,"Add Class Succesfull")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def deleteStudent(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            student = Student.objects.get(pk=id)
            user = User.objects.get(username=student.user.username).delete()
            messages.success(request,"Delete Succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def deleteTeacher(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            teacher = Teacher.objects.get(pk=id)
            user = User.objects.get(username=teacher.user.username).delete()
            messages.success(request,"Delete Succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def deleteClass(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            class_name = Class.objects.get(pk=id).delete()
            messages.success(request,"Delete Succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")

def deleteSubject(request,id):
    if request.user.is_authenticated:
        if request.user.username == "T-502480" or request.user.is_superuser:
            subject = Subject.objects.get(pk=id).delete()
            messages.success(request,"Delete Succesfully")
            return redirect('/adminportal')
        else:
            return redirect("/adminportal/admin_login")
    else:
        return redirect("/adminportal/admin_login")