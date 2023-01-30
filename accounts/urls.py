from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('change_password_validate/<uidb64>/<token>', views.change_password_validate, name='change_password_validate'),
    path('change_password/', views.change_password, name='change_password'),
]
