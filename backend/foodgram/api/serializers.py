from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe, Tag, Ingredient, Amount
from rest_framework import serializers

User = get_user_model()


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
        fields = 'ingredient', 'dimension', 'id', 'recipe'
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

    '''
    def get_ingredients(self, obj):
        ingredients = AmountSerializer.objects.filter(recipe=obj)
        serializer = AmountSerializer(ingredient, many=True)
    '''

    class Meta:
        read_only_fields = ('author',)
        fields = '__all__'
        model = Recipe


'''
class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    # было read_only=True вместо queryset
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    def validate_following(self, following):
        if self.context.get('request').user == following:
            raise serializers.ValidationError
        return following

    class Meta:
        model = Follow
        exclude = ('id',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
'''
