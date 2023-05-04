import json

from django.core.management import BaseCommand
from catalog_app.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()

        with open('fixtures.json', 'r') as file:
            data = json.load(file)

        category_objects = []
        for category in data:
            if category['model'] == 'catalog_app.category':
                fields = category['fields']
                category_objects.append(Category(**fields))

        Category.objects.bulk_create(category_objects)
