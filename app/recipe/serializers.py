from rest_framework import serializers

from user.serializers import UserSerializer
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_difficulty(self, obj):
        return obj.get_display
