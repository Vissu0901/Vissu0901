from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date
import logging

from . import actions
from library import messages
from .forms import ManagementForm, AddNewBookForm
from .models import Management, Books, StudentBooksInfo
from student.models import Student_Registration
from librarian.models import LibrarianRegistration

logging.basicConfig(level=logging.DEBUG, filename='logs/managementDEBUG.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# Create your views here.

# mode change in login page
def mode_change_loginPage(request):
    if request.method=='POST':
        mode = request.POST['mode1']
        management = Management.objects.all()[0]
        management.mode=mode
        management.save()
        return HttpResponseRedirect('/management')
    else:
        return HttpResponse('incorrect method')

# navigate to login page
def navigate_to_login_page(request, msg, user):
    form = ManagementForm()
    dbuser = Management.objects.all()[0]
    return render(request, 'management/managementLogin.html', {
        'title': 'management login',
        'forms': form,
        'msg': msg,
        'mode': dbuser.mode,
        'user':user
    })

# Login page
class ManagementView(View):
    
    def get(self, request):
        logging.info(' trying to load login page for Management login')
        form = ManagementForm()
        management_mode = Management.objects.all()[0]
        logging.info('Successfully loaded...')
        return render(request, 'management/managementLogin.html',{
            'forms':form,
            'title':'management login',
            'msg':'none',
            'mode':management_mode.mode
        })

# Login check
class ManagementLoginView(FormView):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        try:
            dbuser = Management.objects.get(username=username)
            logging.info(f'{username} trying to login...')
            count = int(dbuser.count)
            logging.info('Checking login limit for Management login')
            if count >= 1 and count <= 5:
                if username == dbuser.username and password == dbuser.password:
                    user = authenticate(username=username, password=password)
                    logging.info('Authenticating Management user')
                    if user is not None:
                        login(request, user)
                        logging.info('Checking login....')
                        dbuser.count = 5
                        dbuser.save()
                        logging.info('Done, Successfully logged in...')
                        # return redirect('/management/home')
                        return render(request, 'management/loading_page.html', {
                            'username': user,
                            'formtype': 'user-login'
                        })
                    else:
                        new_user = User.objects.create_user(username=username, email=username + '@mail.com',
                                                            password=password)
                        new_user.set_password(password)
                        new_user.save()
                        login(request, new_user)
                        logging.info('Checking login....')
                        dbuser.count = 5
                        dbuser.save()
                        logging.info('Done, Successfully logged in...')
                        # return redirect('/management/home')
                        return render(request, 'management/loading_page.html', {
                            'username': new_user,
                            'formtype': 'user-login'
                        })
                else:
                    logging.warning(f'{username} entered credentials are not matching with db user...')
                    dbuser.count = dbuser.count - 1
                    dbuser.save()
                    return navigate_to_login_page(request, 'Enter valid Password', dbuser)
            else:
                logging.warning(f'{username} exceeded limit of incorrect credentials...')
                return navigate_to_login_page(request, 'Account locked, Please contact DB admin', dbuser)
        except:
            logging.warning(f'{username} entered credentials are not matching for authentication...')
            return navigate_to_login_page(request, 'Enter valid Username', 'none')

# loading page view for home page
@login_required(login_url='/management')
def loading_page(request):
    if request.method=='POST':
        username = str(request.POST['username'])
        print(username)
        user = Management.objects.get(username=username)
        wish = messages.wish()
        books = Books.objects.all()
        return render(request, 'management/managementHome.html',{
            'wishes': wish,
            'books': books,
            'mode': user.mode,
            'user':user
        })
    else:
        return HttpResponse('something went wrong')


# change mode in management home
@login_required(login_url='/management')
def loading_change_mode_management_home(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        username = request.POST['username']
        user = Management.objects.get(username=username)
        return render(request, 'management/loading_page.html', {
            'username': user,
            'mode':mode,
            'formtype': 'change-mode-home'
        })

    else:
        return HttpResponse('something went wrong')

# change mode in home
@login_required(login_url='/management')
def change_mode_in_home(request):
    if request.method=='POST':
        username = request.POST['username']
        mode = request.POST['mode']
        user = Management.objects.get(username=username)
        user.mode = mode
        user.save()
        return render(request, 'management/loading_page.html', {
            'username': user,
            'formtype': 'user-login'
        })
    else:
        return HttpResponse('something went wrong')


#Add new book
@login_required(login_url='/management')
def add_new_book_navigation(request):
    try:
        form = AddNewBookForm()
        logging.info('Navigating to Add new book page')
        return render(request, 'management/updateAddM.html',{
        'forms':form,
        'title':'add new book',
        'message':''
        })
    except:
        logging.debug('error occurred at line 113...')
        return HttpResponse('something went wrong')

#Add book to database
@login_required(login_url='/management')
def add_new_book(request):

    if request.method=='POST':
        book_title = request.POST['title']
        book_author = request.POST['author']
        book_category = request.POST['category']
        book_description = request.POST['description']
        book_count = request.POST['available_count']
        logging.info(f'book details entered: book name: {book_title}')
        today = date.today()
        book_upload_date = today.strftime("%d/%m/%Y")
        try:
            bookname = Books.objects.get(title=book_title)
            if bookname:
                logging.warning(f'{book_title} :book already exists in database...')
                form = AddNewBookForm()
                logging.info('Navigating to Add new book page')
                return render(request, 'management/updateAddM.html', {
                    'forms': form,
                    'title': 'add new book',
                    'message': 'Book name already exists, Please try again'
                })
        except:
            logging.info(f'trying to store {book_title} details in database...')
            book = Books(
                title=book_title,
                author=book_author,
                category=book_category,
                description=book_description,
                available_count=book_count,
                upload_date=book_upload_date
            )
            book.save()
            logging.info(f'{book_title}: Successfully stored in database')
            form = AddNewBookForm()
            return render(request, 'management/updateAddM.html', {
                'forms': form,
                'title': 'add new book',
                'message': 'Successfully added new book'
            })

    else:
        logging.warning('tried get method instead post...')
        return HttpResponse('incorrect method type')

#search for books
@login_required(login_url='/management')
def search_for_books(request):
    if request.method=='GET':
        try:
            username = request.GET['search_username']
            category = request.GET['select_search']
            search_text = request.GET['search_text']
            books = actions.search_book(category, search_text)
            wish = messages.wish()
            user = Management.objects.get(username=username)
            logging.info('User trying to search of books...')
            return render(request, 'management/ManagementHome.html', {
                'wishes': wish,
                'books': books,
                'mode': user.mode,
                'user':user
        })
        except:
            logging.debug('error occurred at line 170...')
            return HttpResponse('something went wrong')
    else:
        return HttpResponse('incorrect method sent through form')

# for logout
def logout_view(request):
    try:
        logging.info('logging out..')
        logout(request)
        logging.info('User logged out from portal...')
        return redirect('/management')
    except:
        logging.debug('error occured at line 195...')
        return HttpResponse('something went wrong')

# delete book
@login_required(login_url='/management')
def delete_book(request):
    if request.method=='POST':
        username = request.POST['delete_username']
        book_id = request.POST['delete_book_id']
        user = Management.objects.get(username=username)
        book = Books.objects.get(id=int(book_id))
        book.delete()
        return render(request, 'management/loading_page.html',{
            'formtype':'user-login',
            'user':user
        })
    else:
        return HttpResponse('incorrect method used')

# update book information
@login_required(login_url='/management')
def update_book_navigation(request, slug):
    #try:
    logging.info('trying to update book details...')
    book = Books.objects.get(id=slug)
    options = {
        'bachelor-of-arts': 'Bachelor of Arts',
        'bba/bms': 'BBA/BMS',
        'btech-bachelor-of-engg./tech': 'Bachelor of Engg./Tech',
        'bachelor-of-commerce': 'Bachelor of Commerce',
        'bachelor-of-law': 'Bachelor of Law',
        'mbbs-bachelor-of-medicine': 'Bachelor of Medicine',
        'bachelor-of-science': 'Bachelor of Science',
        'intermediate': 'Intermediate',
        'ssc-10th-standard': '10th standard'
    }
    return render(request, 'management/updateAddM.html', {
        'title': 'update book details',
        'book': book,
        'options': options,
        'message':''
    })
    """except:
        logging.debug('error occured at line 235...')
        return HttpResponse('something went wrong')"""

# update book information
@login_required(login_url='/management')
def update_book_information(request, slug):
    if request.method=='POST':
        book_name = request.POST['update_title']
        book_author = request.POST['update_author']
        book_category = request.POST['update_category']
        book_description = request.POST['update_description']
        book_available_count = request.POST['update_count']
        book_location = request.POST['update_location']

        try:
            book = Books.objects.get(id=slug)
            book.title = book_name
            book.author = book_author
            if book_category==0 or book_category=='0':
                book.category = book.category
            else:
                book.category = book_category
            book.description = book_description
            book.available_count = book_available_count
            book.location = book_location
            book.save()
            logging.info(f'{book_name}: updated details in db...')
            options = {
                'bachelor-of-arts': 'Bachelor of Arts',
                'bba/bms': 'BBA/BMS',
                'btech-bachlor-of-engg./tech': 'Bachelor of Engg./Tech',
                'bachelor-of-commerce': 'Bachelor of Commerce',
                'bachelor-of-law': 'Bachelor of Law',
                'mbbs-bachelor-of-medicine': 'Bachelor of Medicine',
                'bachelor-of-science': 'Bachelor of Science',
                'intermediate': 'Intermediate',
                'ssc-10th-standard': '10th standard'
            }
            return render(request, 'management/updateAddM.html',{
                'title':'update book details',
                'book':book,
                'options':options,
                'message':'Successfully updated book details...'
            })
        except:
            logging.warning('incorrect details provided by user...')
            return render(request, 'management/updateAddM.html', {
                'title': 'update book details',
                'book': book,
                'options': options,
                'message':'incorrect information entered...'
            })
    else:
        logging.warning('get method used instead post...')
        return HttpResponse('incorrect method used')

# get book information navigation
@login_required(login_url='/management')
def get_book_details(request, slug):
    try:
        logging.info('User trying see book details...')
        book = Books.objects.get(id=slug)
        return render(request, 'management/detailsM.html',{
            'title':'book details',
            'book':book
        })
    except:
        logging.debug('error occured at line 310...')
        return HttpResponse('something went wrong')

# loading student details
@login_required(login_url='/management')
def loading_student_details(request):
    if request.method=='POST':
        username = request.POST['username_student_details']
        user = Management.objects.get(username=username)
        return render(request, 'management/loading_page.html', {
            'user': user,
            'formtype': 'student-details'
        })
    else:
        return HttpResponse('something went wrong')

# student details
@login_required(login_url='/management')
def get_student_details(request):
    """try:
        students = Student_Registration.objects.all()
        logging.info('trying to display list of students...')
        return render(request, 'management/table.html', {
            'title': 'student details',
            'details': students,
            'student_names':actions.student_and_librarian_list('student names'),
            'student_emails':actions.student_and_librarian_list('student emails'),
            'student_categories':actions.student_and_librarian_list('student categories'),
            'student_books_count':actions.student_and_librarian_list('student books count'),
            'student_status':actions.student_and_librarian_list('student status')
        })
    except:
        logging.debug('error occured at line 303..')
        return HttpResponse('something went wrong')"""
    if request.method=='POST':
        username = request.POST['username']
        user = Management.objects.get(username=username)
        students = Student_Registration.objects.all()
        return render(request, 'management/tableM.html', {
            'title': 'student details',
            'details': students,
            'user':user,
            'student_names': actions.student_and_librarian_list('student names'),
            'student_emails': actions.student_and_librarian_list('student emails'),
            'student_categories': actions.student_and_librarian_list('student categories'),
            'student_books_count': actions.student_and_librarian_list('student books count'),
            'student_status': actions.student_and_librarian_list('student status')
        })
    else:
        return HttpResponse('something went wrong')

# students filtering
def students_filtering(request):
    if request.method=='GET':
        student_name = request.GET['student-name']
        student_email = request.GET['student-email']
        student_category = request.GET['student-category']
        student_books_count = request.GET['student-books-count']
        student_status = request.GET['student-status']
        username = request.GET['m_table_username']

        user = Management.objects.get(username=username)
        students = actions.students_filter(student_name, student_email, student_category, student_books_count, student_status)

        return render(request, 'management/tableM.html', {
            'title': 'student details',
            'details': students,
            'student_names': actions.student_and_librarian_list('student names'),
            'student_emails': actions.student_and_librarian_list('student emails'),
            'student_categories': actions.student_and_librarian_list('student categories'),
            'student_books_count': actions.student_and_librarian_list('student books count'),
            'student_status': actions.student_and_librarian_list('student status'),
            'user':user
        })

    else:
        return HttpResponse('incorrect method')


# student details - student wise
@login_required(login_url='/management')
def get_student_wise_information(request, slug):
    #try:
    student = Student_Registration.objects.get(id=slug)
    logging.info(f'{student.student_name}: details are being displayed...')
    return render(request, 'management/detailsM.html', {
        'title': 'student details',
        'student': student
    })
    """except:
        logging.debug('error occurred at line 317..')
        return HttpResponse('something went wrong')"""

# loading librarian details
@login_required(login_url='/management')
def loading_librarian_details(request):
    if request.method=='POST':
        username = request.POST['username_librarian_details']
        user = Management.objects.get(username=username)
        return render(request, 'management/loading_page.html',{
            'user':user,
            'formtype':'librarian-details'
        })
    else:
        return HttpResponse('something went wrong')

# librarin details
@login_required(login_url='/management')
def get_librarian_details(request):
    """try:
        librarians = LibrarianRegistration.objects.all()
        logging.info('trying to display list of librarians...')
        return render(request, 'management/table.html', {
            'title': 'librarian details',
            'details': librarians,
            'librarian_names': actions.student_and_librarian_list('librarian names'),
            'librarian_emails': actions.student_and_librarian_list('librarian emails'),
            'librarian_shifts': actions.student_and_librarian_list('librarian shifts')
        })
    except:
        logging.debug('error occurred at line 331...')
        return HttpResponse('something went wrong')"""
    if request.method=='POST':
        username = request.POST['username']
        user = Management.objects.get(username=username)
        librarians = LibrarianRegistration.objects.all()
        return render(request, 'management/tableM.html',{
            'title': 'librarian details',
            'details': librarians,
            'librarian_names': actions.student_and_librarian_list('librarian names'),
            'librarian_emails': actions.student_and_librarian_list('librarian emails'),
            'librarian_shifts': actions.student_and_librarian_list('librarian shifts'),
            'user':user
        })
    else:
        return HttpResponse('something went wrong')

# loading back to home of librarians/students
@login_required(login_url='/manangement')
def loading_back_to_home_staff(request):
    if request.method=='POST':
        username = request.POST['username_table']
        user = Management.objects.get(username=username)
        return render(request, 'management/loading_page.html',{
            'user': user,
            'formtype': 'user-login'
        })
    else:
        return HttpResponse('something went wrong')

# librarian filtering
@login_required(login_url='/management')
def librarians_filtering(request):
    if request.method=='GET':
        librarian_name = str(request.GET['librarian-name'])
        librarian_email = str(request.GET['librarian-email'])
        librarian_shift = str(request.GET['librarian-shift'])
        username = request.GET['m_table_username']

        user = Management.objects.get(username=username)
        librarians = actions.librarians_filter(librarian_name,librarian_email,librarian_shift)
        return render(request, 'management/tableM.html', {
            'title': 'librarian details',
            'details': librarians,
            'librarian_names': actions.student_and_librarian_list('librarian names'),
            'librarian_emails': actions.student_and_librarian_list('librarian emails'),
            'librarian_shifts': actions.student_and_librarian_list('librarian shifts'),
            'user':user
        })

# librarian details - librarian wise
@login_required(login_url='/management')
def get_librarian_wise_information(request, slug):
    try:
        librarian = LibrarianRegistration.objects.get(id=slug)
        librarian_email = librarian.librarian_email
        tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)
        pending_tasks = actions.pending_tasks_count(tasks)
        logging.info(f'{librarian.librarian_name}: being displayed...')
        user = Management.objects.all()[0]
        return render(request, 'management/detailsM.html', {
            'title': 'librarian details',
            'librarian': librarian,
            'pending_tasks':pending_tasks,
            'user':user
        })
    except:
        logging.debug('error occurred at line 345...')
        return HttpResponse('something went wrong...')



