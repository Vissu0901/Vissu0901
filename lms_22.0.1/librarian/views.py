from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from datetime import date,timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LibrarianLoginForm, LibrarianRegistrationForm
from .models import LibrarianRegistration
from library import messages
from management.models import Books, StudentBooksInfo
from management import actions as m_actions
from . import actions

from student.models import Student_Registration

logging.basicConfig(level=logging.DEBUG, filename='logs/managementDEBUG.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

securtity_code = '1998'

# Create your views here.

# librarian login form navigation
def librarian_login_navigation(request):
    try:
        logging.info('navigating to librarian login page')
        form = LibrarianLoginForm()
        return render(request, 'librarian/form.html', {
            'title': 'librarian login',
            'forms': form
        })
    except:
        logging.debug('error occured..')
        return HttpResponse('something went wrong')

# librarian registration form navigation
def librarian_registration_navigation(request):
    try:
        logging.info('navigating to librarian registration page')
        form = LibrarianRegistrationForm()
        return render(request, 'librarian/form.html', {
            'title': 'librarian registration',
            'forms': form
        })
    except:
        logging.debug('error occured..')
        return HttpResponse('something went wrong')

# librarian registration
def register_librarian(request):
    logging.info('trying to register new librarian')
    if request.method=='POST':
        librarian_name = request.POST['librarian_name']
        librarian_password = request.POST['librarian_password']
        librarian_email = request.POST['librarian_email']
        librarian_code = request.POST['librarian_security_code']
        librarian_shift = request.POST['librarian_shift']

        try:
            librarians = LibrarianRegistration.objects.get(librarian_email=librarian_email)

            if librarians:
                logging.warning(f'{librarian_email} already exists, trying to create new')
                form = LibrarianRegistrationForm()
                return render(request, 'librarian/form.html', {
                    'title': 'librarian registration',
                    'forms': form,
                    'message': 'Email address already exists..'
                })
            else:
                if librarian_code == securtity_code:
                    today = date.today()
                    librarian = LibrarianRegistration(
                        librarian_name=librarian_name,
                        librarian_password=librarian_password,
                        librarian_email=librarian_email,
                        librarian_shift=librarian_shift,
                        librarian_registration_date=today.strftime("%d/%m/%Y"),
                        librarian_security_code=securtity_code
                    )
                    librarian.save()
                    new_user = User.objects.create_user(username=librarian_email, email=librarian_email,
                                                        password=librarian_password)
                    new_user.set_password(librarian_password)
                    new_user.save()
                    logging.info(f'successfully created librarian with username: {librarian_email}')
                    form = LibrarianLoginForm()
                    return render(request, 'librarian/form.html', {
                        'title': 'librarian login',
                        'forms': form,
                        'message': 'Successfully created account, login here..'
                    })
                else:
                    logging.warning('incorrect security code entered...')
                    form = LibrarianRegistrationForm()
                    return render(request, 'librarian/form.html', {
                        'title': 'librarian registration',
                        'forms': form,
                        'message': 'Incorrect security code..'
                    })

        except:
            if librarian_code == securtity_code:
                today = date.today()
                librarian = LibrarianRegistration(
                    librarian_name=librarian_name,
                    librarian_password=librarian_password,
                    librarian_email=librarian_email,
                    librarian_shift=librarian_shift,
                    librarian_registration_date=today.strftime("%d/%m/%Y"),
                    librarian_security_code=securtity_code
                )
                librarian.save()
                new_user = User.objects.create_user(username=librarian_email, email=librarian_email,
                                                    password=librarian_password)
                new_user.set_password(librarian_password)
                new_user.save()
                logging.info(f'successfully created new librarian with username: {librarian_email}')
                form = LibrarianLoginForm()
                return render(request, 'librarian/form.html', {
                    'title': 'librarian login',
                    'forms': form,
                    'message': 'Successfully created account, login here..'
                })
            else:
                logging.warning('incorrect security code entered...')
                form = LibrarianRegistrationForm()
                return render(request, 'librarian/form.html', {
                    'title': 'librarian registration',
                    'forms': form,
                    'message': 'Incorrect security code..'
                })

    else:
        logging.debug('incorrect method call..')
        return HttpResponse('incorrect method')

# librarian login
def librarian_home(request):
    logging.info('trying to login into librarian home page')
    if request.method=='POST':

        librarian_email = request.POST['librarian_email']
        librarian_password = request.POST['librarian_password']
        #try:
        librarian = LibrarianRegistration.objects.get(librarian_email=librarian_email)
        if librarian.librarian_login_count>0 and librarian.librarian_login_count<=5:
            if librarian:
                if librarian.librarian_email==librarian_email and librarian.librarian_password==librarian_password:
                    user = authenticate(username=librarian_email, password=librarian_password)
                    login(request,user)
                    librarian.librarian_login_count=5
                    librarian.save()
                    wishes = messages.wish()
                    books = Books.objects.all()
                    logging.info('successfully loaded librarian home page...')
                    return render(request, 'librarian/home.html',{
                            'librarian':librarian,
                            'wishes':wishes,
                            'books':books
                        })
                else:
                    librarian.librarian_login_count = librarian.librarian_login_count-1
                    librarian.save()
                    logging.warning('invalid credentials are provided by user...')
                    form = LibrarianLoginForm()
                    return render(request, 'librarian/form.html',{
                            'title':'librarian login',
                            'forms':form,
                            'message':'Invalid credentials entered... else1'
                        })
            else:
                librarian.librarian_login_count = librarian.librarian_login_count - 1
                librarian.save()
                logging.warning('invalid credentials are entered by user...')
                form = LibrarianLoginForm()
                return render(request, 'librarian/form.html', {
                        'title': 'librarian login',
                        'forms': form,
                        'message': 'Invalid credentials entered... else2'
                    })
        else:
            logging.warning('limit exceeded to maximum...')
            form = LibrarianLoginForm()
            return render(request, 'librarian/form.html', {
                    'title': 'librarian login',
                    'forms': form,
                    'message': 'Limit exceeded to maximum contact Management team..'
                })
        """except:
            librarian.librarian_login_count = librarian.librarian_login_count - 1
            librarian.save()
            logging.warning('invalid credentials are entered...')
            form = LibrarianLoginForm()
            return render(request, 'librarian/form.html', {
                'title': 'librarian login',
                'forms': form,
                'message': 'Invalid credentials entered...except'
            })"""
    else:
        logging.debug('incorrect method used...')
        return HttpResponse('something went wrong, try again')
# logout
def logout_view(request):
    logging.info('logging out..')
    logout(request)
    return redirect('/librarian')

# book details
@login_required(login_url='librarian/')
def book_details(request,slug):
    book = Books.objects.get(id=slug)
    return render(request, 'librarian/details.html',{
        'book':book,
        'title':'book details'
    })

# search for books
@login_required(login_url='librarian/')
def search_for_books(request, slug):
    if request.method=='POST':
        librarian = LibrarianRegistration.objects.get(id=slug)
        category = request.POST['select_search']
        text = request.POST['search_input']
        search_result = m_actions.search_book(category,text)
        wish = messages.wish()
        return render(request, 'librarian/home.html', {
            'librarian': librarian,
            'wishes': wish,
            'books': search_result
        })
    else:
        return HttpResponse('incorrect method')

# your task
@login_required(login_url='librarian/')
def librarian_pending_tasks(request):
    if request.method=='POST':
        librarian_email = request.POST['librarianid']
        tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)
        librarian = LibrarianRegistration.objects.get(librarian_email=librarian_email)
        return render(request, 'librarian/table.html',{
            'title':'tasks',
            'tasks':tasks,
            'librarian':librarian
        })
    else:
        return HttpResponse('incorrect method')



