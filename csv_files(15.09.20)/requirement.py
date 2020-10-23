import csv
from materials.models import Requirement, Theme

with open('csv_files(15.09.20)/requirement.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Requirement.objects.get_or_create(parent_theme=Theme.objects.get(id=row['parent_id']),child_theme = Theme.objects.get(id=row['child_id']))

