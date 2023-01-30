from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from items.models import ItemLiked, Item
from django.http import JsonResponse, HttpResponse
from django.db.models import Prefetch
from .context_processors import get_items_liked_counter
from .forms import AddItemForm, EditItemForm
from django.template.defaultfilters import slugify
from django.contrib import messages


@login_required(login_url='login')
def liked_products(request):
    items_liked = ItemLiked.objects.filter(user=request.user)

    return render(request, 'items/liked_products.html', {'items_liked': items_liked})


@login_required(login_url='login')
def add_liked_product(request, item_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        user = User.objects.get(id=request.user.id)

        try:
            # We want to get product which was added as liked product by user at the moment
            item = Item.objects.get(id=item_id)

            try:
                # We want to get user's added products
                items_liked = ItemLiked.objects.get(user=user)

                try:
                    # We check if user already has the product which was clicked at the moment
                    items_liked = ItemLiked.objects.get(items__in=[item], user=user)

                    if items_liked:
                        return JsonResponse({'status': 'warning',
                                             'quantity': get_items_liked_counter(request)['likes_counter'],
                                             'message': 'You have already added this product to your list!'})
                except:
                    # We want to add the product to our items liked by user
                    items_liked.items.add(item)
                    items_liked.quantity += 1
                    items_liked.save()
                    return JsonResponse({'status': 'success',
                                         'quantity': get_items_liked_counter(request)['likes_counter'],
                                         'message': 'You have added new item in your liked products!'})

            except:
                # If user don't have items liked we want to create it
                items_liked = ItemLiked.objects.create(user=user, quantity=1)
                items_liked.items.add(item)
                items_liked.save()
                return JsonResponse({'status': 'success',
                                     'quantity': get_items_liked_counter(request)['likes_counter'],
                                     'message': 'You added the first item in your liked products!'})
        except:
            # item with id from item_id is not exists
            return JsonResponse({'status': 'error', 'message': f'Item with id: {item_id} does not exist!'})
    else:
        return HttpResponse('Invalid request')


@login_required(login_url='login')
def delete_liked_product(request, item_id):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        user = User.objects.get(id=request.user.id)

        try:
            item = Item.objects.get(id=item_id)

            items_liked = ItemLiked.objects.get(items__in=[item], user=user)

            if items_liked:
                items_liked.items.remove(item)
                items_liked.quantity -= 1
                items_liked.save()
                return JsonResponse({'status': 'success',
                                     'quantity': get_items_liked_counter(request)['likes_counter'],
                                     'message': f'You delete item with id: {item_id} from liked items!'})
        except:
            return JsonResponse({'status': 'error', 'message': f'Item with id: {item_id} does not exist!'})

    else:
        return HttpResponse('Invalid request')


def item_details(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        item = None

    return render(request, 'items/item_details.html', {'item': item})


def add_product(request):
    owner = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = AddItemForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            name = form.cleaned_data['name']
            item.owner = owner
            item.save()
            item.slug = slugify(name) + "-" + str(item.id) + "-" + str(request.user.id)
            item.save()
            messages.success(request, 'You added new product!')
            return redirect('dashboard')
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{error}")
            return redirect('add_product')

    else:
        form = AddItemForm()

    return render(request, 'items/add_product.html', {'form': form, 'owner': owner})


def edit_product(request, item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Item.DoesNotExist:
        messages.error(request, f"Item with id: {item_id} does not exists!")
        return redirect('dashboard')

    owner = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = EditItemForm(instance=item, files=request.FILES, data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully edited your product!')
            return redirect('dashboard')
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{error}")
            return redirect('dashboard')

    else:
        form = EditItemForm(instance=item)

    return render(request, 'items/edit_product.html', {'form': form, 'owner': owner})
