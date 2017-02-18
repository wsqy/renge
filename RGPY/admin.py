from django.contrib import admin
from RGPY.models import College, Department, Banji, Student, CollegeManage

# Register your models here.
admin.site.register(College)
admin.site.register(Department)
admin.site.register(Banji)
admin.site.register(Student)
admin.site.register(CollegeManage)
