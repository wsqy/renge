from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from RGPY.models import Student, Banji, CollegeManage, DepartmentManage, \
    Manage, OurUser, Mission, COS, TaskApply, NEWS, TaskList, AddScoreApply
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from RGPY.forms import CreateCollegeForm, CreateDepartmentForm, \
    ChangePasswordForm, CreateBanjiForm
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from RGPY import Util
from RGPY.Notice import NOTICE
from datetime import datetime


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
    print(request.method)
    print(request.POST)
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


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect("/")


@login_required(login_url='/login/')
def index(request):
    if request.GET.get("mes"):
        message = request.GET.get("mes")
    try:
        if request.user.ouruser.level == '1':
            print("学生用户")
            return redirect('/news')
            # return render(request, "RGPY/student/StudentIndex.html", locals())
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
        return render(request, "RGPY/student/StudentInfo.html", locals())


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
def renge_require(request):
    return render(request, "RGPY/student/renge_yaoqiu.html", locals())


@login_required(login_url='/login/')
def attach_score(request):
    _u = request.user.ouruser.student
    score = _u.score
    task_list = TaskList.objects.filter(student=_u)
    return render(request, "RGPY/student/attach_score.html", locals())


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
    # result = get_list_or_404(Banji, department=department)
    result = Banji.objects.filter(department=department)
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
    student_list = Banji.objects.get(id=banji).student_set.all()
    print(student_list)
    return render(request, 'RGPY/Department/student_list.html', locals())


@login_required(login_url='/login/')
def banji_delete(request, banji):
    print(request.user.ouruser.level)
    if int(request.user.ouruser.level) == 2:
        print("班级%s" % (banji,))
        Banji.objects.filter(id=banji).delete()
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
        u = Student.objects.get(id=student)
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
        u = OurUser.objects.get(id=userId)
        if int(u.level) < int(request.user.ouruser.level):
            u.delete()
            result = 1
        else:
            result = 0
    except Exception as e:
        print(e)
        result = 0
    return HttpResponse(result)


@login_required(login_url='/login/')
def student_list_upload(request):
    if request.method == "POST":
        print(request.FILES)
        files = request.FILES.get('excel')
        print(files)
        import os
        import xlrd
        wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
        # 关键点在于这里
        table = wb.sheets()[0]
        for i in range(1, table.nrows):
            row = table.row_values(i)
            phone = None if row[3] == '' else int(row[3])
            if row[4] == '1':
                is_banji_admin = True
            else:
                is_banji_admin = False
            banji = row[5] or os.path.splitext(files)[1]
            Student.objects.create_user(
                username=int(row[0]),
                first_name=row[1],
                email=row[2],
                phone=phone,
                is_banji_admin=is_banji_admin,
                banji=Banji.objects.get(banji=banji),
            )
        return redirect(request.MEAT.get("HTTP_REFERER", "/"))
    else:
        print(request.method)
        error_message = "上传错误,请检查"
        return render("404.html", locals())


@login_required(login_url='/login/')
def task_list(request):
    task_list = Mission.objects.filter(promulgator_id=request.user.id)
    print(task_list)
    return render(request, "RGPY/Department/task_list.html", locals())


@login_required(login_url='/login/')
def task_publish(request):
    if request.method == "POST":
        print(request.POST)
        mission = Mission()
        mission.desc = request.POST.get('desc')
        mission.promulgator = OurUser.objects.get(id=request.user.id)
        mission.required = request.POST.get('required')
        mission.service_type = COS.objects.get(id=(int(request.user.ouruser.level) + 1))
        mission.start_time = str2date(request.POST.get('start_time'))
        mission.end_time = str2date(request.POST.get('end_time'))
        mission.task_time = str2date(request.POST.get('task_time'))
        mission.score = request.POST.get('score')
        mission.remark = request.POST.get('remark')
        mission.save()
        return redirect(reverse('RGPY:task_list'))
    else:
        return render(request, 'RGPY/Department/task_publish.html', locals())


@login_required(login_url='/login/')
def task_delete(request, taskid):
    try:
        m = Mission.objects.get(id=taskid)
        m.flag = not m.flag
        m.save()
        result = 1
    except Exception as e:
        print(e)
        result = -1
    return HttpResponse(result)


def str2date(str):
    return str.replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')


