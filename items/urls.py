from django.urls import path
from . import views

urlpatterns = [
    path('liked_products/', views.liked_products, name="liked_products"),
    path('add_liked_product/<int:item_id>/', views.add_liked_product, name="add_liked_product"),
    path('delete_liked_product/<int:item_id>/', views.delete_liked_product, name="delete_liked_product"),
    path('item_details/<int:item_id>/', views.item_details, name='item_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:item_id>/', views.edit_product, name='edit_product'),
]