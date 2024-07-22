from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email address")
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
        verbose_name="Username",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
