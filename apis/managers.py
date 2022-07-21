from datetime import datetime
# manager
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user_id, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user_id, password, **extra_fields)

    def create_superuser(self, user_id, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('create_date', datetime.now())

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user_id, password, **extra_fields)

    def get_by_natural_key(self, user_id):
        return self.get(user_id=user_id)
