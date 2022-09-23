# Generated by Django 3.2.4 on 2022-09-23 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0003_ingredients_recipe_unit_ingredient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='количество')),
            ],
            options={
                'verbose_name': 'ингредиент рецепта',
                'verbose_name_plural': 'ингредиенты рецепта',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
            },
        ),
        migrations.CreateModel(
            name='ShopList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'список покупок',
                'verbose_name_plural': 'списки покупок',
            },
        ),
        migrations.AlterModelOptions(
            name='ingredients_recipe',
            options={'ordering': ['name_ingredient'], 'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='title',
        ),
        migrations.AddField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(default=1, verbose_name='время приготовления'),
        ),
        migrations.AddField(
            model_name='tag',
            name='colour_code_tag',
            field=models.CharField(max_length=50, null=True, verbose_name='стиль тега'),
        ),
        migrations.AddField(
            model_name='tag',
            name='title_tag',
            field=models.CharField(default=3, max_length=100, verbose_name='тег'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredients_recipe',
            name='name_ingredient',
            field=models.CharField(max_length=200, unique=True, verbose_name='название ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredients_recipe',
            name='unit_ingredient',
            field=models.CharField(max_length=32, verbose_name='единица измерения'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(null=True, upload_to='recipe/', verbose_name='Фото рецепта'),
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients_recipe',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tag',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(help_text='Выберите Tag', related_name='recipe', to='recipe.Tag', verbose_name='tag'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title_recipe',
            field=models.CharField(max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='значение тега'),
        ),
        migrations.AddConstraint(
            model_name='ingredients_recipe',
            constraint=models.UniqueConstraint(fields=('name_ingredient', 'unit_ingredient'), name='unique_recipe_ingredient'),
        ),
        migrations.AddField(
            model_name='shoplist',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoplist', to='recipe.recipe', verbose_name='рецепты'),
        ),
        migrations.AddField(
            model_name='shoplist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoplist', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to='recipe.recipe', verbose_name='рецепт в избранном'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='amount',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_amounts', to='recipe.ingredients_recipe', verbose_name='ингредиент'),
        ),
        migrations.AddField(
            model_name='amount',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_amounts', to='recipe.recipe', verbose_name='рецепт'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients_recipe',
            field=models.ManyToManyField(help_text='Выберите ингредиент', related_name='ingredients_recipe', through='recipe.Amount', to='recipe.Ingredients_recipe', verbose_name='ingredients_recipe'),
        ),
        migrations.AddConstraint(
            model_name='shoplist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shoplist'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='UniqueFavorite'),
        ),
        migrations.AddConstraint(
            model_name='amount',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient_recipe'),
        ),
        migrations.AddConstraint(
            model_name='amount',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 1)), name='quantity_gte_1'),
        ),
    ]
