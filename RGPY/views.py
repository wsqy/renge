from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def test(request):
    return HttpResponse("人格培养管理平台测试页")


def register(request):
    return render(request, "RGPY/register.html")
