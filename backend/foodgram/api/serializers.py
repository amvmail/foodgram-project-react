from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from recipes.models import Amount, Ingredient, Recipe, Subscription, Tag
from users.models import User

from .utils import amount_create


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'name', 'value'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = 'title', 'dimension'
        model = Ingredient


class AmountGetSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    title = serializers.ReadOnlyField(source='ingredient.title')
    dimension = serializers.ReadOnlyField(
        source='ingredient.dimension'
    )

    class Meta:
        model = Amount
        fields = ('id', 'title', 'dimension', 'quantity')
        validators = [
            UniqueTogetherValidator(
                queryset=Amount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class AmountSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(write_only=True, min_value=1)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = Amount
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Amount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(max_length=None, use_url=True)
    cooking_time = serializers.IntegerField(min_value=1)

    class Meta:
        read_only_fields = ('id', 'author', 'tags')
        fields = '__all__'
        model = Recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_list = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients_list) != len(set(ingredients_list)):
            raise serializers.ValidationError(
                'Ингредиент был выбран несколько раз'
            )
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        amount_create(ingredients_data, Amount, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in self.validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in self.validated_data:
            ingredients_data = validated_data.pop('ingredients')
            amount_set = Amount.objects.filter(
                recipe__id=instance.id)
            amount_set.delete()
            amount_create(ingredients_data, Amount, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields.pop('tags')
        representation = super().to_representation(instance)
        representation['ingredients'] = AmountGetSerializer(
            Amount.objects.filter(recipe=instance), many=True
        ).data
        representation['tags'] = TagSerializer(
            instance.tags, many=True
        ).data
        return representation


class RecipeFollowSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    '''Подписка.'''
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
        return Subscription.objects.filter(
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


class RecipeGetSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True)
    ingredients = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'title', 'description', 'ingredients', 'tags',
                  'cooking_time', 'is_favorited', 'is_in_shopping_cart',
                  'image')
        read_only_fields = ('id', 'author',)

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorite_recipes.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shoplist.filter(user=user).exists()

    def get_ingredients(self, obj):
        amounts = Amount.objects.filter(recipe=obj)
        return AmountGetSerializer(amounts, many=True).data


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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'id', 'password')


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