# approve student request
@login_required(login_url='librarian/')
def librarian_approve_request(request):
    if request.method=='POST':
        task_id = int(request.POST['approve-task'])
        librarian_email = request.POST['librarian-approve']

        task = StudentBooksInfo.objects.get(id=task_id)
        task.status = 'approved'
        task.approved_date = date.today()
        task.return_date = date.today() + timedelta(days=15)
        task.return_approved_date = date.today() + timedelta(days=15)
        task.save()

        tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)
        return render(request, 'librarian/table.html', {
            'title': 'tasks',
            'tasks': tasks
        })
    else:
        return HttpResponse('incorrect method')

# task wise information
@login_required(login_url='librarian/')
def task_wise_details(request):
    if request.method=='POST':
        task_id = int(request.POST['taskid'])
        task = StudentBooksInfo.objects.get(id=task_id)
        librarian_email = task.librarian_email
        librarian = LibrarianRegistration.objects.get(librarian_email=librarian_email)
        student_email = task.student_email
        student = Student_Registration.objects.get(student_email=student_email)
        book_name = task.book_name
        book = Books.objects.get(title=book_name)
        return render(request, 'librarian/details.html',{
            'title':'librarian task',
            'librarian':librarian,
            'task':task,
            'student':student,
            'book':book
        })
    else:
        return HttpResponse('incorrect method')




