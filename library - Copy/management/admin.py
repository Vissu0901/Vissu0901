from django.contrib import admin
from .models import Management, Books, StudentBooksInfo

# Register your models here.

class ManagementAdmin(admin.ModelAdmin):
    list_display = ('username', 'count')

class BooksAdmin(admin.ModelAdmin):
    list_display = ('title','author','category','available_count')

class StudentBooksInfoAdmin(admin.ModelAdmin):
    list_display = ('book_name', 'librarian_email', 'student_email', 'status')

admin.site.register(Management, ManagementAdmin)
admin.site.register(Books,BooksAdmin)
admin.site.register(StudentBooksInfo, StudentBooksInfoAdmin)