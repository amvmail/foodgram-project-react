from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from recipes.models import Recipe, Tag, Amount, Ingredient
from rest_framework import filters, viewsets
from .pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view

from .serializers import TagSerializer, RecipesSerializer, IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset к Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@api_view(['GET', 'POST'])
class IngredientViewSet(viewsets.ModelViewSet):
    """Viewset к Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)


# @api_view(['GET', 'POST'])
class RecipesViewSet(viewsets.ModelViewSet):
    """Viewset к рецептам."""
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('title', 'author', 'tags', 'description', 'pub_date',)
    search_fields = ('title', 'author__username',)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
