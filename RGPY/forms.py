from django.db import models
from django import forms
from RGPY.models import CollegeManage, DepartmentManage, Department


class CreateCollegeForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_rep = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="姓名", max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label="手机", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        try:
            CollegeManage.objects.get(username=username)
            raise forms.ValidationError("用户%s已经存在" % username)
        except CollegeManage.DoesNotExist:
            pass
        return username

    def clean(self):
        cleaned_data = super(CreateCollegeForm, self).clean()
        password = cleaned_data.get("password")
        password_rep = cleaned_data.get("password_rep")
        if password != password_rep:
            self._errors['password_rep'] = self.error_class(["两次输入的密码不一致"])
        return cleaned_data


class CreateDepartmentForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_rep = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="姓名", max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label="手机", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(label="管理的系别", queryset=Department.objects.filter(college=1))

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        try:
            CollegeManage.objects.get(username=username)
            raise forms.ValidationError("用户%s已经存在" % username)
        except CollegeManage.DoesNotExist:
            pass
        return username

    def clean(self):
        cleaned_data = super(CreateDepartmentForm, self).clean()
        password = cleaned_data.get("password")
        password_rep = cleaned_data.get("password_rep")
        if password != password_rep:
            self._errors['password_rep'] = self.error_class(["两次输入的密码不一致"])
        return cleaned_data


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label="旧密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_new = forms.CharField(label="新密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_new_rep = forms.CharField(label="确认密码", max_length=128, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password_new = cleaned_data.get("password_new")
        password_rep = cleaned_data.get("password_new_rep")
        if password_new != password_rep:
            self._errors['password_new_rep'] = self.error_class(["两次输入的密码不一致"])
        return cleaned_data
