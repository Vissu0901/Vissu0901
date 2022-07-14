from django.db import models

# Create your models here.

class Management(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    count = models.IntegerField(default=5)
    mode = models.CharField(max_length=20, default='Dark Mode')

class Books(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    CHOICES = (
        (0,'Select Category'),
        ('bachelor-of-arts','Bachelor of Arts'),
        ('bba/bms','BMS/BBA'),
        ('btech-bachlor-of-engg./tech','Bachelor of Engg./Tech' ),
        ('bachelor-of-commerce','Bachelor of Commerce' ),
        ('bachelor-of-law','Bachelor of Law'),
        ('mbbs-bachelor-of-medicine','Bachelor of Medicine' ),
        ('bachelor-of-science','Bachelor of Science'),
        ('intermediate','Intermediate'),
        ('ssc-10th-standard','10th Standard')
    )
    category = models.CharField(max_length=30, choices=CHOICES, default=0)
    upload_date = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    available_count = models.IntegerField(default=0)
    location = models.CharField(max_length=30)

# Student books information
class StudentBooksInfo(models.Model):
    book_name = models.CharField(max_length=40)
    librarian_email = models.CharField(max_length=40)
    student_email = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    requested_date = models.DateField()
    approved_date = models.DateField()
    return_date = models.DateField()
    return_approved_date = models.DateField()



