from django.contrib import admin

from .models import Category, Genre, Title
from users.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
