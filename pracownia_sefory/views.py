from django.shortcuts import render
from items.models import Item


def dashboard(request):
    if request.user.is_active and request.user.is_authenticated:
        items = Item.objects.all()
        return render(request, 'dashboard.html', {'items': items})
    else:
        return render(request, 'dashboard.html')