#reject request
@login_required(login_url='librarian/')
def reject_student_request(request):
    if request.method=='POST':
        task_id = int(request.POST['reject-task'])
        task = StudentBooksInfo.objects.get(id=task_id)
        task.status = 'rejected'
        task.save()

        student_email = task.student_email
        student = Student_Registration.objects.get(student_email=student_email)
        student.student_books_count = student.student_books_count+1
        student.save()

        book_name = task.book_name
        book = Books.objects.get(title=book_name)
        book.available_count = book.available_count+1
        book.save()

        librarian_email = task.librarian_email
        tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)
        return render(request, 'librarian/table.html',{
            'title': 'tasks',
            'tasks': tasks
        })
    else:
        return HttpResponse('incorrect method')

# student information in table form
@login_required(login_url='librarian/')
def student_information_table(request):
    if request.method=='POST':
        students = Student_Registration.objects.all()
        return render(request, 'librarian/table.html',{
            'title':'students information',
            'students':students
        })
    else:
        return HttpResponse('incorrect method')

# librarian return accept
@login_required(login_url='librarian/')
def return_accept(request):
    if request.method=='POST':
        task_id = int(request.POST['librarian-return-request'])
        librarian_email = request.POST['return-librarian']

        task = StudentBooksInfo.objects.get(id=task_id)
        task.status = 'return accepted'
        task.return_approved_date = date.today()
        task.save()

        book_name = task.book_name
        book = Books.objects.get(title=book_name)
        book.available_count = book.available_count+1
        book.save()

        student_email = task.student_email
        student = Student_Registration.objects.get(student_email=student_email)
        student.student_books_count = student.student_books_count+1
        student.save()

        librarian_tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)
        return render(request, 'librarian/table.html',{
            'title': 'tasks',
            'tasks': librarian_tasks
        })
    else:
        return HttpResponse('incorrect method')

# filter page navigation
@login_required(login_url='librarian/')
def filter_navigation(request):
    if request.method=='POST':
        librarian_email = request.POST['librarianid']
        book_names_filter, student_emails_filter, status_filter = actions.librarian_list_filter(librarian_email)
        librarian = LibrarianRegistration.objects.get(librarian_email=librarian_email)
        tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email).order_by('-status')
        return render(request, 'librarian/table.html', {
            'title': 'tasks-filter',
            'book_names_filter': book_names_filter,
            'student_emails_filter': student_emails_filter,
            'status_filter': status_filter,
            'librarian': librarian,
            'tasks':tasks
        })
    else:
        return HttpResponse('incorrect method')

# filtering librarian tasks
@login_required(login_url='librarian/')
def filtering_tasks(request):
    if request.method=='POST':
        librarian_id = int(request.POST['librarian'])
        book_name = request.POST['book-name']
        student_email = request.POST['student-email']
        status = request.POST['status']

        librarian = LibrarianRegistration.objects.get(id=librarian_id)
        librarian_email = librarian.librarian_email

        if book_name=='0' and student_email=='0' and status=='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email = librarian_email).order_by('-status')
        elif book_name!='0' and student_email=='0' and status=='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, book_name=book_name)
        elif book_name=='0' and student_email!='0' and status=='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, student_email=student_email)
        elif book_name=='0' and student_email=='0' and status!='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, status=status)
        elif book_name!='0' and student_email!='0' and status=='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, book_name=book_name, student_email=student_email)
        elif book_name!='0' and student_email=='0' and status!='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, book_name=book_name, status=status)
        elif book_name=='0' and student_email!='0' and status!='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email, student_email=student_email, status=status)
        elif book_name!='0' and student_email!='0' and status!='0':
            tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email,book_name=book_name, student_email=student_email, status=status)
        else:
           tasks = None

        book_names_filter, student_emails_filter, status_filter = actions.librarian_list_filter(librarian_email)
        return render(request, 'librarian/table.html', {
            'title': 'tasks-filter',
            'book_names_filter': book_names_filter,
            'student_emails_filter': student_emails_filter,
            'status_filter': status_filter,
            'librarian': librarian,
            'tasks': tasks
        })

    else:
        return HttpResponse('incorrect method')