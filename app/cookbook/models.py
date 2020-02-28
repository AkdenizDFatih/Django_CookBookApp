from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cookbook(models.Model):
    title = models.CharField(max_length=100)

    description = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='cookbooks'
    )

    starred_by = models.ManyToManyField(
        to=User,
        verbose_name='starred by',
        related_name='starred_cookbooks',
        blank=True,
    )

    def __str__(self):
        title = f'{self.title[:30]}...' if len(self.title) > 30 else self.title
        return f'Cookbook {self.pk}: {title} by {self.author.username}'
