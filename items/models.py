from django.db import models
from accounts.models import User

request_object = ""


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=30, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"
        verbose_name = "category"

    def __str__(self):
        return self.name


class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_item')
    name = models.CharField(max_length=40)
    slug = models.SlugField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to=f"items/item_image")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __init__(self, *args, **kwargs):
    #     super(Item, self).__init__(*args, **kwargs)
    #     self.owner = User.objects.get(id=request_object.user.id)

    def __str__(self):
        return self.name


class ItemLiked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='liked_items')
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Items Liked"
        verbose_name = "Item Liked"

    def __unicode__(self):
        return self.quantity
