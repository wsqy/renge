from RGPY import views
from django.conf.urls import url

app_name = 'RGPY'

urlpatterns = [
    # 测试样例
    url(r'test', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^test', views.test, name='test'),

    # 登录类
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout, name='logout'),

    # 学生类
    url(r'^user_info', views.user_info, name='user_info'),
    url(r'^check_passwd', views.check_passwd, name='check_passwd'),

    # 超级管理员
    url(r'^createUser/college', views.create_college_manage, name='create_college_manage'),
    url(r'^createUser/Department', views.create_department_manage, name='create_department_manage'),

    # 修改密码(管理员专用的)
    url(r'^change_password', views.change_password, name='change_password'),
    # 重置密码
    url(r'^reset_password', views.reset_password, name='reset_password'),


    # 报表
    # 用户类
    url(r'^user_list/college', views.college_user_list, name='college_user_list'),
    url(r'^user_list/department', views.department_user_list, name='department_user_list'),

    # 系
    url(r'^list/department', views.department_list, name='department_list'),
]
