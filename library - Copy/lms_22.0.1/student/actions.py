from management.models import Books, StudentBooksInfo
from librarian.models import LibrarianRegistration
from library import messages
from django.shortcuts import render
from .forms import StudentLoginForm
from .models import Student_Registration

from datetime import datetime, date, timedelta

# load books based on students category
def get_student_books(student_category):
    books = Books.objects.all()
    student_books = []
    for book in books:
        if book.category==student_category:
            student_books.append(book)
    return student_books

# search books student
def search_books(search_type, search_input, student):
    total_books = Books.objects.all()
    category = student.student_category
    student_books = []
    final_books=[]
    for book in total_books:
        if category==book.category:
            student_books.append(book)

    if search_type == 'title':
        for book in student_books:
            if str(search_input).lower() in str(book.title).lower():
                final_books.append(book)
    elif search_type == 'author':
        for book in student_books:
            if str(search_input).lower() in str(book.author).lower():
                final_books.append(book)
    else:
        return None

    return final_books

# librarian details
def get_librarian_details():
    now = datetime.now()
    total_librarians = None
    time_now = int(now.strftime("%H"))
    if time_now < 24 and time_now >= 14:
        total_librarians = LibrarianRegistration.objects.filter(librarian_shift='afternoon')
    elif time_now < 14 and time_now > 6:
        total_librarians = LibrarianRegistration.objects.filter(librarian_shift='morning')

    return total_librarians

# student notifications
def student_notifications(student):
    book_names = []
    diff_days = []
    try:
        tasks = StudentBooksInfo.objects.filter(student_email=student.student_email, status='approved')
        for task in tasks:
            day_today = date.today()
            diff = task.return_date - day_today
            if diff.days <= 5:
                book_names.append(task.book_name)
                diff_days.append(diff.days)

        return book_names, diff_days
    except:
        book_names = None
        diff_days = None
        return book_names, diff_days

# student home page navigation
def student_home_page_navigation(request,student):
    wish = messages.wish()
    student_books = get_student_books(student.student_category)
    librarians = get_librarian_details()
    return render(request, 'student/home.html', {
        'student': student,
        'wishes': wish,
        'books': student_books,
        'id': student.id,
        'librarians': librarians
    })

# student login page navigation
def student_login_page_navigation(request, msg):
    form = StudentLoginForm()
    return render(request, 'student/form.html', {
        'title': 'student login',
        'forms': form,
        'message': msg
    })

# student return book request
def student_return_book(task_id):
    task = StudentBooksInfo.objects.get(id=task_id)
    task.status = 'return request'
    task.return_date = date.today()
    task.save()

# update student details
def update_student_details(student_id, new_student_name, new_student_category):
    student = Student_Registration.objects.get(id=int(student_id))
    student.student_name = new_student_name
    student.student_category = new_student_category
    student.save()
