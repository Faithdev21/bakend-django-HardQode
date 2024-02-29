from typing import Tuple

from django.contrib import admin

from products.models import Access, Group, Lesson, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display: Tuple = (
        'id', 'creator', 'title',
        'start_date', 'cost',
        'min_group_users', 'max_group_users',
    )
    search_fields: Tuple = ('id', 'title', 'amount',)
    list_filter: Tuple = (
        'id', 'start_date', 'cost',
        'min_group_users', 'max_group_users',
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter: Tuple = ('id', 'name',)
    list_display: Tuple = ('id', 'name', 'link',)
    search_fields: Tuple = ('id', 'name', 'link',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_filter: Tuple = ('id', 'name',)
    list_display: Tuple = ('id', 'name',)
    search_fields: Tuple = ('id', 'name',)


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    pass
