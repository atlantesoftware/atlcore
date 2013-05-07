#coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from atlcore.contenttype.models import Video
from atlcore.plugins.atlplugin_jwplayer import plugin_settings


class AtlJWPlayer(CMSPlugin):
    title = models.CharField('Title', max_length=256, default=None, null=True)
    video = models.ForeignKey(Video, related_name = 'plugins')
    width = models.PositiveSmallIntegerField(_('width'), default=plugin_settings.VIDEO_WIDTH)
    height = models.PositiveSmallIntegerField(_('height'), default=plugin_settings.VIDEO_HEIGHT)

    auto_play = models.BooleanField(_('auto play'), default=plugin_settings.VIDEO_AUTOPLAY)


def __unicode__(self):
        return self.video.title


