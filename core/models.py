from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .constants import GROUP_INVESTOR
from .constants import GROUP_MANAGER
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Email address")
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
        verbose_name="Username",
    )
    firebase_uid = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def in_group(self, name):
        return self.groups.filter(name=name).exists()

    def is_investor(self):
        return self.in_group(name=GROUP_INVESTOR)

    def is_manager(self):
        return self.in_group(name=GROUP_MANAGER)
