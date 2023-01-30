from django.shortcuts import render
from items.models import Item


def dashboard(request):
    if request.user.is_authenticated:
        items = Item.objects.filter(is_available=True).order_by('-created_at')
        return render(request, 'dashboard.html', {'items': items})
    else:
        return render(request, 'dashboard.html')
