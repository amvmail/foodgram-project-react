from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils.text import slugify  # взято из инета

from .models import Recipe, Amount, Ingredients_recipe, Comment


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title_recipe', 'text', 'tag', 'image', 'cooking_time')
        widgets = {
            'tag': forms.CheckboxSelectMultiple(),
            'cooking_time': forms.NumberInput(attrs={'value': 1}),
        }

        cooking_time = forms.IntegerField(required=True, min_value=1)
        image = forms.ImageField(required=True)

        def save_recipe(self, recipe, ingredients):
            for title_recipe, quantity in ingredients_recipe.items():
                ingredient = get_object_or_404(ingredients_recipe, title=title)
                recipe_ingredients = Amount(recipe=recipe,
                                            ingredient=ingredient,
                                            quantity=quantity)
                recipe_ingredients.save()

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
