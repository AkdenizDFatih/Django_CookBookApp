from rest_framework import serializers

from ingredient.serializers import IngredientSerializer
from user.serializers import UserSerializer
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'title', 'description', 'difficulty', 'created', 'updated', 'cookbooks', 'ingredients', 'starred_by']


class RecipeOnlySerializer(serializers.ModelSerializer):
    difficulty = serializers.CharField(source='get_difficulty_display')
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'difficulty', 'created', 'updated', 'ingredients']
