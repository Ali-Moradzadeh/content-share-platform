from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import UserProfile


User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def remove_self_following(sender, **kwargs):
    if kwargs.get("action", None) == "post_add" and (instance:=kwargs.get("instance", None)):
            instance.followings.remove(instance)

m2m_changed.connect(remove_self_following, sender=UserProfile.followings.through)