@login_required(login_url='/login/')
def task_info(request, taskid):
    mission = Mission.objects.get(id=taskid)
    if request.method == "POST":
        print(request.POST)
        mission.desc = request.POST.get('desc')
        mission.required = request.POST.get('required')
        mission.start_time = str2date(request.POST.get('start_time'))
        mission.end_time = str2date(request.POST.get('end_time'))
        mission.task_time = str2date(request.POST.get('task_time'))
        mission.score = request.POST.get('score')
        mission.remark = request.POST.get('remark')
        mission.save()
        return redirect(reverse('RGPY:task_list'))
    else:
        try:
            task_list = TaskApply.objects.filter(task_id=taskid)
            student_list = []
            for task in task_list:
                student = {}
                s = Student.objects.get(id=task.student_id)
                student['username'] = s.username
                student['id'] = s.id
                student['first_name'] = s.first_name
                student['banji'] = s.banji
                student['department'] = s.banji.department
                student['score'] = s.score
                student['phone'] = s.phone
                student['email'] = s.email
                student['is_approval'] = task.is_approval
                student_list.append(student)
        except Exception as e:
            print(e)
        return render(request, 'RGPY/Department/task_info.html', locals())


@login_required(login_url='/login/')
def agree_apply(request, taskid, studentid):
    try:
        task = TaskApply.objects.get(task_id=taskid)
        task.is_approval = not task.is_approval
        approval = task.is_approval
        _u = OurUser.objects.get(id=studentid)
        _m = Mission.objects.get(id=taskid)

        notice = NOTICE(user=_u, task=_m, type=2, approval=approval)
        notice.send_notice()

        task.save()
        if approval:
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@login_required(login_url='/login/')
def addScore(request, taskid, studentid):
    try:
        task = TaskApply.objects.get(task_id=taskid)
        if task.add_score:
            return HttpResponse("0")
        task.add_score = True
        _u = Student.objects.get(id=studentid)
        _m = Mission.objects.get(id=taskid)
        _u.score += _m.score
        r = Util.get_user_info(request)

        if r.get('type', '1') == '1':
            if request.user.ouruser.student.is_banji_admin:
                _task_type = "班级任务"
            else:
                _task_type = "个人任务"
        elif r.get('type', '1') == '2':
            _task_type = "系任务"
        elif r.get('type', '1') == '3':
            _task_type = "院任务"
        else:
            _task_type = "不确定的任务类型"
        shen_he_ren = OurUser.objects.get(id=_m.promulgator.id)
        TaskList.objects.create(
            name=_m,
            task_type=_task_type,
            student=_u,
            review=shen_he_ren,
        )
        task.save()
        _u.save()
        # 发送通知
        notice = NOTICE(user=_u, task=_m, type=3)
        notice.send_notice()
        return HttpResponse('1')
    except Exception as e:
        print(e)
        return HttpResponse('-1')


@login_required(login_url='/login/')
def task_department_list(request):
    # 用户所在的系别
    student_depar = request.user.ouruser.student.banji.department
    # print(student_depar)
    # 找出自己所在系的全部管理员
    depar_admin = DepartmentManage.objects.filter(department=student_depar)
    # print(depar_admin)
    task_list = Mission.objects.filter(promulgator__in=depar_admin)
    # print(task_list)
    return render(request, "RGPY/student/task_list.html", locals())


@login_required(login_url='/login/')
def task_college_list(request):
    pass


@login_required(login_url='/login/')
def task_student_info(request, taskid):
    try:
        mission = Mission.objects.get(id=taskid)
    except Exception as e:
        print(e)
    finally:
        return render(request, 'RGPY/student/task_info.html', locals())


@login_required(login_url='/login/')
def task_student_baoming(request, taskid):
    try:
        s = request.user.ouruser.student
        _m = Mission.objects.get(id=taskid)
        TaskApply.objects.create(student=s, task=_m)

        # 发送通知
        notice = NOTICE(user=s, task=_m, type=1)
        notice.send_notice()

        return HttpResponse("1")
    except Exception as e:
        print(e)
        return HttpResponse("-1")


@login_required(login_url='/login/')
def news(request):
    u = request.user.ouruser
    try:
        news_list = NEWS.objects.filter(reader=u, is_read=False)
    except:
        print(e)
    finally:
        return render(request, 'RGPY/student/new.html', locals())


