from django.db import models
from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

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



class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews')
    # image = models.ImageField(
    #     upload_to='posts/', null=True, blank=True)
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        related_name='reviews', null=True
    )
    score = models.IntegerField()


    def __str__(self):
        return self.text

class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
