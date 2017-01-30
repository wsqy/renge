from django.shortcuts import render
from django.http import HttpResponse
from RGPY.models import Student, Banji
from django.contrib.auth import login, logout, authenticate


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
        user = authenticate(username=username, password=password)
        if user is not None:
            print(user)
            print("登录成功")
            # login(request, user)
        else:
            print(user)
    return render(request, "RGPY/login.html", locals())
