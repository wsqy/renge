from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from RGPY.models import Student, Banji, CollegeManage, DepartmentManage, Manage
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from RGPY.forms import CreateCollegeForm, CreateDepartmentForm, ChangePasswordForm


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
    if request.GET.get("mes"):
        message = request.GET.get("mes")
    try:
        if request.user.ouruser.is_student():
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_department():
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_college():
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.is_manage():
            return render(request, "RGPY/Manage/ManageIndex.html", locals())
    except:
        return render(request, "RGPY/Manage/ManageIndex.html", locals())


@login_required(login_url='/login/')
def user_info(request):
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


@login_required(login_url='/login/')
def create_college_manage(request):
    if request.method == "POST":
        # 如果是POST,接收用户输入
        create_college_manage_form = CreateCollegeForm(request.POST)
        # 表单验证
        if create_college_manage_form.is_valid():
            CollegeManage.objects.create_user(
                username=create_college_manage_form.cleaned_data['username'],
                password=create_college_manage_form.cleaned_data['password'],
                first_name=create_college_manage_form.cleaned_data['first_name'],
                email=create_college_manage_form.cleaned_data['email'],
                phone=create_college_manage_form.cleaned_data['phone'],
                level=1,
            )
            message = "成功创建学院管理员:%s" % (create_college_manage_form.cleaned_data['username'])
            return redirect("/?mes=%s" % (message,))
    else:
        create_college_manage_form = CreateCollegeForm()
    return render(request, "RGPY/Manage/create_college.html", locals())


@login_required(login_url='/login/')
def create_department_manage(request):
    if request.method == "POST":
        # 如果是POST,接收用户输入
        create_department_manage_form = CreateDepartmentForm(request.POST)
        # 表单验证
        if create_department_manage_form.is_valid():
            DepartmentManage.objects.create_user(
                username=create_department_manage_form.cleaned_data['username'],
                password=create_department_manage_form.cleaned_data['password'],
                first_name=create_department_manage_form.cleaned_data['first_name'],
                email=create_department_manage_form.cleaned_data['email'],
                phone=create_department_manage_form.cleaned_data['phone'],
                department=create_department_manage_form.cleaned_data['department'],
                level=2,
            )
            message = "成功创建系管理员:%s" % (create_department_manage_form.cleaned_data['username'])
            return redirect("/?mes=%s" % (message,))
    else:
        create_department_manage_form = CreateDepartmentForm()
    return render(request, "RGPY/Manage/create_department.html", locals())


@login_required(login_url='/login/')
def change_password(request):
    if request.method == "POST":
        # 如果是POST,接收用户输入
        change_password_form = ChangePasswordForm(request.POST)
        # 表单验证
        if change_password_form.is_valid():
            u = Manage.objects.get(username=request.user.ouruser.manage.get_username())
            new_passwd = request.POST.get("password_new", "")
            if new_passwd != "":
                u.set_password(new_passwd)
                u.save()
            message = "密码修改成功"
            return redirect("/?mes=%s" % (message,))
    else:
        change_password_form = ChangePasswordForm()
    return render(request, "RGPY/change_password.html", locals())
