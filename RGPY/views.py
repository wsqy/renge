from django.shortcuts import render
from django.http import HttpResponse
from RGPY.forms import RegisterForm
from RGPY.models import Student, Banji


# Create your views here.
def test(request):
    return HttpResponse("人格培养管理平台测试页")


def register(request):
    print(request.method)
    print("-----")
    if request.method == "POST" and request.POST:
        print(request.POST)
        print("-----")
        # wangluo_banji = Banji.objects.get(id=1)
        # print(wangluo_banji.id)
        registerFrom = RegisterForm(request.POST)
        print(registerFrom)
        print("-----")
        if registerFrom.is_valid():
            clear_data = registerFrom.cleaned_data
            print(clear_data)
            print("-----")
            Student.objects.create_user(
                username=clear_data['username'],
                password=clear_data['password'],
                email=clear_data['email'],
                phone=clear_data['phone'],
            )
            return HttpResponse("注册成功")
    return render(request, "RGPY/register.html", locals())
