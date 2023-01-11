from django.contrib import admin
from .models import Item, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']
    search_fields = ['name', 'created_by', 'created_at', 'updated_at']

    class Meta:
        ordering = ('-created_at',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'owner', 'is_active']
    search_fields = ['name', 'category', 'owner']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    list_per_page = 10

    class Meta:
        ordering = ('-created_at',)
