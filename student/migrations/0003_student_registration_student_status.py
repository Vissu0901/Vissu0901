# Generated by Django 4.0.4 on 2022-06-13 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_delete_studentbooks'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_registration',
            name='student_status',
            field=models.CharField(default='unblock', max_length=10),
        ),
    ]