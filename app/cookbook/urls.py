from django.urls import path

from cookbook.views import ListCreateCookbook, ReadUpdateDeleteCookbook, ToggleStarringCookbook

urlpatterns = [
    path('', ListCreateCookbook.as_view()),
    path('<int:cookbook_id>/', ReadUpdateDeleteCookbook.as_view()),
    path('toggle-starred/<int:cookbook_id>/', ToggleStarringCookbook.as_view())
]
