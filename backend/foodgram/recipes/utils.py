from .models import ShopList, Tag


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            ingredient_item = key.split('_')[1]
            ingredients[request.POST[key]] = request.POST[
                'valueIngredient_' + ingredient_item]
    return ingredients


def get_shoplist(request):
    shoplist_count = None
    if request.user.is_authenticated:
        shoplist_count = ShopList.objects.filter(
            user=request.user).count()
    return {'shoplist_count': shoplist_count}


def define_tags(request):
    all_tags = Tag.objects.all()
    request_tags = request.GET.getlist('tags')

    active_tags = {}

    for tag in all_tags:
        if tag.value in request_tags:
            active_tags[tag.value] = {'status': True,
                                      'name': tag.name,
                                      'style': tag.style}
        else:
            active_tags[tag.value] = {'status': False,
                                      'name': tag.name,
                                      'style': tag.style}
    return active_tags, request_tags, all_tags