@login_required(login_url='/login/')
def news_reader(request, newid):
    try:
        n = NEWS.objects.get(id=newid)
        n.is_read = True
        n.save()
    except Exception as e:
        pass
    finally:
        return HttpResponse("ok")


@login_required(login_url='/login/')
def apply_authentication(request):
    if request.method == "POST":
        _u = request.user.ouruser.student
        asa = AddScoreApply()
        asa.student = _u
        asa.desc = request.POST.get('desc', '')
        asa.score = int(request.POST.get('score', 0))
        asa.apply_time = datetime.now()
        asa.remark = request.POST.get('remark', '')
        asa.save()
        print(asa.id)

        # 发送通知
        notice = NOTICE(user=_u, apply=asa, type=4)
        notice.send_notice()

        return redirect(reverse('RGPY:apply_authentication_info', kwargs={"applyid": asa.id, }))
    else:
        return render(request, 'RGPY/student/apply_authentication.html', locals())


@login_required(login_url='/login/')
def apply_authentication_info(request, applyid):
    if request.method == "POST":
        authentication = AddScoreApply.objects.get(id=applyid)
        authentication.desc = request.POST.get('desc', '')
        authentication.score = int(request.POST.get('score', 0))
        authentication.remark = request.POST.get('remark', '')
        authentication.save()

        # 发送通知
        _u = request.user.ouruser.student
        notice = NOTICE(user=_u, apply=authentication, type=5)
        notice.send_notice()
    else:
        try:
            authentication = AddScoreApply.objects.get(id=applyid)
        except Exception as e:
            print(e)
    return render(request, 'RGPY/student/apply_authentication_info.html', locals())


@login_required(login_url='/login/')
def my_apply_authentication_list(request):
    try:
        authentication_list = AddScoreApply.objects.filter(student=request.user.ouruser.student)
    except Exception as e:
        authentication_list = []
    finally:
        return render(request, 'RGPY/student/apply_authentication_list.html', locals())


@login_required(login_url='/login/')
def authentication_list(request):
    try:
        banji = request.user.ouruser.student.banji
        authentication_list = AddScoreApply.objects.filter(student__banji=banji, flag=None)
    except Exception as e:
        authentication_list = []
    finally:
        return render(request, 'RGPY/student/banji/apply_authentication_list.html', locals())


@login_required(login_url='/login/')
def authentication_agree(request, authentication_id, agree_id):
    try:
        _a = AddScoreApply.objects.get(id=authentication_id)
        agree_id = int(agree_id)
        if agree_id == 1:
            _a.flag = True
            _t = TaskList.objects.create(
                name=_a.desc,
                task_type="个人任务",
                student=_a.student,
                review=request.user.ouruser,
                taskDate=datetime.now()
            )
        else:
            _a.flag = False
        _a.save()

        # 发送通知
        notice = NOTICE(_a.student, apply=_a, agree_id=agree_id, type=6, level=[1, 2, 3])
        notice.send_notice()

    except Exception as e:
        print(e)
    finally:
        return redirect(request.META.get("HTTP_REFERER", '/'))


@login_required(login_url='/login/')
def authentication_batch(request):
    if request.method == "POST":
        desc = request.POST.get("desc", "")
        score = int(request.POST.get("score", 0))
        review_id = request.user.ouruser.id
        print(request.FILES)
        files = request.FILES.get('excel')
        print(files)
        import os
        import xlrd
        wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['excel'].read())
        # 关键点在于这里
        table = wb.sheets()[0]
        student_list = []
        for i in range(1, table.nrows):
            try:
                stu_no = str(int(table.row_values(i)[0]))
                print(stu_no)
                u = Student.objects.get(username=stu_no)
                TaskList.objects.create(
                    name=desc,
                    task_type="班级任务",
                    taskDate=datetime.now(),
                    review_id=review_id,
                    score=score,
                    student_id=u.id,
                )
                u.score += score
                u.save()
                # 发送通知
                notice = NOTICE(user=u, desc=desc, type=9, level=[1, 2, 3])
                notice.send_notice()
            except Exception as e:
                pass
        mes = "班级团体任务成功导入"
        return render(request, 'RGPY/student/banji/add_banji.html', locals())
    else:
        return render(request, 'RGPY/student/banji/add_banji.html', locals())
