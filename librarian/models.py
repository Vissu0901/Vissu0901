from django.db import models

# Create your models here.

class LibrarianRegistration(models.Model):
    librarian_name = models.CharField(max_length=20)
    librarian_password = models.CharField(max_length=20)
    librarian_email = models.CharField(max_length=40)
    CHOICES = (
        (0, 'Select your shift'),
        ('morning', '6am to 2pm'),
        ('afternoon', '2pm to 11pm'),
    )
    librarian_shift = models.CharField(max_length=30, default=0, choices=CHOICES)
    librarian_registration_date = models.CharField(max_length=30)
    librarian_login_count = models.IntegerField(default=5)
    librarian_security_code = models.IntegerField(default=0)
