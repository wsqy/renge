from django.shortcuts import render, redirect
from django.http import HttpResponse
from RGPY.models import Student, Banji
from django.contrib import auth


# Create your views here.
def test(request):
    return HttpResponse("人格培养管理平台测试页")


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
        if user is not None:
            auth.login(request, user)
            return redirect("/")
    return render(request, "RGPY/login.html", locals())


def index(reuqest):
    return HttpResponse("这是首页")
