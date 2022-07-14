from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManagementView.as_view(), name='management-login'),
    path('login', views.ManagementLoginView.as_view(), name='management-home'),
    path('home',views.loading_page, name='home-navigation'),
    #path('home', views.home, name='home'),
    path('change-mode',views.loading_change_mode_management_home, name='management-change-mode'),
    path('changing-mode', views.change_mode_in_home, name='management-changing-mode'),
    path('add-new-book', views.add_new_book_navigation, name='add-new-book'),
    path('add-book',views.add_new_book),
    path('search',views.search_for_books),
    path('logout',views.logout_view, name='logout'),
    path('loading-student-details', views.loading_student_details, name='m-loading-student-details'),
    path('student-details', views.get_student_details, name='m-student-details'),
    path('student-information/<slug>', views.get_student_wise_information, name='student-wise-details'),
    #path('delete/<slug>', views.delete_book, name='delete-book'),
    path('deleting-book', views.delete_book, name='delete-book'),
    path('update-<slug>', views.update_book_navigation, name='update-navigation'),
    path('update-book/<slug>', views.update_book_information, name='update-book'),
    path('loading-librarian-details', views.loading_librarian_details, name='m-loading-librarian-details'),
    path('librarian-details', views.get_librarian_details, name='m-librarian-details'),
    path('loading-back-to-home', views.loading_back_to_home_staff, name='m-back-to-home'),
    path('librarian-information/<slug>', views.get_librarian_wise_information, name='librarian-wise-details'),
    path('book-details/<slug>', views.get_book_details, name='management-book-details'),
    path('search-students', views.students_filtering),
    path('search-librarians', views.librarians_filtering),
    path('md/login', views.mode_change_loginPage, name='mode-change-for-login')
]