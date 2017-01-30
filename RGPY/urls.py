from RGPY import views
from django.conf.urls import url

app_name = 'RGPY'

urlpatterns = [
    # 测试样例
    url(r'^test', views.test, name='test'),
]
