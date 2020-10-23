import csv
from materials.models import Supersection

with open('csv_files(15.09.20)/supersection.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        _, created = Supersection.objects.get_or_create(order=row['order_index'],title = row['title'])

