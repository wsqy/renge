from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from RGPY.models import Student, Banji
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import django.db.models.fields.related_descriptors


# Create your views here.
def test(request):
    return render(request, "RGPY/base.html", locals())


def register(request):
    if request.method == "POST" and request.POST:
        Student.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            email=request.POST['email'],
            phone=request.POST['phone'],
        )
        return HttpResponse("注册成功")
    return render(request, "RGPY/register.html", locals())


def login(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = auth.authenticate(username=username, password=password)
        next = request.GET.get("next", "/")
        if user is not None:
            auth.login(request, user)
            return redirect(next)
    return render(request, "RGPY/login.html", locals())


def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url='/login/')
def index(request):
    try:
        if request.user.ouruser.is_student():
            print(1)
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_department():
            print(2)
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_college():
            print(3)
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_manage():
            print(4)
            return render(request, "RGPY/Manage/ManageIndex.html", locals())
    except:
        print(5)
        return render(request, "RGPY/Manage/ManageIndex.html", locals())


@login_required(login_url='/login/')
def user_info(request):
    print("------")
    print(dir(request.user))
    print("------")
    print(dir(request.user.ouruser))
    print("------")
    student = {
        "first_name": request.user.ouruser.student.get_short_name(),
        "username": request.user.ouruser.student.get_username(),
        "phone": request.user.ouruser.student.phone,
        "email": request.user.ouruser.student.email,
        "banji": request.user.ouruser.student.banji,
        "department": request.user.ouruser.student.banji.department,
        "college": request.user.ouruser.student.banji.department.college,
    }
    if request.method == "POST" and request.POST:
        u = Student.objects.get(username=request.user.ouruser.student.get_username())
        u.phone = request.POST.get("phone")
        u.email = request.POST.get("email")
        new_passwd = request.POST.get("password_new", "")
        if new_passwd != "":
            u.set_password(new_passwd)
        u.save()
        return HttpResponse("个人信息修改成功")
    else:
        return render(request, "RGPY/StudentInfo.html", locals())


def check_passwd(request):
    username = request.GET.get("username")
    password = request.GET.get("passwd")
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        result = 1
    else:
        result = 0
    return HttpResponse(result)
