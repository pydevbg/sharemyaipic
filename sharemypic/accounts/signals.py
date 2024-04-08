from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from sharemypic.accounts.models import Profile

UserModel = get_user_model()

#this code ensures that every time a new user is created in the system,
# a corresponding Profile object is automatically created as well,
# providing a seamless association between users and their profiles.
@receiver(post_save, sender=UserModel)
def user_created(sender,instance, created, **kwargs):

    if not created:
        return

    Profile.objects.create(user=instance)
