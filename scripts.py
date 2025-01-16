import random
from datacenter.models import Subject, Lesson, Chastisement, Mark, Commendation, Schoolkid



def fix_marks(student_name):
    student = get_name(student_name)
    Mark.objects.filter(schoolkid=student, points__lt=4).update(points=random.randint(4, 5))

def remove_chastisements(student_name):
    student = get_name(student_name)
    teachers_comments = Chastisement.objects.filter(schoolkid=student)
    teachers_comments.delete()

def create_commendation(student_name, subject):
    student = get_name(student_name)
    school_subject = get_subject(subject, student.year_of_study)
    lesson = Lesson.objects.filter(subject=school_subject).order_by('-date').first()
    if lesson is None:
        return 'Данного урока нет'
    with open('comments.txt', 'r', encoding='utf-8') as file:
        comments = random.choice(file.readlines())
    Commendation.objects.create(schoolkid=student, subject=school_subject, text=comments, created=lesson.date, teacher=lesson.teacher)

def get_name(student_name):
    try:
        student = Schoolkid.objects.get(full_name__contains=student_name)
        return student
    except Schoolkid.MultipleObjectsReturned:
        raise ValueError('Найдено несколько учеников с таким именем. Пожалуйста, уточните запрос.')
    except Schoolkid.DoesNotExist:
        raise ValueError('Введены некорректные данные. Ученик не найден.')

def get_subject(item_name, year_of_study):
    try:
        subject = Subject.objects.get(title=item_name, year_of_study=year_of_study)
        return subject
    except Subject.DoesNotExist:  # Здесь тоже используем специфичное исключение
        raise ValueError('Введены некорректные данные. Предмет не найден.')