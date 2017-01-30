from django.db import models
from django.contrib.auth.models import User


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
    college = models.ForeignKey(College, verbose_name="所属学院")

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
    department = models.ForeignKey(Department, verbose_name="所属系别")

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.banji

    __repr__ = __str__


class Stuent(User):
    """
    这里继承django的User类，他已经定义了以下属性username password first_name last_name email is_staff is_active date_joined last_login
    username 在我们的系统里用以代表学号
    first_name 在我们的系统里用以代表姓名
    password 密码 在我们的系统里直接使用  加密我们采用基于SHA256 的哈希值使用PBKDF2算法，它是NIST推荐的算法
    """
    phone = models.CharField(max_length=11, verbose_name="用户手机", blank=True, null=True)
    banji = models.ForeignKey(Banji, verbose_name="所属班级")
    is_banji_admin = models.BooleanField(
        default=False,
        help_text='是否是班级管理员.',
    )
    # 这里使用PositiveSmallIntegerField 因为获得时长肯定是正数 并且不会超过32767
    score = models.PositiveSmallIntegerField("已获时长")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
