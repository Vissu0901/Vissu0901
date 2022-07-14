from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from datetime import date, timedelta, datetime

import logging
from management.models import StudentBooksInfo
from student.models import Student_Registration

logging.basicConfig(level=logging.DEBUG, filename='logs/managementDEBUG.log', filemode='w', format='%(asctime)s %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# landing page
class LandingPage(View):
    def get(self, request):
        logging.info('Loading landing page...')

        day_check = date.today()+timedelta(days=1)
        tasks = StudentBooksInfo.objects.filter(status='approved')

        for task in tasks:
            if task.return_date<day_check:
                student = Student_Registration.objects.get(student_email=task.student_email)

                consective_failures_check()
                student.save()

        logging.info('loaded landing page')
        return render(request, 'landing_page_new.html')

def consective_failures_check():
    approved_tasks = StudentBooksInfo.objects.filter(status='approved')
    day_check = date.today() + timedelta(days=1)
    for task in approved_tasks:
        if task.return_date<day_check:
            student = Student_Registration.objects.get(student_email=task.student_email)

            #fine amount
            date1_today = date.today()
            date2_return = task.return_date

            diff_str = str(date1_today-date2_return)
            split_days = diff_str.split()
            days = int(split_days[0])
            student.fine_amount = days*10
            student.save()

            failures = [student.failure_1, student.failure_2, student.failure_3, student.failure_4, student.failure_5]

            if student.failure_1!=0 and student.failure_2!=0 and student.failure_3!=0 and student.failure_4!=0 and student.failure_5!=0:
                student.student_status = 'block'
                student.save()
            else:
                if task.id not in failures:
                    for i in range(len(failures)):
                        if failures[i] == 0:
                            if i == 0:
                                student.failure_1 = int(task.id)
                                student.save()
                                break
                            elif i == 1:
                                student.failure_2 = int(task.id)
                                student.save()
                                break
                            elif i == 2:
                                student.failure_3 = int(task.id)
                                student.save()
                                break
                            elif i == 3:
                                student.failure_4 = int(task.id)
                                student.save()
                                break
                            elif i == 4:
                                student.failure_5 = int(task.id)
                                student.save()
                                break




                """for i in failures:
                    if i==int(task.id):
                        break
                    else:
                        pass


                        for i in range(len(failures)):
                            if failures[i] == 0:
                                if i == 0:
                                    student.failure_1 = int(task.id)
                                    student.save()
                                    break
                                elif i == 1:
                                    student.failure_2 = int(task.id)
                                    student.save()
                                    break
                                elif i == 2:
                                    student.failure_3 = int(task.id)
                                    student.save()
                                    break
                                elif i == 3:
                                    student.failure_4 = int(task.id)
                                    student.save()
                                    break
                                elif i == 4:
                                    student.failure_5 = int(task.id)
                                    student.save()
                                    break




                for i in failures:
                    if i==0:
                        student.i = task.id
                        student.save()"""
