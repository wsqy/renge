from RGPY import views
from django.conf.urls import url

app_name = 'RGPY'

urlpatterns = [
    # 测试样例
    url(r'^test', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^test', views.test, name='test'),

    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),

    url(r'^user_info', views.user_info, name='user_info'),
]
