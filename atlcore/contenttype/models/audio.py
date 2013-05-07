#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.utils.translation import ugettext_lazy as _
from django.db import models

class Audio(Content):
    
    # fields
    audio = models.FileField (_("audio"), upload_to="audios/", blank=True)
    mp3_file = models.FileField (_("audio mp3"), upload_to="audios_mp3/", blank=True, default='')
    ogg_file = models.FileField (_("audio ogg"), upload_to="audios_ogg/", blank=True, default='')
    wav_file = models.FileField (_("audio wav"), upload_to="audios_wav/", blank=True, default='') 
    #FileBrowseField(_('audio file'), max_length=256, directory="audios/", extensions=settings.AUDIOS_EXT, format='Audio')
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('audio')
        verbose_name_plural = _('audios')