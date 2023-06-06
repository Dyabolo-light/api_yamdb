from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('super_user', 'super_user'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254,
                              unique=True,
                              blank=False,
                              null=False)
    role = models.CharField(max_length=15, choices=ROLES, default='user')
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class ConfirmationCode(models.Model):
    confirmation_code = models.CharField(max_length=5)
    username = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='confirmation_code',
        null=True,
    )
