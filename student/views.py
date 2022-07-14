import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date

from .forms import StudentRegistrationForm, StudentLoginForm
from .models import Student_Registration
from library import messages
from management.models import Books, StudentBooksInfo
from librarian.models import LibrarianRegistration

from . import actions

logging.basicConfig(level=logging.DEBUG, filename='logs/managementDEBUG.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Create your views here.

#student registration navigation
def student_registration_navigation(request):
    form = StudentRegistrationForm
    logging.info('rendering student registration page')
    return render(request, 'student/form.html',{
        'forms':form,
        'title':'student registration'
    })

# student login navigation
def student_login_navigation(request):
    form = StudentLoginForm
    logging.info('rendering student login page')
    return render(request, 'student/form.html',{
        'forms':form,
        'title':'student login'
    })

"""student home page navigation ------->
def student_home_page_navigation(request,student):
    wish = messages.wish()
    student_books = actions.get_student_books(student.student_category)
    librarians = actions.get_librarian_details()
    return render(request, 'student/home.html', {
        'student': student,
        'wishes': wish,
        'books': student_books,
        'id': student.id,
        'librarians': librarians
    })"""

"""student login page navigation ---------->
def student_login_page_navigation(request, msg):
    form = StudentLoginForm()
    return render(request, 'student/form.html', {
        'title': 'student login',
        'forms': form,
        'message': msg
    })"""

# student home navigation
@login_required(login_url='student-login')
def student_home_page(request):
    pass

# student login check
def student_home(request):
    logging.info('rendering student login')
    if request.method=='POST':
        student_email = request.POST['student_email']
        student_password = request.POST['student_password']
        logging.info(f'{student_email} is trying to login')
        try:
            student = Student_Registration.objects.get(student_email=student_email)
            student_count = int(student.student_login_count)

            if student.student_status == 'unblock':
                if student_count > 0 and student_count <= 5:
                    if student_email == student.student_email and student_password == student.student_password:
                        user = authenticate(username=student_email, password=student_password)
                        login(request, user)
                        student.student_login_count = 5
                        student.save()
                        logging.info('successfully logged in')
                        """student_books = actions.get_student_books(student.student_category)
                        wish = messages.wish()
                        librarians = actions.get_librarian_details()
                        return render(request, 'student/home.html', {
                            'student': student,
                            'wishes': wish,
                            'books': student_books,
                            'id': student.id,
                            'librarians': librarians
                        })"""
                        return actions.student_home_page_navigation(request, student)

                    else:
                        student.student_login_count = student.student_login_count - 1
                        student.save()
                        # form = StudentLoginForm()
                        logging.warning('Invalid credentials are entered')
                        """return render(request, 'student/form.html', {
                            'title': 'student login',
                            'forms': form,
                            'message': 'Invalid Credentials...'
                        })"""
                        #return student_login_page_navigation(request, 'Invalid Credentials...')
                        return actions.student_login_page_navigation(request, 'Invalid Credentials...')
                else:
                    # form = StudentLoginForm()
                    logging.warning('login limit exceeded to maximum')
                    """return render(request, 'student/form.html', {
                        'title': 'student login',
                        'forms': form,
                        'message': 'Limited exceeded, Please contact Librarian...'
                    })"""
                    #return student_login_page_navigation(request, 'Limited exceeded, Please contact Librarian...')
                    return actions.student_login_page_navigation(request, 'Limit exceeded, Please contact Librarian...')
            else:
                # form = StudentLoginForm()
                logging.warning('your account blocked')
                """"return render(request, 'student/form.html', {
                    'title': 'student login',
                    'forms': form,
                    'message': 'Your account blocked, Please check with Librarain...'
                })"""
                #return student_login_page_navigation(request, 'Your account blocked, Please check with Librarain...')
                return actions.student_login_page_navigation(request, 'Your account blocked, Please check with Librarian...')
        except:
            return student_login_page_navigation(request, f'{student_email} not registered with us...')
    else:
        logging.debug('get method used')
        return HttpResponse('incorrect method used')

# register new student
def register_new_student(request):
    logging.info('trying to register new student')
    if request.method=='POST':
        student_name = request.POST['student_name']
        student_password = request.POST['student_password']
        student_email = request.POST['student_email']
        student_category = request.POST['student_category']
        today = date.today()
        student_registration_date = today.strftime("%d/%m/%Y")
        try:
            check_email = Student_Registration.objects.filter(student_email=student_email)

            if check_email:
                form = StudentRegistrationForm()
                logging.info(f'{student_email} are in use')
                return render(request, 'student/form.html',{
                    'title':'student registration',
                    'forms':form,
                    'message':'Email already exists,'
                })
            else:
                student = Student_Registration(
                    student_name=student_name,
                    student_email=student_email,
                    student_password=student_password,
                    student_category=student_category,
                    student_registration_date=student_registration_date
                )
                student.save()
                new_user = User.objects.create_user(username=student_email, email=student_email,
                                                    password=student_password)
                new_user.set_password(student_password)
                new_user.save()
                logging.info(f'successfully created new account for email: {student_email}')
                form = StudentLoginForm()
                return render(request, 'student/form.html', {
                    'title': 'student login',
                    'forms': form,
                    'message': 'Successfully created account, login here'
                })
        except:
            student = Student_Registration(
                student_name=student_name,
                student_email=student_email,
                student_password=student_password,
                student_category=student_category,
                student_registration_date=student_registration_date
            )
            student.save()
            new_user = User.objects.create_user(username=student_name, email=student_email, password=student_password)
            new_user.set_password(student_password)
            new_user.save()
            logging.info(f'successfully created new account for email: {student_email}')
            form = StudentLoginForm()
            return render(request, 'student/form.html', {
                'title': 'student login',
                'forms': form,
                'message': 'Successfully created account, login here'
            })
    else:
        logging.info('get method used')
        return HttpResponse('incorrect method used')

# for logout
def logout_view(request):
    logging.info('logging out..')
    logout(request)
    return redirect('/student')

# search for books
@login_required(login_url='student/')
def search_for_books(request, slug):
    if request.method=='POST':
        student = Student_Registration.objects.get(id=slug)
        category = request.POST['select_search']
        text = request.POST['search_input']
        search_result = actions.search_books(category, text, student)
        wish = messages.wish()
        librarians = actions.get_librarian_details()
        book_names, diff_days = actions.student_notifications(student)
        return render(request, 'student/home.html',{
            'student': student,
            'wishes': wish,
            'books': search_result,
            'librarians':librarians,
            'book_names':book_names,
            'diff_days':diff_days
        })
    else:
        return HttpResponse('incorrect method used')

# book details
@login_required(login_url='student/')
def get_book_details(request,slug):
    book = Books.objects.get(id=slug)
    return render(request, 'student/details.html',{
        'book':book,
        'title':'book details'
    })

#get librarians information
@login_required(login_url='student/')
def librarian_details(request):
    librarians = actions.get_librarian_details()
    return render(request, 'student/table.html',{
        'librarians':librarians,
        'title':'librarian details',
    })

# student collections
@login_required(login_url='student/')
def student_collections(request):
    if request.method=='POST':
        student_email = request.POST['email1']
        borrowed_books = StudentBooksInfo.objects.filter(student_email=student_email)
        return render(request, 'student/table.html',{
        'title':'student books',
        'details':borrowed_books
    })
    else:
        return HttpResponse('incorrect method')

#student update navigation
@login_required(login_url='student/')
def student_update_navigation(request):
    if request.method=='POST':
        email = request.POST['email']
        student = Student_Registration.objects.get(student_email=email)
        return render(request, 'student/update.html', {
            'student': student
        })
    else:
        return HttpResponse('incorrect method used')

# update student details
@login_required(login_url='student/')
def update_student(request):
    if request.method=='POST':
        student_id = request.POST['student_id']
        new_student_name = request.POST['student_name']
        new_student_category = request.POST['student_category']

        student = Student_Registration.objects.get(id=int(student_id))
        """student.student_name = new_student_name
        student.student_category = new_student_category
        student.save()"""

        actions.update_student_details(student_id,new_student_name,new_student_category)

        return render(request, 'student/update.html',{
            'student':student,
            'message':'Successfully updated your details'
        })

    else:
        return HttpResponse('incorrect method used')

# preview book details
@login_required(login_url='student/')
def preview_book_details(request):
    if request.method=='POST':
        student_ref = request.POST['student']
        book_ref = request.POST['bookname']

        student = Student_Registration.objects.get(id=student_ref)
        book = Books.objects.get(id=book_ref)
        librarians = actions.get_librarian_details()

        return render(request, 'student/details.html',{
            'title':'borrow book',
            'student':student,
            'book':book,
            'librarians':librarians
        })
    else:
        return HttpResponse('incorrect method')

# borrow book for student
@login_required(login_url='student/')
def borrow_book_for_student(request):
    if request.method=='POST':
        book_id = request.POST['bookid']
        student_email = request.POST['studentid']
        librarian_email = request.POST['librarianid']
        requested_date = date.today()

        student = Student_Registration.objects.get(student_email=student_email)
        book = Books.objects.get(id=int(book_id))
        book_name = book.title
        book_count_check = len(StudentBooksInfo.objects.filter(book_name=book_name, student_email=student.student_email, status='approved'))
        librarians = actions.get_librarian_details()

        if librarian_email==0 or librarian_email=='0':
            return render(request, 'student/details.html',{
                'title':'borrow book',
                'error_message':'Please select Librarian...',
                'student':student,
                'book':book,
                'librarians':librarians
            })
        else:
            if book_count_check>=1:
                return render(request, 'student/details.html', {
                    'title': 'borrow book',
                    'error_message': 'Already requested...',
                    'student': student,
                    'book': book,
                    'librarians': librarians,
                    'msg':'remove'
                })
            else:
                borrow_book = StudentBooksInfo(
                    book_name=book_name,
                    librarian_email=librarian_email,
                    student_email=student_email,
                    status='requested',
                    requested_date=requested_date,
                    approved_date=requested_date,
                    return_date=requested_date,
                    return_approved_date=requested_date
                )
                borrow_book.save()
                student.student_books_count = student.student_books_count-1
                student.save()
                book.available_count = book.available_count-1
                book.save()
                return render(request, 'student/details.html', {
                    'title': 'borrow book',
                    'success_message': 'Successfully sent your book request to respective librarian...',
                    'student': student,
                    'book': book,
                    'librarians': librarians,
                    'msg': 'remove'
                })
    else:
        return HttpResponse('incorrect method')

# student task details
@login_required(login_url='student/')
def task_wise_information(request):
    if request.method=='POST':
        task_id = int(request.POST['taskid'])
        task = StudentBooksInfo.objects.get(id=task_id)
        student_email = task.student_email
        student = Student_Registration.objects.get(student_email=student_email)

        return render(request, 'student/details.html',{
            'title':'book status',
            'task':task,
            'student':student
        })
    else:
        return HttpResponse('incorrect method')

# return book
def return_book(request):
    try:
        if request.method == 'POST':
            task_id = int(request.POST['returnid'])
            student_email = request.POST['studentemail']
            """task = StudentBooksInfo.objects.get(id=task_id)
            task.status = 'return request'
            task.return_date = date.today()
            task.save()"""
            actions.student_return_book(int(task_id))
            borrowed_books = StudentBooksInfo.objects.filter(student_email=student_email)
            return render(request, 'student/table.html', {
                'title': 'student books',
                'details': borrowed_books
            })
        else:
            return HttpResponse('incorrect method')
    except:
        return HttpResponse('something went wrong')






