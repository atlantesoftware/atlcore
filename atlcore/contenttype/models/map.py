#coding=UTF-8
from atlcore.contenttype.models.content import Content
from atlcore.contenttype.manager import LocaleManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Map(Content):
    # fields
    embeded_map=models.TextField(_('embeded map'), blank=False)
    
    # managers    
    # default manager
    objects = models.Manager()
    objects_translated = LocaleManager()
    
    @property
    def resource(self):
        return self.embeded_map
    
    def get_absolute_url_static (self):
        """
        Crea una imagen de manera automatica del mapa de google.
        """        
        try:
            parts = self.embeded_map.split("?")
            params = parts[1]
            paramsarray = params.split('&amp;')
            if (len(paramsarray)==1):
                paramsarray = params.split('&')
            center = None
            zoom = 0
            label = ""
            for param in paramsarray:
                results = param.split('=')
                if (results[0] == "ll"):
                    center = results[1]
                if (results[0] == "hnear"):
                    center = results[1]
                if (results[0] == "z"):
                    zoom = int(results[1])
                if (results[0] == "ll"):
                    coord = results[1]
                    label = "&markers=color:blue|label:A|%s" % (coord)
            url = "http://maps.google.com/maps/api/staticmap?center=%s&zoom=%d&size=430x311&maptype=roadmap%s&sensor=false" % ( center, zoom, label)
            return url
        except:
            return None

    
    class Meta:
        app_label = 'contenttype'
        verbose_name = _('map')
        verbose_name_plural = _('maps')
