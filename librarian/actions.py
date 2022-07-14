from management.models import StudentBooksInfo

# librarian task filter list
def librarian_list_filter(librarian_email):
    tasks = StudentBooksInfo.objects.filter(librarian_email=librarian_email)

    book_name_list = []
    student_email_list = []
    status_list = []

    for task in tasks:
        book_name_list.append(task.book_name)
        student_email_list.append(task.student_email)
        status_list.append(task.status)

    return list(set(book_name_list)), list(set(student_email_list)), list(set(status_list))
