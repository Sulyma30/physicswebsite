import csv
from materials.models import Theme, Theory, Literature

with open('csv_files(15.09.20)/theory.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Theory.objects.get_or_create(theme=Theme.objects.get(title=row['theme']),literature=Literature.objects.get(title=row['literature']), start_page=row['start_page'], end_page=row['end_page'], chosen=row['chosen'], difficulty=row['difficulty'])

