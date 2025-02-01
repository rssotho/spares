from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser
)
import global_app.constants as constant


class UserManager(BaseUserManager):

    def create_user(
        self,
        email: str = None,
        role_id: int = None,
        password: str = None,
        phone_number: str = None,
        **extra_fields
    ):

        if not email and not phone_number:

            raise ValueError(_('Users must have an email address or phone number'))

        if email:
            email = self.normalize_email(email)

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('phone_number', phone_number)
        extra_fields.setdefault('role_id', role_id)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        email: str = None,
        password: str = None,
        last_name: str = None,
        first_name: str = None,
        phone_number: str = None,
        **extra_fields
    ):
        if not email:
            raise ValueError(_('Superuser must have an email address'))
        if not password:
            raise ValueError(_('Superuser must have a password'))
        if not first_name:
            raise ValueError(_('Superuser must have a first name'))
        if not last_name:
            raise ValueError(_('Superuser must have a last name'))

        role, created = Role.objects.get_or_create(
            role=constant.SYSTEM_ADMIN
        )
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role_id', role.id)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('phone_number', phone_number)
        extra_fields.setdefault('first_name', first_name)
        extra_fields.setdefault('last_name', last_name)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(
            email=email,
            password=password,
            **extra_fields
        )


class Role(models.Model):

    role = models.CharField(max_length=100)


class User(AbstractBaseUser):

    password = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=255, unique=True, null=True, blank=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):

        return self.email


class Country(models.Model):

    country = models.CharField(max_length=255)


class Province(models.Model):

    province = models.CharField(max_length=255)


class Gender(models.Model):

    gender = models.CharField(max_length=255)


class Race(models.Model):

    race = models.CharField(max_length=255)
    other_race = models.CharField(max_length=255)


class OneTimePin(models.Model):

    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Profile(models.Model):

    town = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=4)
    street_address = models.CharField(max_length=255)

    race = models.ForeignKey(Race, on_delete=models.PROTECT)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
