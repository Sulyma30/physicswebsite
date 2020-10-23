import csv
from materials.models import Theme, Section

with open('csv_files(15.09.20)/theme.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Theme.objects.get_or_create(full_title=row['full_title'],section=Section.objects.get(title=row['section']),order=row['order_index'],title = row['title'])

