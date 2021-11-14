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
    for row in data_reader:
        print(row)
        Teas.objects.create(
            name=row['name'],
            brand=row['brand'],
            type=row['type'],
            flavor=row['flavor'],
            caffeine=row['caffeine'],
            efficacies=row['efficacies'],
            site_url=row['url'],
            price=row['price'],
            stock=row['stock'],
            create_date = now,
            update_date = now,
        )
