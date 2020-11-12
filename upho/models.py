from django.db import models

# Create your models here.

class Olympiad(models.Model):
    OLYMP_CHOICES = [('national', 'Всеукраїнська'), ('regional', 'Обласна')]
    name = models.CharField(max_length=100)
    olymp_type = models.CharField(max_length=10, choices=OLYMP_CHOICES)

    def __str__(self):
        return self.name

class Location(models.Model):
    TYPE_CHOICES = [('city', 'місто'), ('region', 'область')]
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)

    def __str__(self):
        representation = f"м. {self.title}" if self.location_type == 'city' else f"{self.title} обл."
        return representation

class OlympEvent(models.Model):
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class OlympFile(models.Model):
    GRADE_CHOICES = [(0, 'Всі класи'), (8, '8 клас'), (9, '9 клас'), (10, '10 клас'), (11 ,'11 клас')]
    TOUR_CHOICES = [('theory', 'Теоретичний тур'), ('exp', 'Експериментальний тур')]
    event = models.ForeignKey(OlympEvent,related_name='files', on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    tour = models.CharField(max_length=6, choices=TOUR_CHOICES)
    problems = models.FileField(null=True, blank=True)
    solutions = models.FileField(null=True, blank=True)