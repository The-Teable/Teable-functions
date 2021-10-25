import csv
import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "teable-functions.settings")
django.setup()

from polls.models import Teas

CSV_PATH_PRODUCTS = './products.csv'
now = datetime.now()

with open(CSV_PATH_PRODUCTS, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)
    next(data_reader, None) 
    for row in data_reader:
        print(row)
        Teas.objects.create(
            name=row['brand'],
            brand=row['name'],
            type=row['type'],
            flavor=row['flavor'],
            caffeine=row['caffeine'],
            efficacies=row['efficacies'],
            price=row['price'],
            create_date = now,
            update_date = now,
        )
