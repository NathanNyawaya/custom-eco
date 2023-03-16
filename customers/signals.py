from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='default')
        instance.groups.add(group)
