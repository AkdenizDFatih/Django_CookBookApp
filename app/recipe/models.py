from django.contrib.auth import get_user_model
from django.db import models

from cookbook.models import Cookbook
from ingredient.models import Ingredient

User = get_user_model()


class Recipe(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField()

    DIFFICULTY_CHOICES = [
        (1, 'Easy'),
        (2, 'Intermediate'),
        (3, 'Hard')
    ]

    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    cookbooks = models.ManyToManyField(
        to=Cookbook,
        related_name='recipes',
        blank=True,
    )

    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name='recipes',
        blank=True,
    )

    starred_by = models.ManyToManyField(
        to=User,
        verbose_name='starred by',
        related_name='starred_recipes',
        blank=True,
    )

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    def __str__(self):
        title = f'{self.title[:30]}...' if len(self.title) > 30 else self.title
        return f'Recipe {self.pk}: {title} by {self.author.username}'
