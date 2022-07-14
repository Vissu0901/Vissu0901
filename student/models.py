from django.db import models

# Create your models here.
class Student_Registration(models.Model):
    student_name = models.CharField(max_length=20)
    student_email = models.CharField(max_length=40)
    student_password = models.CharField(max_length=20)
    CHOICES = (
        (0, 'Select Category'),
        ('bachelor-of-arts', 'Bachelor of Arts'),
        ('bba/bms', 'BMS/BBA'),
        ('btech-bachlor-of-engg./tech', 'Bachelor of Engg./Tech'),
        ('bachelor-of-commerce', 'Bachelor of Commerce'),
        ('bachelor-of-law', 'Bachelor of Law'),
        ('mbbs-bachelor-of-medicine', 'Bachelor of Medicine'),
        ('bachelor-of-science', 'Bachelor of Science'),
        ('intermediate', 'Intermediate'),
        ('ssc-10th-standard', '10th Standard')
    )
    student_category = models.CharField(max_length=30, choices=CHOICES, default=0)
    student_books_count = models.IntegerField(default=3)
    student_login_count = models.IntegerField(default=5)
    student_registration_date = models.CharField(max_length=30)
    student_status = models.CharField(max_length=10, default='unblock')
    fine_amount = models.IntegerField(default=0)
    failure_1 = models.IntegerField(default=0)
    failure_2 = models.IntegerField(default=0)
    failure_3 = models.IntegerField(default=0)
    failure_4 = models.IntegerField(default=0)
    failure_5 = models.IntegerField(default=0)


