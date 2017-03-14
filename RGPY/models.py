from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


# Create your models here.
class College(models.Model):
    college = models.CharField("学院", max_length=50)

    class Meta:
        verbose_name = "学院"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.college


class Department(models.Model):
    department = models.CharField("系别", max_length=50)
    college = models.ForeignKey(College, verbose_name="所属学院", default=1, blank=True)

    class Meta:
        verbose_name = "系别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.department


class Banji(models.Model):
    """
    班级的英文 class是python的关键字，防止冲突这里用中文拼音
    """
    banji = models.CharField("班级", max_length=50)
    department = models.ForeignKey(Department, verbose_name="所属系别", default=2, blank=True)
    grade = models.CharField("年级", max_length=10, default="2013",)

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name
        ordering = ['-grade', ]

    def __str__(self):
        return self.banji

    __repr__ = __str__


class OurUser(User):
    """
    这里继承django的User类，他已经定义了以下属性username password first_name last_name email is_staff is_active date_joined last_login
    username 在我们的系统里用以代表学号
    first_name 在我们的系统里用以代表姓名
    password 密码 在我们的系统里直接使用  加密我们采用基于SHA256 的哈希值使用PBKDF2算法，它是NIST推荐的算法
    """
    user_level = (
        ('1', "学生"),
        ('2', "系管理员"),
        ('3', "院管理员"),
        ('4', "管理员"),
    )
    phone = models.CharField(max_length=11, verbose_name="用户手机", blank=True, null=True)
    level = models.CharField(max_length=1, verbose_name="用户级别", choices=user_level, default='1')

    class Meta:
        verbose_name = "自定义用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Student(OurUser):
    banji = models.ForeignKey(Banji, verbose_name="所属班级", default=1, blank=True)
    is_banji_admin = models.BooleanField(
        verbose_name="是否是班级管理员",
        default=False,
        help_text='是否是班级管理员.',
    )
    # 这里使用PositiveSmallIntegerField 因为获得时长肯定是正数 并且不会超过32767
    score = models.PositiveSmallIntegerField("已获时长", default=0, blank=True)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name
        ordering = ['username', ]


class DepartmentManage(OurUser):
    department = models.ForeignKey(Department, verbose_name="管理的系别", default=2, blank=True)
    banji = models.ForeignKey(Banji, verbose_name="管理班级", null=True, blank=True)

    class Meta:
        verbose_name = "系管理员"
        verbose_name_plural = verbose_name


class CollegeManage(OurUser):
    class Meta:
        verbose_name = "院管理员"
        verbose_name_plural = verbose_name


class Manage(OurUser):
    class Meta:
        verbose_name = "管理员"
        verbose_name_plural = verbose_name


class COS(models.Model):
    service = models.CharField(max_length=32, verbose_name="任务类别")

    class Meta:
        verbose_name = "任务类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.service)


class Mission(models.Model):
    desc = models.CharField(max_length=50, verbose_name="任务名称", blank=False)
    promulgator = models.ForeignKey(User, verbose_name="任务发布者")
    required = models.PositiveSmallIntegerField(verbose_name="需要的人数", )
    service_type = models.ForeignKey(COS, verbose_name="任务类型", default=2)
    start_time = models.DateField(verbose_name="开始报名时间", default=timezone.now)
    end_time = models.DateField(verbose_name="报名结束时间", default=timezone.now)
    task_time = models.DateField(verbose_name="任务完成时间",default=timezone.now, )
    score = models.PositiveSmallIntegerField(verbose_name="时长", default=2)
    remark = models.TextField(verbose_name="备注")
    flag = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        verbose_name = "任务"
        verbose_name_plural = verbose_name
        ordering = ('-task_time', 'end_time', '-id')

    def __str__(self):
        return str(self.desc)


class TaskApply(models.Model):
    student = models.ForeignKey(Student, verbose_name="申请人")
    task = models.ForeignKey(Mission, verbose_name="任务")
    is_approval = models.BooleanField(verbose_name="是否批准", default=False)
    add_score = models.BooleanField(verbose_name="是否增加时长", default=False)

    class Meta:
        unique_together = (("student", "task"),)


class NEWS(models.Model):
    reader = models.ForeignKey(OurUser, verbose_name="读者")
    info = models.TextField(verbose_name="消息")
    link = models.CharField(max_length=100, verbose_name="链接", blank=True)
    time = models.DateField(verbose_name="时间", default=timezone.now)
    is_read = models.BooleanField(verbose_name="是否已读", default=False)

    class Meta:
        ordering = ('-id', )
