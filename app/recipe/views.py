from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer
from user.permissions import IsObjectAuthorOrReadOnly, ReadOnly


class ListCreateRecipe(ListCreateAPIView):
    """
    get:
    Returns all the cookbooks

    post:
    Creates a new cookbook instance and returns it
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    permission_classes = [IsAuthenticated | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReadUpdateDeleteRecipe(RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a recipe based on the given id

    put:
    Updates and returns a recipe based on the given id

    patch:
    Partially updates and returns a recipe based on the given id

    delete:
    Deletes a recipe based on the given id and return no content status 204
    """

    queryset = Recipe
    serializer_class = RecipeSerializer
    lookup_url_kwarg = 'recipe_id'
    permission_classes = [IsObjectAuthorOrReadOnly]


class ToggleStarringRecipe(GenericAPIView):
    """
    patch:
    Toggle starring recipe by logged in user
    """

    queryset = Recipe
    serializer_class = RecipeSerializer
    lookup_url_kwarg = 'recipe_id'

    def patch(self, request, *args, **kwargs):
        recipe = self.get_object()
        user = self.request.user
        user_starred_recipe = user in recipe.starred_by.all()
        if user_starred_recipe:
            recipe.starred_by.remove(user)
        else:
            recipe.starred_by.add(user)
        return Response(self.get_serializer(recipe).data)
