# Generated by Django 4.0.4 on 2022-06-20 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_student_registration_fine_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_registration',
            name='failure_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_registration',
            name='failure_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_registration',
            name='failure_3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_registration',
            name='failure_4',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student_registration',
            name='failure_5',
            field=models.IntegerField(default=0),
        ),
    ]