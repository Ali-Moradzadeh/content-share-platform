from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from .utility import send_signup_confirmation_email
from constants.errors import (
    PASSWORD_HAS_NO_NUMBER,
    PASSWORD_HAS_NO_UPPERCASE,
    PASSWORD_HAS_NO_SPECIAL
    )
from constants.statics import SPECIAL_CHARACTERS


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, phone_number=None, **extra_fields):
        if not username:
            raise ValueError('The Username field is required')
        if not any(char.isdigit() for char in password):
            raise ValidationError(PASSWORD_HAS_NO_NUMBER)
        if not any(char.isupper() for char in password):
            raise ValidationError(PASSWORD_HAS_NO_UPPERCASE)
        if not any(char in SPECIAL_CHARACTERS for char in password):
            raise ValidationError(PASSWORD_HAS_NO_SPECIAL)

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        send_signup_confirmation_email(user.email)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

