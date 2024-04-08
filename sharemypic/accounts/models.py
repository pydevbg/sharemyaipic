from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib import auth

from sharemypic.accounts.managers import SMPUserManager

# Create your models here.

use_in_migrations = True



class SMPUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    MAX_USERNAME_LENGTH = 150

    username = models.CharField(
        _("username"),
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "username"
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )

    objects =SMPUserManager()


class Profile(models.Model):
    MAX_FIRST_NAME_LENGTH = 30
    MAX_LAST_NAME_LENGTH = 30

    first_name = models.CharField(max_length=MAX_FIRST_NAME_LENGTH,
                                  blank=True, null=True,
                                  verbose_name='First Name')

    last_name = models.CharField(max_length=MAX_LAST_NAME_LENGTH,
                                 blank=True, null=True)

    email = models.EmailField( blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    profile_pic = models.ImageField(blank=True, null=True, upload_to='profile_pics/')

    user = models.OneToOneField(SMPUser, primary_key=True, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # Delete the associated user when deleting the profile
        self.user.delete()
        super().delete(*args, **kwargs)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if not self.first_name and not self.last_name:
            return f""
        return f"{self.first_name} or {self.last_name}"
