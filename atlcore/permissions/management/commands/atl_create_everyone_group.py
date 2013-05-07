#coding=UTF-8
"""
Management utility to create everyone group.
"""
from atlcore.contenttype.models import Folder
from atlcore.permissions.models import AtlGroupPermission, READ

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

class Command(BaseCommand):
    help = 'Used to create a everyone group.'

    def handle(self, *args, **options):
        try:
            everyone, created = Group.objects.get_or_create(name='Everyone')
        except:
            raise CommandError(_("Everyone group was not created."))
        try:
            profiles, is_created = Folder.objects.get_or_create_profiles_folder()       
        except:
            pass
        else:
            qs = AtlGroupPermission.objects.filter_for_object(profiles).filter(group=everyone)
            if qs:
                qs.update(codename=unicode(READ))
            else:
                AtlGroupPermission.objects.create(content_object=profiles, group=everyone, codename=unicode(READ))
        print _("Everyone group was created successfully.")
