import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    """
    Команда 'load_ingredients' загружает ингредиенты
    в БД Ingredient из csv файла, который располагается в
    директории recipes/management/fixtures/.
    """

    def handle(self, *args, **options):
        self.import_ingredients()
        print('Загрузка ингредиентов завершена.')

    def import_ingredients(self, file='recipes/management/fixtures/ingredients.csv'):
        print(f'Загрузка {file}...')
        file_path = f'{file}'
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                status, created = Ingredient.objects.update_or_create(
                    title=row[0],
                    dimension=row[1]
                )
