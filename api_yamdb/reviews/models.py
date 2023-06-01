from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('User', 'User'),
        ('Moderator', 'Moderator'),
        ('Admin', 'Admin'),

    )

    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer.'
                   'Letters, digits and @/./+/-/_ only.'),
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True,
        null=False
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=15, choices=ROLES, default='User')


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name='titles', blank=False, null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles', blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Comment(models.Model):
    pass
