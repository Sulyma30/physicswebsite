import csv
from materials.models import Theme, Theory, Literature, TaskSet

with open('csv_files(15.09.20)/theory.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = TaskSet.objects.get_or_create(theme=Theme.objects.get(full_title=row['theme']),literature=Literature.objects.get(title=row['literature']), difficulty=row['difficulty'])

with open('csv_files(15.09.20)/theory.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Theory.objects.get_or_create(task_set=TaskSet.objects.get(theme=Theme.objects.get(full_title=row['theme']),literature=Literature.objects.get(title=row['literature']), difficulty=row['difficulty']), start_page=row['start_page'], end_page=row['end_page'])
