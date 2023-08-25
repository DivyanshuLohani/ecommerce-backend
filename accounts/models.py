from django.db import models
from django.contrib.auth.models import AbstractUser

AUTH_PROVIDER = (
    ('email', 'Email'),
    ('google', 'Google'),
    ('facebook', 'facebook')
)

# Create your models here.


class User(AbstractUser):

    auth_provider = models.CharField(
        choices=AUTH_PROVIDER,
        default=AUTH_PROVIDER[0][0]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'first_name']
