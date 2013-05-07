#coding=UTF-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext, ugettext_lazy as _

from atlcore import settings as atlcore_settings
from atlcore.libs.stdimage import StdImageField
from atlcore.utils.guid import get_guid


class AtlUserProfile(models.Model):
    user = models.OneToOneField(User)
    biography = models.TextField(_('biography'), blank=True)
    #country = models.ForeignKey(Country, related_name='%(class)s_related', blank=True, null=True)
    photo = StdImageField(upload_to='nodes/images', blank=True, size=atlcore_settings.IMAGE_SIZE, thumbnail_size=atlcore_settings.THUMBNAIL_SIZE)
    facebook = models.CharField('facebook', blank=True, max_length=256)
    twitter = models.CharField('twitter', blank=True, max_length=256)
    activation_code = models.CharField(max_length=36, default=get_guid)
    
    def __unicode__(self):
        return u'%s %s' %(self.user.username, ugettext('profile'))    
    
    def get_twitter_url(self):
        return "http://twitter.com/@%s" % self.twitter
    
def user_data_creation(sender, instance, created, **kwargs):
    if created:
        AtlUserProfile.objects.create(user=instance)
     
post_save.connect(user_data_creation, sender=User)
