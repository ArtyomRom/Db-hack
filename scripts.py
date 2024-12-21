from datacenter.models import *
from django.core.exceptions import ObjectDoesNotExist
import random

def fix_marks(student_name):
    student = check_name(student_name)
    bad_ratings = Mark.objects.filter(schoolkid=student, points__lt=4)
    for bad_rating in bad_ratings:
        bad_rating.points = random.randint(4, 5)
        bad_rating.save()

def remove_chastisements(student_name):
    student = check_name(student_name)
    teachers_comments = Chastisement.objects.filter(schoolkid=student)
    teachers_comments.delete()

def create_commendation(student_name, subject):
    student = check_name(student_name)
    school_subject = Subject.objects.filter(title=check_subject(subject), year_of_study=str(student.year_of_study))
    lesson = random.choice(Lesson.objects.filter(subject=school_subject))
    with open('comments.txt', 'r', encoding='utf-8') as file:
        comments = random.choice(file.readlines())
    Commendation.objects.create(schoolkid=student, subject=school_subject, text=comments, created=lesson.date, teacher=lesson.teacher)

def check_name(student_name):
    student = Schoolkid.objects.filter(full_name__contains=student_name)
    try:
        student = student.get(id=2)
        student = student.get(id=0)
        student = student[0]
        return student[0]
    except ObjectDoesNotExist as error:
        return error + '\nВведене некорректные данные'

def check_subject(item_name):
    subject = Subject.objects.filter(title=item_name)
    try:
        subject = subject.get(id=0)
        subject = subject[0]
        return subject.title
    except ObjectDoesNotExist as error:
        return error + '\nВведене некорректные данные'