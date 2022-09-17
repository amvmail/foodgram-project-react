from django.contrib import admin

from .models import Tag, Recipe, Comment, Follow


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'tag')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('tag',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
admin.site.register(Follow)
