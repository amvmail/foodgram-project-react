from django.contrib import admin

from .models import Tag, Recipe, Ingredients_recipe, Amount, Comment, Follow


class Ingredients_recipeInline(admin.TabularInline):
    model = Ingredients_recipe
    extra = 2


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_recipe', 'text', 'pub_date', 'author')
    search_fields = ('tag', 'name_ingredient',)
    list_filter = ('pub_date',)
    list_editable = ('text',)
    # inlines = (Ingredients_recipeInline,)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_tag', 'slug', 'colour_code_tag')
    search_fields = ('title_tag',)


class Ingredients_recipeAdmin(admin.ModelAdmin):
    list_display = ('name_ingredient', 'unit_ingredient',)
    list_filter = ('name_ingredient',)
    search_fields = ('name_ingredient',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredients_recipe, Ingredients_recipeAdmin)
admin.site.register(Comment)
admin.site.register(Follow)
