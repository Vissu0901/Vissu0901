from django.forms import ModelForm, PasswordInput, Textarea, EmailInput
from .models import Student_Registration

class StudentRegistrationForm(ModelForm):
    class Meta:
        model = Student_Registration
        fields = ['student_name','student_email','student_password','student_category']
        labels = {
            'student_name':'Enter your name',
            'student_email':'Enter you email address',
            'student_password':'Enter your password',
            'student_category':''
        }
        widgets = {
            'student_password':PasswordInput(),
            'student_email':EmailInput()
        }

class StudentLoginForm(ModelForm):
    class Meta:
        model = Student_Registration
        fields = ['student_email','student_password']
        labels = {
            'student_email':'Enter email address',
            'student_password':'Enter your password'
        }

        widgets = {
            'student_password':PasswordInput(),
            'student_email':EmailInput()
        }