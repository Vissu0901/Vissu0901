from django.forms import ModelForm, PasswordInput, EmailInput
from .models import LibrarianRegistration

class LibrarianRegistrationForm(ModelForm):
    class Meta:
        model = LibrarianRegistration
        fields = ['librarian_name','librarian_password','librarian_email','librarian_security_code','librarian_shift',]
        labels = {
            'librarian_name':'Enter your name',
            'librarian_password':'Enter your password',
            'librarian_email':'Enter your email address',
            'librarian_security_code':'Enter your security code',
            'librarian_shift':''
        }
        widgets = {
            'librarian_password':PasswordInput(),
            'librarian_email':EmailInput()
        }

class LibrarianLoginForm(ModelForm):
    class Meta:
        model = LibrarianRegistration
        fields = ['librarian_email','librarian_password']
        labels = {
            'librarian_email':'Enter your email address',
            'librarian_password':'Enter your password'
        }
        widgets = {
            'librarian_email':EmailInput(),
            'librarian_password':PasswordInput()
        }