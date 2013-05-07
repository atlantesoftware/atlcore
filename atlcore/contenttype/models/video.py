#coding=UTF-8
#from atlcore.settings import VIDEO_SOURCES_CHOICES, DEFAULT_VIDEO_SOURCE
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager
from atlcore.libs.stdimage import StdImageField


IMAGE_SIZE = (640, 480)
THUMBNAIL_SIZE = (100, 100, True)


VIDEO_SOURCES_CHOICES = (
    ('local', _('Local file')),
    ('ftp', _('FTP Folder')),
    ('external', _('External URL')),
    ('embeded', _('Embeded video')),
)

DEFAULT_VIDEO_SOURCE = VIDEO_SOURCES_CHOICES[0][0]

class Video(Content):
    
    # fields    
    video=models.FileField (_("video"), upload_to='uploadtmp', blank=True)
    video_url=models.FilePathField(_('video from ftp folder'), path='%svideosftp' %settings.MEDIA_ROOT, blank=True, max_length=256)
    external_url=models.CharField(_('external URL'), blank=True, max_length=256)
    video_source=models.CharField(_("file source"), max_length=20, choices=VIDEO_SOURCES_CHOICES, default=DEFAULT_VIDEO_SOURCE)
    embeded_video=models.TextField(_('embeded video'), blank=True)
    thumbnail = StdImageField(upload_to='videos/thumb', blank=True)
   # image=thumbnail
    x_aspect_ratio = models.FloatField(_('x aspect ratio'), blank=True, null=True)
    y_aspect_ratio = models.FloatField(_('y aspect ratio'), blank=True, null=True)
    body = models.TextField(_('body'))
    
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        
    #def save(self):
    #    super(Video, self).save()
        #str_thumb = str(video.thumbnail)
        #   from atlcore.utils.video import takethumbnailfromvideo(self.video, )
        
    def get_absolute_thumbnail_url(self):
        return "%s/%s" % (settings.MEDIA_URL, self.thumbnail)   
    
            
            