from .models import ItemLiked


def get_items_liked_counter(request):
    likes_counter = 0
    try:
        items_liked = ItemLiked.objects.get(user=request.user)
        likes_counter = items_liked.quantity

    except:
        likes_counter = 0

    return dict(likes_counter=likes_counter)
