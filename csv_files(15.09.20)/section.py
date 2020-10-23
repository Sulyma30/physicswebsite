import csv
from materials.models import Supersection, Section

with open('csv_files(15.09.20)/section.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Section.objects.get_or_create(supersection=Supersection.objects.get(title=row['supersection']), order=row['order_index'],title = row['title'])

