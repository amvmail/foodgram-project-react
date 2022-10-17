from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
# from django.contrib.auth.tokens import default_token_generator
from recipes.models import (Amount, Favorite, Ingredient, Recipe, ShopList,
                            Subscription, Tag)
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .pagination import CustomPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import (AmountSerializer, FollowSerializer,
                          IngredientSerializer, RecipeFollowSerializer,
                          RecipeGetSerializer, RecipeSerializer,
                          TagSerializer, UsersSerializer)
# RegisterDataSerializer, UserEditSerializer
from .utils import delete, post


class AmountViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset к Tag."""
    queryset = Amount.objects.all()
    serializer_class = AmountSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('recipe', 'ingredient')
    search_fields = ('recipe', 'ingredient',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset к Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name', 'value', 'style',)
    search_fields = ('name', 'value',)


class IngredientViewSet(viewsets.ModelViewSet):
    """Viewset к Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('title', 'dimension',)
    search_fields = ('title', 'dimension',)


class RecipesViewSet(viewsets.ModelViewSet):
    """Viewset к рецептам."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('title', 'author', 'tags', 'description', 'pub_date',)
    search_fields = ('title', 'author__username',)

    def get_permissions(self):
        if self.action != 'create':
            return (IsOwnerOrReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and int(is_favorited) == 1:
            return Recipe.objects.filter(favorites__user=self.request.user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')
        if is_in_shopping_cart is not None and int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(cart__user=self.request.user)
        return Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGetSerializer
        return RecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return post(request, pk, Favorite, RecipeFollowSerializer)
        return delete(request, pk, Favorite)

    @action(detail=True, methods=['POST', 'DELETE'], )
    def shoplist(self, request, pk):
        if request.method == 'POST':
            return post(request, pk, ShopList, RecipeFollowSerializer)
        return delete(request, pk, ShopList)


class UsersViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    addition_serializer = FollowSerializer
    pagination_class = CustomPageNumberPagination

    @action(
        detail=True,
        permission_classes=[AllowAny],
        methods=['POST', 'DELETE']
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if self.request.method == 'POST':
            if Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user == author:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            follow = Subscription.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if Subscription.objects.filter(user=user, author=author).exists():
            follow = get_object_or_404(Subscription, user=user, author=author)
            follow.delete()
            return Response(
                'Подписка успешно удалена',
                status=status.HTTP_204_NO_CONTENT
            )
        if user == author:
            return Response(
                {'errors': 'Нельзя отписаться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'errors': 'Вы не подписаны на данного пользователя'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET']
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscription.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
