from django.forms import ModelForm, PasswordInput, Textarea
from management.models import Management,Books

class ManagementForm(ModelForm):
    class Meta:
        model = Management
        fields = ['username','password']
        labels = {
            "username":"Username",
            "password":"Password"
        }
        widgets = {
            'password':PasswordInput()
        }

class AddNewBookForm(ModelForm):
    class Meta:
        model = Books
        fields = ['title','author','category','description','available_count','location']
        labels = {
            'title':'Enter book title',
            'author':'Enter book author name',
            'category':'',
            'description':'Enter book description',
            'available_count':'Enter no.of books ',
            'location':'Book Location'
        }
        widgets = {
            'description': Textarea()
        }

