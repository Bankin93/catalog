from django.core.management import BaseCommand, call_command

from catalog_app.models import Category, Product
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        call_command('loaddata', 'fixtures.json')








