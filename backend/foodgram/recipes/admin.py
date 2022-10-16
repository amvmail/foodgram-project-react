from django.contrib import admin
from foodgram.settings import EMPTY

from .models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                     Subscription, Tag)
from users.models import User


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


@admin.register(ShopList)
class ShopList(admin.ModelAdmin):
    list_display = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    search_fields = ('user',)


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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name'
    )
    list_filter = ('email', 'first_name', 'first_name', 'last_name')
    empty_value_display = EMPTY
