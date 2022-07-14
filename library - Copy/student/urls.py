from django.urls import path
from . import views

urlpatterns = [
    path('',views.student_login_navigation, name='student-login'),
    path('new-account', views.student_registration_navigation, name='student-registration'),
    path('registration', views.register_new_student),
    path('home', views.student_home, name='student-home'),
    path('logout', views.logout_view, name='student-logout'),
    path('search/<slug>', views.search_for_books, name='search'),
    path('books/<slug>', views.get_book_details, name='student-book-details'),
    path('librarian-details', views.librarian_details, name='student-librarian-details'),
    path('student-books', views.student_collections, name='student-collections'),
    path('update', views.student_update_navigation, name='student-update-navigation'),
    path('updated', views.update_student),
    path('preview-book', views.preview_book_details, name='preview-book'),
    path('borrow-book', views.borrow_book_for_student, name='student-borrow-book'),
    path('task-status', views.task_wise_information, name='student-task-status'),
    path('return-book', views.return_book, name='student-return-book'),
]