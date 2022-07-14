from django.urls import path
from . import views

urlpatterns = [
    path('', views.librarian_login_navigation, name='librarian-login'),
    path('new-account', views.librarian_registration_navigation, name='librarian-registration'),
    path('register', views.register_librarian),
    path('home', views.librarian_home),
    path('logout', views.logout_view, name='librarian-logout'),
    path('book-details/<slug>', views.book_details, name='book-details'),
    path('search/<slug>', views.search_for_books, name='search-books-librarian'),
    path('pending-tasks', views.filter_navigation, name='librarian-pending-tasks'),
    path('approve-request', views.librarian_approve_request, name='librarian-approve-request'),
    path('reject-request', views.reject_student_request, name='librarian-reject-request'),
    path('task-details', views.task_wise_details, name='librarian-task-details'),
    path('student-information', views.student_information_table, name='librarian-student-information'),
    path('return-accept', views.return_accept, name='librarian-return-accept'),
    path('filter', views.filter_navigation, name='librarian-filter'),
    path('filtering', views.filtering_tasks)
]