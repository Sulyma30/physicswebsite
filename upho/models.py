from django.db import models

# Create your models here.
class Supersection(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    def serialize(self):
        return {
            "title" : self.title,
            "id" : self.id
        }

    def __str__(self):
        return f"{self.title}"

class Section(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)
    supersection = models.ForeignKey(Supersection, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "title" : self.title,
            "id" : self.id
        }

    def __str__(self):
        return f"{self.title}"

class Theme(models.Model):
    title = models.CharField(max_length=100)
    full_title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "title" : self.title,
            "id" : self.id,
            "full_title" : self.full_title,
            "requirements" : [requirement.parent_theme.title for requirement in Requirement.objects.filter(child_theme=self)]
        }

    def __str__(self):
        return f"{self.title}"
    
class Requirement(models.Model):
    parent_theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="requirement")
    child_theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="theme")

class Literature(models.Model):

    LITERATURE_CHOICES = [ ('theory', 'Підручник' ), ('problems', 'Задачник') ]
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    literature_type = models.CharField(max_length=10, choices=LITERATURE_CHOICES)
    eng_title = models.CharField(max_length=50, null=True)

    def literature_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<eng_title__year> if eng_title exists
        if (instance.eng_title and instance.year):
            return '{0}_{1}.pdf'.format(instance.eng_title, instance.year)
        else:
            return '{0}'.format(filename)

    pdf = models.FileField(null=True, upload_to=literature_filename)

    def serialize(self):
        return {
            "title" : self.title,
            "id" : self.id,
            "short_title" : self.short_title,
            "supersections" : list(dict.fromkeys([ material.theme.section.supersection.title for material in (Theory.objects.filter(literature=self) if self.literature_type=='theory' else Problem.objects.filter(literature=self)) ])),
            "year" : self.year,
            "pdf" : self.pdf.url if self.pdf else ''
        }

    def __str__(self):
        return f"{self.short_title}"



class Theory(models.Model):
    THEORY_DIFFICULTY_CHOICE = [
        (0, 'Novice'), (1, 'Advanced'), (2, 'Expert')
    ]
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    start_page = models.PositiveSmallIntegerField(default=0)
    end_page = models.PositiveSmallIntegerField(default=0)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(choices=THEORY_DIFFICULTY_CHOICE)
    chosen = models.BooleanField(default=False)

class Problem(models.Model):
    PROBLEM_DIFFICULTY_CHOICE = [
        (0, 'Novice'), (1, 'Advanced'), (2, 'Expert'), (3, 'Math')
    ]
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    number = models.CharField(max_length=10)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)
    difficulty = models.PositiveSmallIntegerField(null=True, choices=PROBLEM_DIFFICULTY_CHOICE)
    chosen = models.BooleanField(default=False)

    
    # Olymp_type must be unique!!!
class Olympiad(models.Model):
    OLYMP_CHOICES = [('national', 'Всеукраїнська'), ('regional', 'Обласна')]
    name = models.CharField(max_length=100)
    olymp_type = models.CharField(max_length=10, choices=OLYMP_CHOICES)

    def __str__(self):
        return self.name

class OlympEvent(models.Model):
    LOCATION_CHOICES = [
            ('KYIV','м. Київ'),
            ('LVIV', 'м. Львів'),
            ('ODESA', 'м. Одеса'),
            ('KHERSON', 'м. Херсон'),
    ]
    olympiad = models.ForeignKey(Olympiad, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=30, choices=LOCATION_CHOICES)


class OlympFile(models.Model):
    GRADE_CHOICES = [(0, 'Всі класи'), (8, '8 клас'), (9, '9 клас'), (10, '10 клас'), (11 ,'11 клас')]
    TOUR_CHOICES = [('theory', 'Теоретичний тур'), ('exp', 'Експериментальний тур')]
    event = models.ForeignKey(OlympEvent, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES)
    tour = models.CharField(max_length=6, choices=TOUR_CHOICES)
    solutions = models.BooleanField(default=False)
    pdf = models.FileField()
