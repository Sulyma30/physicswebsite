from django.db import models

# Create your models here.

class Olympiad(models.Model):
    OLYMP_CHOICES = [('national', 'Всеукраїнська'), ('regional', 'Обласна')]
    name = models.CharField(max_length=100)
    olymp_type = models.CharField(max_length=10, choices=OLYMP_CHOICES)

    def __str__(self):
        return self.name

class OlympEvent(models.Model):
    LOCATION_CHOICES = [(
        'Міста',(
            ('KYIV','м. Київ'),
            ('LVIV', 'м. Львів'),
            ('ODESA', 'м. Одеса'),
            ('KHERSON', 'м. Херсон'),
            ('KRYVYI_RIH', 'м. Кривий Ріг'),
            ('SUMY', 'м. Суми'),
            ('IVANO-FRANKIVSK', 'м. Івано-Франківськ'),)
        ),(
        'Області', (
            ('LVIV_REGION', 'Львівська обл.'),
            ('ODESA_REGION', 'Одеська обл.'),
            ('KHARKIV_REGION', 'Харківська обл.'),)
        ),
    ]
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES)


class OlympFile(models.Model):
    GRADE_CHOICES = [(0, 'Всі класи'), (8, '8 клас'), (9, '9 клас'), (10, '10 клас'), (11 ,'11 клас')]
    TOUR_CHOICES = [('theory', 'Теоретичний тур'), ('exp', 'Експериментальний тур')]
    event = models.ForeignKey(OlympEvent,related_name='files', on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    tour = models.CharField(max_length=6, choices=TOUR_CHOICES)
    problems = models.FileField(null=True, blank=True)
    solutions = models.FileField(null=True, blank=True)