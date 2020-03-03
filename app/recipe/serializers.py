from rest_framework import serializers

from ingredient.serializers import IngredientSerializer
from user.serializers import UserSerializer
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeOnlySerializer(serializers.ModelSerializer):
    difficulty = serializers.SerializerMethodField()
    ingredients = IngredientSerializer(many=True)

    @staticmethod
    def get_difficulty(obj):
        return [tup for tup in obj.DIFFICULTY_CHOICES if tup[0] == obj.difficulty][0][1]

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'difficulty', 'created', 'updated', 'ingredients']
