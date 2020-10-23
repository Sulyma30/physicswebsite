import csv
from materials.models import Theme, Problem, Literature

with open('csv_files(15.09.20)/problem.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Problem.objects.get_or_create(theme=Theme.objects.get(full_title=row['theme']),literature=Literature.objects.get(title=row['literature']), number=row['number'], chosen=row['chosen'], difficulty=row['difficulty'] if row['difficulty'] else None)

