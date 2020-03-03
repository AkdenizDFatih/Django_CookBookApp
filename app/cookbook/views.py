from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from cookbook.models import Cookbook
from cookbook.serializers import CookbookSerializer, CookbookDetailedSerializer
from user.permissions import IsObjectAuthorOrReadOnly, ReadOnly


class ListCreateCookbook(GenericAPIView):
    """
    get:
    Returns all the cookbooks if no search parameters is given
    If a search parameter is given, it will return all cookbooks that contain it in their title or description

    post:
    Creates a new cookbook instance and returns it
    """

    queryset = Cookbook.objects.all()
    serializer_class = CookbookSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_string = self.request.query_params.get('search')
        if search_string:
            queryset = queryset.filter(Q(title__icontains=search_string) | Q(description__icontains=search_string))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadUpdateDeleteCookbook(GenericAPIView):
    """
    get:
    Returns a cookbook based on the given id

    patch:
    Partially updates and returns a cookbook based on the given id

    delete:
    Deletes a cookbook based on the given id and return no content status 204
    """

    queryset = Cookbook
    serializer_class = CookbookDetailedSerializer
    lookup_url_kwarg = 'cookbook_id'
    permission_classes = [IsObjectAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        cookbook = self.get_object()
        serializer = self.get_serializer(cookbook)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        cookbook = self.get_object()
        serializer = self.get_serializer(cookbook, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        cookbook = self.get_object()
        cookbook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ToggleStarringCookbook(GenericAPIView):
    """
    patch:
    Toggle starring recipe by logged in user
    """

    queryset = Cookbook
    serializer_class = CookbookSerializer
    lookup_url_kwarg = 'cookbook_id'

    def patch(self, request, *args, **kwargs):
        cookbook = self.get_object()
        user = self.request.user
        user_starred_recipe = user in cookbook.starred_by.all()
        if user_starred_recipe:
            cookbook.starred_by.remove(user)
        else:
            cookbook.starred_by.add(user)
        return Response(self.get_serializer(cookbook).data)
