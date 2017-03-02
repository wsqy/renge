from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from RGPY.models import Student, Banji, CollegeManage, DepartmentManage, Manage, OurUser
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from RGPY.forms import CreateCollegeForm, CreateDepartmentForm, ChangePasswordForm, CreateBanjiForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse


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
        print("------")
        print(username)
        print(password)
        print("------")
        user = auth.authenticate(username=username, password=password)
        print(user)
        next = request.GET.get("next", "/")
        print(next)
        if user is not None:
            print("登录")
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
    print(request.user.ouruser.level)
    try:
        if request.user.ouruser.level == '1':
            print("学生用户")
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.level == '2':
            print("系管理员")
            return render(request, "RGPY/Department/index.html", locals())
        elif request.user.ouruser.level == '3':
            print("学院管理员")
            return render(request, "RGPY/StudentIndex.html", locals())
        elif request.user.ouruser.level == '4':
            print("超级管理员")
            return render(request, "RGPY/Manage/index.html", locals())
    except Exception as e:
        print(e)
        print("djang用户")
        return render(request, "RGPY/Manage/index.html", locals())


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


@login_required(login_url='/login/')
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
                level=3,
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
            print(change_password_form.cleaned_data)
            print(request.user)
            u = OurUser.objects.get(username=request.user)
            new_passwd = change_password_form.cleaned_data.get("password_new", "")
            if new_passwd != "":
                u.set_password(new_passwd)
                u.save()
            message = "密码修改成功"
            return redirect("/?mes=%s" % (message,))
    else:
        change_password_form = ChangePasswordForm()
    return render(request, "RGPY/change_password.html", locals())


# 分页代码
def getPage(request, user_list, pageListNum=10):
    page_paginator = Paginator(user_list, pageListNum)
    try:
        page = int(request.GET.get("page", 1))
        user_list = page_paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger) as e:
        logger.error(e)
        # 出错默认跳转至第一页
        user_list = page_paginator.page(1)
    return user_list


@login_required(login_url='/login/')
def college_user_list(request):
    # try:
    #     user_list = CollegeManage.objects.all()
    # except:
    #     raise Http404()
    user_list = get_list_or_404(CollegeManage)
    return render(request, 'RGPY/Manage/user_list.html', locals())


@login_required(login_url='/login/')
def department_user_list(request):
    user_list = get_list_or_404(DepartmentManage)
    return render(request, 'RGPY/Manage/user_list.html', locals())


@login_required(login_url='/login/')
def reset_password(request):
    userId = request.GET.get("userId")
    u = OurUser.objects.get(id=userId)
    print(request.user.ouruser.level)
    print(u.level)
    if int(request.user.ouruser.level) >= int(u.level):
        u.set_password("123456")
        u.save()
        result = 1
    else:
        result = 0
    return HttpResponse(result)


@login_required(login_url='/login/')
def department_list(request):
    # 如果用户级别是4(超级管理员)，设置flag=True即可以查看,否则不允许查看
    if int(request.user.ouruser.level) == 4:
        flag = True
    else:
        flag = False
    return render(request, 'RGPY/Manage/department_list.html', locals())


@login_required(login_url='/login/')
def banji_list(request):
    # print(dir(request.user.ouruser.departmentmanage.department))
    department = request.user.ouruser.departmentmanage.department
    # print(department)
    # print(type(department))
    # print("----")
    result = get_list_or_404(Banji, department=department)
    # print(result)
    # banji = result[0]
    # print(dir(banji))
    # print(banji.grade)
    # print(banji.id)
    # print(banji.student_set.get(is_banji_admin=True))
    # print(banji.student_set.count())
    # print(department)
    banji_list = []
    for banji in result:
        try:
            # 过滤班级负责人
            admin = banji.student_set.get(is_banji_admin=True)
            # 看看班级负责人的姓名有没有
            name = admin.get_short_name()
            # 如果有学号后面再加姓名 类似于 241392335(王美熔)
            if name:
                admin = "%s(%s)" % (admin.username, name,)
        except Exception as e:
            # 如果没设置班级管理员,显示 未设置
            print(e)
            admin = "未设置"
        one = {
            'banji': banji,
            'grade': banji.grade,
            'count': banji.student_set.count(),
            'admin': admin,
            'department': department,
            'id': banji.id,
        }
        banji_list.append(one)
    return render(request, 'RGPY/Department/banji_list.html', locals())


@login_required(login_url='/login/')
def banji_info(request, banji):
    student_list = Banji.objects.get(pk=banji).student_set.all()
    print(student_list)
    return render(request, 'RGPY/Department/student_list.html', locals())


@login_required(login_url='/login/')
def banji_delete(request, banji):
    print(request.user.ouruser.level)
    if int(request.user.ouruser.level) == 2:
        print("班级%s" % (banji,))
        Banji.objects.filter(pk=banji).delete()
        result = 1
    else:
        result = 0
    return HttpResponse(result)


@login_required(login_url='/login/')
def banji_add(request):
    print(request.method)
    grade_list = []
    import time
    year = time.strftime('%Y', time.localtime(time.time()))
    month = time.strftime('%m', time.localtime(time.time()))
    # month = "09"
    # print(month)
    if int(month) < 6:
        year = str(int(year) - 1)
    for i in range(4):
        grade_list.append(year)
        year = str(int(year) - 1)
    banji = {
        "department": request.user.ouruser.departmentmanage.department,
        "grade": grade_list,
    }
    if request.method == "POST" and request.POST:
        # print(request.POST)
        Banji.objects.create(
            banji=request.POST.get("banji"),
            department=request.user.ouruser.departmentmanage.department,
            grade=request.POST.get("grade"),
        )
        return HttpResponseRedirect(reverse('RGPY:banji_list'))
    else:
        banji_form = CreateBanjiForm()
    return render(request, 'RGPY/Department/banji_add.html', locals())


@login_required(login_url='/login/')
def student_reset_admin(request, student):
    print(request.user.ouruser.level)
    if int(request.user.ouruser.level) == 2:
        print("学生%s" % (student,))
        u = Student.objects.get(pk=student)
        is_admin = not u.is_banji_admin
        u.is_banji_admin = is_admin
        u.save()
        result = 1
    else:
        result = 0
    return HttpResponse(result)


@login_required(login_url='/login/')
def user_del(request, userId):
    try:
        u = OurUser.objects.get(pk=userId)
        if int(u.level) < int(request.user.ouruser.level):
            u.delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0
    return HttpResponse(result)


def student_list_upload(request):
    if request.method == "POST":
        print(request.FILES)
        files = request.FILES.get('excel')
        print(files)
        import xlrd
        wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
        # 关键点在于这里
        table = wb.sheets()[0]
        row = table.nrows
        for i in range(1, row):
            col = table.row_values(i)
        print(col)
        return HttpResponse("POST")
    else:
        print(request.method)
        return HttpResponse("test")
