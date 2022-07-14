from .models import Books
from student.models import Student_Registration
from librarian.models import LibrarianRegistration


#management books search
def search_book(search_type, search_input):
    books = Books.objects.all()
    final_books = []
    if str(search_type).lower()=='title':
        for book in books:
            if str(search_input).lower() in str(book.title).lower():
                final_books.append(book)

    elif str(search_type).lower()=='author':
        for book in books:
            if str(search_input).lower() in str(book.author).lower():
                final_books.append(book)
    elif str(search_type).lower()=='category':
        for book in books:
            if str(search_input).lower() in str(book.category).lower():
                final_books.append(book)
    elif str(search_type)=='0':

        if len(search_input)==0:
            final_books = Books.objects.all()
        else:
            books = Books.objects.all()
            for book in books:
                search_string = str(book.title).lower()+str(book.author).lower()+str(book.category).lower()
                search_text = str(search_input).lower()
                if search_text in search_string:
                    final_books.append(book)
    else:
        return None
    return final_books


# librarian pending tasks count
def pending_tasks_count(librarian_tasks):
    tasks_list = []
    for task in librarian_tasks:
        if task.status=='requested' or task.status=='return request':
            tasks_list.append(task)

    return len(tasks_list)

# students filter
def students_filter(student_name, student_email, category, books_count, status):

    if student_name=='none' and student_email=='none' and category=='none' and books_count=='none' and status=='none':
        students = Student_Registration.objects.all()
        return students
    elif student_name!='none' and student_email!='none' and category!='none' and books_count!='none' and status!='none':
        students = Student_Registration.objects.filter(student_name=student_name,
                                                       student_email=student_email,
                                                       student_category = category,
                                                       student_books_count = books_count,
                                                       student_status = status)
        return students
    elif student_name=='none' and student_email=='none' and category=='none' and books_count!='none' and status=='none':
        students = Student_Registration.objects.filter(student_books_count = books_count)
        return students
    else:
        items = [student_name, student_email, category, books_count, status]
        search_items = []

        for item in items:
            if item=='none':
                pass
            else:
                search_items.append(item)

        students = Student_Registration.objects.all()
        searching_students = []

        search_text = ''
        for i in search_items:
            search_text = search_text + str(i)

        for student in students:
            student_text1 = str(student.student_name) + str(student.student_email) + str(student.student_category) + str(
                student.student_books_count) + str(student.student_status)

            student_text2 = str(student.student_name)+str(student.student_category)+str(student.student_books_count)+str(student.student_status)+str(student.student_email)
            student_text3 = str(student.student_name)+str(student.student_email)+str(student.student_books_count)+str(student.student_status)+str(student.student_category)
            student_text4 = str(student.student_name)+str(student.student_email)+str(student.student_category)+str(student.student_status)+str(student.student_books_count)
            student_text5 = str(student.student_name)+str(student.student_email)+str(student.student_books_count)+str(student.student_status)+str(student.student_category)
            student_text6 = str(student.student_name)+str(student.student_email)+str(student.student_status)+str(student.student_category)+str(student.student_books_count)
            student_text7 = str(student.student_name)+str(student.student_email)+str(student.student_status)+str(student.student_books_count)+str(student.student_category)
            student_text8 = str(student.student_name)+str(student.student_email)+str(student.student_category)+str(student.student_status)+str(student.student_books_count)


            if search_text in student_text1 or search_text in student_text2 or search_text in student_text3 or search_text in student_text4 or search_text in student_text5 or search_text in student_text6 or search_text in student_text7 or search_text in student_text8:
                searching_students.append(student)

        return searching_students

# searching librarians
def librarians_filter(name, email, shift):
    if name=='none' and email=='none' and shift=='none':
        librarians = LibrarianRegistration.objects.all()
        return librarians
    elif name!='none' and email!='none' and shift!='none':
        librarians = LibrarianRegistration.objects.filter(librarian_name=name, librarian_email=email, librarian_shift=shift)
        return librarians
    else:
        items = [name, email, shift]
        search_items = []

        for item in items:
            if item!='none':
                search_items.append(item)

        search_text = ''
        for i in search_items:
            search_text = search_text + str(i)

        filtered_librarians = []

        librarians = LibrarianRegistration.objects.all()
        for librarian in librarians:
            text1 = str(librarian.librarian_name)+str(librarian.librarian_email)+str(librarian.librarian_shift)
            text2 = str(librarian.librarian_name)+str(librarian.librarian_shift)+str(librarian.librarian_email)
            if search_text in text1 or search_text in text2:
              filtered_librarians.append(librarian)
            print(search_text)
            print(text1)
            print(text2)

        return filtered_librarians

# list of student and librarian details
def student_and_librarian_list(list_item):
    students = Student_Registration.objects.all()
    librarians = LibrarianRegistration.objects.all()

    student_names = []
    student_emails = []
    student_categories = []
    student_book_counts = []
    student_status = []

    librarian_names = []
    librarian_emails =[]
    librarian_shifts = []

    for student in students:
        student_names.append(student.student_name)
        student_emails.append(student.student_email)
        student_categories.append(student.student_category)
        student_book_counts.append(student.student_books_count)
        student_status.append(student.student_status)

    for librarian in librarians:
        librarian_names.append(librarian.librarian_name)
        librarian_emails.append(librarian.librarian_email)
        librarian_shifts.append(librarian.librarian_shift)

    if list_item=='student names':
        return list(set(student_names))
    elif list_item=='student emails':
        return list(set(student_emails))
    elif list_item=='student categories':
        return list(set(student_categories))
    elif list_item=='student books count':
        return list(set(student_book_counts))
    elif list_item=='student status':
        return list(set(student_status))
    elif list_item=='librarian names':
        return list(set(librarian_names))
    elif list_item=='librarian emails':
        return list(set(librarian_emails))
    elif list_item=='librarian shifts':
        return list(set(librarian_shifts))
    else:
        return None

