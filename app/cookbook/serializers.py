from rest_framework import serializers

from recipe.serializers import RecipeOnlySerializer
from user.serializers import UserSerializer
from cookbook.models import Cookbook


class CookbookSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Cookbook
        fields = ['title', 'description', 'created', 'updated', 'author', 'starred_by']


class CookbookDetailedSerializer(CookbookSerializer):
    recipes = RecipeOnlySerializer(many=True)
    amount_of_recipes = serializers.SerializerMethodField()

    @staticmethod
    def get_amount_of_recipes(obj):
        return obj.recipes.all().count()

    class Meta:
        model = Cookbook
        fields = CookbookSerializer.Meta.fields + ['recipes', 'amount_of_recipes']
