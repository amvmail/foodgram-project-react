import csv

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredient data to database'

    filename = f'{BASE_DIR}/recipes/management/fixtures/ingredients.csv'

    def __load_data(self, filename):
        with open(self.filename, newline='') as isfile:
            data = csv.DictReader(
                isfile, fieldnames=('title', 'dimension'))
            for item in data:
                yield item

    def handle(self, *args, **options):
        """
        The function adds ingredients and tags to the database on first deployment
        python manage.py load_product_data
        """
        for item in self.__load_data(self.filename):
            obj = Ingredient(**item)
            obj.save()