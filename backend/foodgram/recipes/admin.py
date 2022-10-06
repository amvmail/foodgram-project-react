from django.contrib import admin

from .models import Amount, Ingredient, Recipe, Subscription, Tag, Favorite
from users.models import User
from foodgram.settings import EMPTY


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'role', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


class AmountInline(admin.TabularInline):
    model = Amount
    fields = ['ingredient', 'quantity']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    inlines = [AmountInline]
    list_filter = ('author', 'title', 'tags')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('value', 'style', 'name')


@admin.register(Amount)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'quantity',)
    list_display_links = ('pk', 'recipe')
    list_filter = ('recipe', 'ingredient',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
    empty_value_display = EMPTY
