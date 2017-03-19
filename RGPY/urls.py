from RGPY import views
from django.conf.urls import url, include

app_name = 'RGPY'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^test/$', views.test, name='test'),

    # 登录类
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user_del/(?P<userId>[0-9]+)/$', views.user_del, name='user_del'),

    # 学生类
    url(r'^user_info/$', views.user_info, name='user_info'),
    url(r'^check_passwd/$', views.check_passwd, name='check_passwd'),

    # 超级管理员
    url(r'^createUser/college/$', views.create_college_manage, name='create_college_manage'),
    url(r'^createUser/Department/$', views.create_department_manage, name='create_department_manage'),

    # 修改密码(管理员专用的)
    url(r'^change_password/$', views.change_password, name='change_password'),
    # 重置密码
    url(r'^reset_password/$', views.reset_password, name='reset_password'),

    # 报表
    # 用户类
    url(r'^user_list/college/$', views.college_user_list, name='college_user_list'),
    url(r'^user_list/department/$', views.department_user_list, name='department_user_list'),

    # 系别列表
    url(r'^list/department/$', views.department_list, name='department_list'),

    # 系管理员使用
    url(r'^department/', include([
        url(r'^banji_list/$', views.banji_list, name='banji_list'),
        url(r'^banji/(?P<banji>[0-9]+)/$', views.banji_info, name='banji_info'),
        url(r'^banji/(?P<banji>[0-9]+)/delete/$', views.banji_delete, name='banji_delete'),
        url(r'^banji/add/$', views.banji_add, name='banji_add'),
        url(r'^student/(?P<student>[0-9]+)/reset_admin/$', views.student_reset_admin, name='student_reset_admin'),
    ])),

    url(r'^excel/', include([
        url(r'^upload/student_list/$', views.student_list_upload, name='student_list_upload'),

    ])),

    url(r'^task/', include([
        url(r'^publish/$', views.task_publish, name='task_publish'),
        url(r'^list/$', views.task_list, name='task_list'),
        url(r'^(?P<taskid>[0-9]+)/del/$', views.task_delete, name='task_delete'),
        url(r'^(?P<taskid>[0-9]+)/info/$', views.task_info, name='task_info'),
        url(r'^agree/(?P<taskid>[0-9]+)/(?P<studentid>[0-9]+)/$', views.agree_apply, name='agree_apply'),
        url(r'^addScore/(?P<taskid>[0-9]+)/(?P<studentid>[0-9]+)/$', views.addScore, name='addScore'),

        url(r'^student/', include([
            url(r'^list/department/$', views.task_department_list, name='task_department_list'),
            url(r'^list/college/$', views.task_college_list, name='task_college_list'),
            url(r'^(?P<taskid>[0-9]+)/info/$', views.task_student_info, name='task_student_info'),
            url(r'^(?P<taskid>[0-9]+)/baoming/$', views.task_student_baoming, name='task_student_baoming'),
            url(r'^apply/authentication$', views.apply_authentication, name='apply_authentication'),
            url(r'^apply/authentication/list$', views.my_apply_authentication_list, name='my_apply_authentication_list'),
            url(r'^apply/authentication/info/(?P<applyid>[0-9]+)/', views.apply_authentication_info, name='apply_authentication_info'),

            url(r'^authentication/list/', views.authentication_list, name='authentication_list'),
            url(r'^authentication/agree/(?P<authentication_id>[0-9]+)/(?P<agree_id>[0-9])/$', views.authentication_agree, name='authentication_agree'),
            url(r'^authentication/batch/', views.authentication_batch, name='authentication_batch'),

        ])),
    ])),

    url(r'^news/$', views.news, name='news'),
    url(r'^news/(?P<newid>[0-9]+)/read/$', views.news_reader, name='news_reader'),

]
