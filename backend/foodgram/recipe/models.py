from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel
from users.models import User

# User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Recipe(models.Model):
    text = models.TextField(
        'Текст рецепта',
        help_text='Введите текст рецепта'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author')  # проверить правильность
    tag = models.ForeignKey(
        Tag,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipe',  # было поправлено с qroups
        verbose_name='Tag',
        help_text='Выберите Tag'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipe/',
        blank=True
    )
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
