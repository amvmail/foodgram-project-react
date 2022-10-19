from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

from users.models import User


class Tag(models.Model):
    """
    Recipe tag model, color field with a choice of colors in hex format.
    """
    name = models.CharField(_('Имя'), max_length=50, unique=True)
    color = ColorField(_('Цвет HEX'), unique=True)
    slug = models.SlugField(_('Слаг'), unique=True)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['-name']
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')


class Ingredient(models.Model):
    """
    Ingredient Model
    """
    name = models.CharField(_('Имя'), max_length=150, unique=True)
    measurement_unit = models.CharField(_('Единица измерения'), max_length=60)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['-name']
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')


class Recipe(models.Model):
    """Recipe Model"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name=_('автор'))
    name = models.CharField(verbose_name='название', max_length=200)
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientRecipe',
                                         through_fields=('recipe',
                                                         'ingredient'),
                                         verbose_name='ингредиенты')

    image = models.ImageField(_('Изображение'), upload_to='recipe/')
    text = models.TextField(_('Описание'))
    tags = models.ManyToManyField(Tag, verbose_name=_('Тег'))
    cooking_time = models.PositiveIntegerField(
        _('Время приготовления'),
        validators=[MinValueValidator(limit_value=1,
                    message=_("Введите число больше единицы"))])
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.name

    class Meta():
        ordering = ['-pub_date']
        verbose_name = ('Рецепт')
        verbose_name_plural = ('Рецепты')


class IngredientRecipe(models.Model):
    """
    A model for linking recipes, ingredients and the number of ingredients.
    """
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='recipes',
                                   verbose_name=_('Ингредиент'))
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='ingredients_IngredientRecipe',
                               verbose_name=_('Рецепт'))
    # amount = models.PositiveSmallIntegerField(_('Количество'))
    amount = models.IntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f"Ингредиент: {self.ingredient}, Рецепт: {self.recipe}"

    class Meta():
        ordering = ['-id']
        verbose_name = _('Ингредиент для рецепта')
        verbose_name_plural = _('Ингредиенты для рецептов')


class Favorite(models.Model):
    """
    Model of selected recipes
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='recipes_favorites',
                             verbose_name=_('Пользователь'))
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name="favorites",
                               verbose_name=_('Рецепт'))

    def __str__(self):
        return f'избранное пользователя {self.user}'

    class Meta():
        ordering = ['-id']
        verbose_name = _('Избранный рецепт')
        verbose_name_plural = _('Избранные рецепты')


class ShoppingCart(models.Model):
    """
    Shopping List Model
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='shopping_carts',
                             verbose_name=_('Пользователь'))
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping_carts',
                               verbose_name=_('Рецепт'))

    def __str__(self):
        return f'список покупок пользователя {self.user}'

    class Meta():
        ordering = ['-id']
        verbose_name = _('Список покупок')
        verbose_name_plural = _('Списки покупок')
        models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_recording')
