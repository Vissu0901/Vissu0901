# Generated by Django 4.0.4 on 2022-06-23 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('category', models.CharField(choices=[(0, 'Select Category'), ('bachelor-of-arts', 'Bachelor of Arts'), ('bba/bms', 'BMS/BBA'), ('btech-bachlor-of-engg./tech', 'Bachelor of Engg./Tech'), ('bachelor-of-commerce', 'Bachelor of Commerce'), ('bachelor-of-law', 'Bachelor of Law'), ('mbbs-bachelor-of-medicine', 'Bachelor of Medicine'), ('bachelor-of-science', 'Bachelor of Science'), ('intermediate', 'Intermediate'), ('ssc-10th-standard', '10th Standard')], default=0, max_length=30)),
                ('upload_date', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
                ('available_count', models.IntegerField()),
                ('location', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Management',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('count', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='StudentBooksInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=40)),
                ('librarian_email', models.CharField(max_length=40)),
                ('student_email', models.CharField(max_length=40)),
                ('status', models.CharField(max_length=40)),
                ('requested_date', models.DateField()),
                ('approved_date', models.DateField()),
                ('return_date', models.DateField()),
                ('return_approved_date', models.DateField()),
            ],
        ),
    ]
