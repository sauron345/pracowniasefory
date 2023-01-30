from django.contrib import admin
from .models import Item, Category, ItemLiked


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']
    search_fields = ['name', 'created_by', 'created_at', 'updated_at']

    class Meta:
        ordering = ('-created_at',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'owner', 'is_available']
    search_fields = ['name', 'category', 'owner']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_available']
    list_per_page = 10

    class Meta:
        ordering = ('-created_at',)


@admin.register(ItemLiked)
class ItemLikedAdmin(admin.ModelAdmin):
    list_display = ['user', 'quantity', 'created_at']
    search_fields = ['user', 'items']
    readonly_fields = ['quantity']
    list_per_page = 10

    class Meta:
        ordering = ('-created_at',)


admin.site.site_header = 'Pracownia Sefory'