from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'Ingredient id {self.pk}: {self.name}'
