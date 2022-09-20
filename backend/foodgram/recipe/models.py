from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Ingredients_recipe(models.Model):
    name_ingredient = models.CharField(max_length=200, unique=True)
    unit_ingredient = models.CharField(max_length=20)
    description_ingredient = models.TextField(null=True, blank=True)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author')  # проверить правильность
    title_recipe = models.CharField(max_length=200)
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipe/',
        blank=True
    )
    text = models.TextField(
        'Текст рецепта',
        help_text='Введите текст рецепта'
    )
    ingredients_recipe = models.ForeignKey(
        Ingredients_recipe,
        null=True,
        on_delete=models.SET_NULL,
        related_name='ingredients_recipe',  # было поправлено с qroups
        verbose_name='ingredients_recipe',
        help_text='Выберите ингредиент'
    )
    tag = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.SET_NULL,
        related_name='tag',
        verbose_name='tag',
        help_text='Выберите Tag'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    # Аргумент upload_to указывает директорию,
    # в которую будут загружаться пользовательские файлы.

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text[:15]


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
        unique_together = (('user', 'author'),)

    def __str__(self):
        return self.user.username
