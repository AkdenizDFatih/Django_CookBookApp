from django.urls import path

from recipe.views import ListCreateRecipe, ReadUpdateDeleteRecipe, ToggleStarringRecipe

urlpatterns = [
    path('', ListCreateRecipe.as_view()),
    path('<int:recipe_id>/', ReadUpdateDeleteRecipe.as_view()),
    path('toggle-starred/<int:recipe_id>/', ToggleStarringRecipe.as_view())
]
