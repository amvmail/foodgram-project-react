import csv

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient

file_name = f'{BASE_DIR}/fixtures/ingredients.csv'


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(file_name) as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                title, unit = line
                Ingredient.objects.get_or_create(title=title, dimension=unit)
