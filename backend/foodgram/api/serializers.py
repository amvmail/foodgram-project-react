from django.contrib.auth import get_user_model
from recipes.models import Recipe, Tag, Ingredient, Amount
from rest_framework import serializers

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class AmountSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Amount


class RecipesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tag = TagSerializer(many=True)
    ingredient = IngredientSerializer(many=True)
    # ingredient = Amount(many=True)

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
