from django.contrib.auth import get_user_model
from django.db import models
from core.models import CreatedModel

 User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Recipe(models.Model):
    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='author')  # проверить правильность
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',  # было поправлено с qroups
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    # Аргумент upload_to указывает директорию,
    # в которую будут загружаться пользовательские файлы.

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

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
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост_для_комента',
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
