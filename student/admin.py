from django.contrib import admin
from .models import Student_Registration

# Register your models here.

class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student_name','student_email','student_category','student_login_count')




admin.site.register(Student_Registration, StudentRegistrationAdmin)
