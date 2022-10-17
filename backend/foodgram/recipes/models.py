from django.db import models
from users.models import User

from .validators import image_size_validator


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='автор',
                               on_delete=models.CASCADE,
                               related_name='recipes')
    title = models.CharField(verbose_name='название',
                             max_length=128)
    pub_date = models.DateTimeField(verbose_name='дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(verbose_name='изображение',
                              upload_to='recipes/',
                              null=True,
                              validators=[image_size_validator])
    description = models.TextField(verbose_name='описание')
    tags = models.ManyToManyField('Tag',
                                  verbose_name='теги',
                                  related_name='recipes')
    ingredients = models.ManyToManyField('Ingredient',
                                         verbose_name='ингредиенты',
                                         through='Amount',
                                         through_fields=('recipe',
                                                         'ingredient'))
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления',
        default=1
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(verbose_name='название ингредиента',
                             max_length=128,
                             unique=True,
                             db_index=True)
    dimension = models.CharField(verbose_name='единица измерения',
                                 max_length=32)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'dimension'],
            name='unique_recipe_ingredient')]
        ordering = ['title', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.title} ({self.dimension})'


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт',
                               related_name='recipe_amounts',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='ингредиент',
                                   related_name='ingredient_amounts',
                                   on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            ),
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name='quantity_gte_1'
            ),
        ]
        verbose_name = 'ингредиент рецепта'
        verbose_name_plural = 'ингредиенты рецепта'

    def __str__(self):
        return self.ingredient.title


class Tag(models.Model):
    name = models.CharField(verbose_name='название тега',
                            max_length=50, unique=True)
    color = models.CharField(verbose_name='цвет',
                             null=True, max_length=10)
    slug = models.SlugField('Slug', unique=True, max_length=200)

    class Meta:
        ordering = ['name']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class ShopList(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='shoplist',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепты',
                               related_name='shoplist',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_shoplist')]
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'

    def __str__(self):
        return self.recipe.title


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт в избранном',
                               related_name='favorite_recipes',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             verbose_name='пользователь',
                             related_name='favorites',
                             on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='UniqueFavorite')]
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'

    def __str__(self):
        return self.recipe.title


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='подписчик',
                             related_name='follower',
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               verbose_name='автор',
                               related_name='following',
                               on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_subscription')]
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} подписан(а) на {self.author}'
