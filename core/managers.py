from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        user = self.model(
            email=self.normalize_email(email),
            username=GlobalUserModel.normalize_username(username) if username else None,
            **extra_fields,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        return super().create_user(
            email=email,
            password=password,
            username=username,
            **extra_fields,
        )

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        return super().create_superuser(
            email=email,
            password=password,
            username=username,
            **extra_fields,
        )
