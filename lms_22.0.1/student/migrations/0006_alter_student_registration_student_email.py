# Generated by Django 4.0.4 on 2022-07-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_student_registration_failure_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_registration',
            name='student_email',
            field=models.CharField(max_length=40),
        ),
    ]
