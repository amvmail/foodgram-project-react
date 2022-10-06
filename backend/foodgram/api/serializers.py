from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.validators import UniqueValidator
from recipes.models import Recipe, Tag, Ingredient, Amount, Subscription
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'name', 'value'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'title', 'dimension'
        model = Ingredient


class AmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    recipe = serializers.ReadOnlyField(source='Amount.recipe')
    ingredient = serializers.ReadOnlyField(source='ingredient.title')
    dimension = serializers.ReadOnlyField(source='ingredient.dimension')
    quantity = serializers.ReadOnlyField(source='Amount.quantity')

    class Meta:
        fields = 'id', 'ingredient', 'dimension',  'quantity', 'recipe'
        model = Amount
        validators = [
            UniqueTogetherValidator(
                queryset=Amount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True)
    ingredient = AmountSerializer(read_only=True, many=True)
    image = Base64ImageField()

    class Meta:
        read_only_fields = ('author',)
        fields = '__all__'
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(source='author.recipes.count')

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.user,
            author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeFollowSerializer(queryset, many=True).data


# class UserSerializer(serializers.ModelSerializer):
class UsersSerializer(UserSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',)


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class SendEmailSerializer(serializers.ModelSerializer):
    queryset = User.objects.all()

    class Meta:
        model = User
        fields = ('username',)


class RegisterDataSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username "me" нельзя использовать'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()