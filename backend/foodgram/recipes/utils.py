from .models import ShopList


def get_shoplist(request):
    shoplist_count = None
    if request.user.is_authenticated:
        shoplist_count = ShopList.objects.filter(
            user=request.user).count()
    return {'shoplist_count': shoplist_count}
