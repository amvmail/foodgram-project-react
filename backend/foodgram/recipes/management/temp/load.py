import csv
import mimetypes
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')
django.setup()

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.recipes import get_recipes_application

from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Ingredient
from recipes.models import Ingredient, Amount, Recipe

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_name = f'{BASE_DIR}/fixtures/ingredients.csv'
'''

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_name) as f:
            reader = csv.reader(f)
            for row in reader:
                created = Ingredient.objects.get_or_create(
                    title=row[0],
                    dimension=row[1],
                )

    for item in self.handle(file_name):
        obj = Ingredient(**item)
        obj.save()

'''


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_name, 'r') as csv_file:
            csv_file, fieldnames = ('title', 'dimension')
            csv_reader = csv.reader(csv_file, delimiter=';')
            # data = csv.reader(
            #    csv_file, fieldnames=('title', 'dimension'))
            # for item in data:
            #    yield item
            for item in csv_reader:
                obj = Ingredient(**item)
                obj.save()
                # Ingredient.objects.create(title=row[0], dimension=row[1])
            #for item in data:
            #    yield item