import csv
import os

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_name = f'{BASE_DIR}/recipes/management/fixtures/ingredients.csv'


class Command(BaseCommand):
    help = 'Load ingredient data to database'

    def handle(self, *args, **options):
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                title, dimension = line
                Ingredient.objects.get_or_create(title=title, dimension=dimension)
