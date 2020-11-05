from django.db import models

# Create your models here.
class Supersection(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.title}"

class Section(models.Model):
    title = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0)
    supersection = models.ForeignKey(Supersection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Theme(models.Model):
    title = models.CharField(max_length=100)
    full_title = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    section = models.ForeignKey(Section, related_name="themes", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Requirement(models.Model):
    parent_theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="themes")
    child_theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="requirements")

    def __str__(self):
        return f"{self.parent_theme.title}"

class Literature(models.Model):

    LITERATURE_CHOICES = [ ('theory', 'Підручник' ), ('problems', 'Задачник'), ('exp', 'Експеримент') ]
    title = models.CharField(max_length=200)
    short_title = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()
    literature_type = models.CharField(max_length=10, choices=LITERATURE_CHOICES)
    eng_title = models.CharField(max_length=50, null=True, blank=True)

    def literature_filename(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<eng_title__year> if eng_title exists
        if (instance.eng_title and instance.year):
            file_type = 'pdf' if 'pdf' in filename else 'djvu'
            return '{0}_{1}.{2}'.format(instance.eng_title, instance.year, file_type)
        else:
            return '{0}'.format(filename)

    pdf = models.FileField(null=True, blank=True, upload_to=literature_filename)
    djvu = models.FileField(null=True, blank=True, upload_to=literature_filename)

    def __str__(self):
        return f"{self.short_title}"


class TaskSet(models.Model):
    DIFFICULTY_CHOICE = [
        (0, 'novice'), (1, 'advanced'), (2, 'expert'), (3, 'math')
    ]
    difficulty = models.PositiveSmallIntegerField(null=True, choices=DIFFICULTY_CHOICE)
    theme = models.ForeignKey(Theme, related_name='task_sets', on_delete=models.CASCADE)
    literature = models.ForeignKey(Literature, on_delete=models.CASCADE)

class Theory(models.Model):
    start_page = models.PositiveSmallIntegerField(default=0)
    end_page = models.PositiveSmallIntegerField(default=0)
    task_set = models.ForeignKey(TaskSet, related_name='theory_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.start_page}-{self.end_page}"
    

class Problem(models.Model):
    number = models.CharField(max_length=10)
    chosen = models.BooleanField(default=False)
    task_set = models.ForeignKey(TaskSet, related_name='problem_tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.number