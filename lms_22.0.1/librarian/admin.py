from django.contrib import admin
from .models import LibrarianRegistration

# Register your models here.
class LibrarianRegistrationAdmin(admin.ModelAdmin):
    list_display = ('librarian_name','librarian_email','librarian_shift','librarian_login_count')

admin.site.register(LibrarianRegistration, LibrarianRegistrationAdmin)