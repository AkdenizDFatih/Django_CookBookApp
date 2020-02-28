from rest_framework import serializers

from user.serializers import UserSerializer
from cookbook.models import Cookbook


class CookbookSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Cookbook
        fields = '__all__'
