#coding=UTF-8
from atlcore.permissions import models as permissions_app

from django.db.models import get_models, signals

def atl_create_everyone_group(app, created_models, verbosity=2, **kwargs):
    from django.contrib.auth.models import Group
    from django.core.management import call_command
    if Group in created_models:
        call_command("atl_create_everyone_group")

signals.post_syncdb.connect(
    atl_create_everyone_group,
    sender=permissions_app,
    dispatch_uid = "atlcore.permissions.management.atl_create_everyone_group"
)