import sys
sys.path.append("../users")
from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel
from users.models import User

class Tag(models.Model):
    title_tag = models.CharField(verbose_name='тег', max_length=100)
    slug = models.SlugField(verbose_name='значение тега', max_length=200, unique=True)
    colour_code_tag = models.CharField(verbose_name='стиль тега',
                             max_length=50, null=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.slug


class Ingredients_recipe(models.Model):
    name_ingredient = models.CharField(verbose_name='название ингредиента',
                                       max_length=200, unique=True)
    unit_ingredient = models.CharField(verbose_name='единица измерения',
                                       max_length=32)
    description_ingredient = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name_ingredient', 'unit_ingredient'],
            name='unique_recipe_ingredient')]
        ordering = ['name_ingredient', ]
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

        def __str__(self):
            return f'{self.name_ingredient} ({self.unique_recipe_ingredient})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipe')
    title_recipe = models.CharField(verbose_name='название', max_length=200)
    image = models.ImageField(
        verbose_name='Фото рецепта',
        upload_to='recipe/',
        null=True
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Введите текст рецепта'
    )
    ingredients_recipe = models.ManyToManyField(
        Ingredients_recipe,
        through='Amount',
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='tag',
        help_text='Выберите Tag'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления',
        default=1
    )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)


    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text[:15]


class Amount(models.Model):
    """
        Модель, связывающая рецепт и ингредиент.
        В этой таблице будет хранится кол-во ингредиента в рецепте.
    """
    recipe = models.ForeignKey(Recipe,
                               verbose_name='рецепт',
                               related_name='recipe_amounts',
                               on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients_recipe,
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
        return self.Ingredients_recipe.name_ingredient


class Comment(CreatedModel):
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    # created = yatube/models.py/created
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор_комента',
        related_name='comments')  # проверить правильность
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт_для_комента',
        related_name='comments')  # проверить правильность

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор постов',
        related_name='following'
    )

    class Meta:
        verbose_name = 'Подписка на'
        verbose_name_plural = 'Подписки на'
        unique_together = (('user', 'author'),)

    def __str__(self):
        return self.user.username


class ShopList(models.Model):
    user = models.ForeignKey(get_user_model(),
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
        return self.recipe.title_recipe


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
