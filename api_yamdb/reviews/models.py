from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )


class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    author = models.CharField(max_length=200)
    category = models.OneToOneField(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name='titles', blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ['-pub_date']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
