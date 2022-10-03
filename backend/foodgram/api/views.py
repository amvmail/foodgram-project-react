from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from recipes.models import Recipe, Tag, Ingredient
from users.models import User
from rest_framework import filters, viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from .permissions import IsAdmin, IsAdminOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.serializers import ValidationError

from .pagination import CustomPageNumberPagination
from .serializers import (
    TagSerializer, RecipesSerializer,
    IngredientSerializer, UserSerializer, TokenSerializer,
    UserEditSerializer,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset к Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name', 'value', 'style',)
    search_fields = ('name', 'value',)


class IngredientViewSet(viewsets.ModelViewSet):
    """Viewset к Ingredient."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('title', 'dimension',)
    search_fields = ('title', 'dimension',)


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


class SignUpViewSet(viewsets.ModelViewSet):
    @api_view(['POST'])
    @permission_classes([permissions.AllowAny])
    def signup(request):
        serializer = RegisterDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user, created = User.objects.get_or_create(
            username=serializer.validated_data['username']
        )
        if not user.is_admin:  # noqa: E712
            confirmation_code = default_token_generator.make_token(user)
            send_mail(subject='Foodgram registration',
                      message=f'Your confirmation code: {confirmation_code}',
                      from_email=None,
                      recipient_list=[user.email],)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAdmin,)
