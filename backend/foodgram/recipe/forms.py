from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify  # взято из инета

from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title_recipe ', 'image', 'text', 'ingredients_recipe',
                  'tag', 'time_to_cook_recipe'
                  )
        text = forms.CharField(label='Текст рецепта'),
        image = forms.ImageField(label='Фото рецепта'),
        tag = forms.CharField(label='Tag')

    # Валидация поля slug
    def clean_slug(self):
        """Обрабатывает случай, если slug не уникален."""
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        if not slug:
            title = cleaned_data.get('title')
            slug = slugify(title)[:100]
        if Recipe.objects.filter(slug=slug).exists():
            raise ValidationError(
                f'Tag "{slug}" уже существует, '
                'придумайте уникальное значение'
            )
        return slug


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        text = forms.CharField(label='Текст комментария')
