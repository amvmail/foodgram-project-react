from django.contrib import admin

from .models import Recipe, Ingredients_recipe, Tag

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('tag',)
    list_editable = ('title',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_recipe', 'text', 'ingredients_recipe', 'tag', 'pub_date')
    search_fields = ('tag', 'title_recipe')
    list_filter = ('pub_date', 'tag',)
    list_editable = ('title_recipe', 'text', 'ingredients_recipe', 'tag',)
    empty_value_display = '-пусто-'


class Ingredients_recipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name_ingredient', 'unit_ingredient', 'description_ingredient')
    search_fields = ('name_ingredient', 'unit_ingredient')
    list_filter = ('name_ingredient', 'unit_ingredient',)
    list_editable = ('name_ingredient', 'unit_ingredient', 'description_ingredient',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients_recipe, Ingredients_recipeAdmin)
admin.site.register(Tag, TagAdmin)
