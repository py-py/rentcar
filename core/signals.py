from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .constants import GROUPS


@receiver(post_migrate)
def init_groups(sender, **kwargs):
    for group_id, group_name in GROUPS:
        Group.objects.update_or_create(id=group_id, defaults={"name": group_name})
