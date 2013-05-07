#coding=UTF-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.widgets import Input
from django.utils.safestring import mark_safe

from atlcore import settings as atlsettings
        
class AtlAutocompleteWidget(Input):
    
    models = None
    
    def __init__(self, attrs=None, models=None):
        super(AtlAutocompleteWidget, self).__init__(attrs)
        self.models = models
    
    def render(self, name, value, attrs=None):
        html = super(AtlAutocompleteWidget, self).render(name, value, attrs)
        if self.models is None:
            return html
        else:
            models = ','.join(self.models)
        url = reverse('json-objects', args=[models])
        return html + mark_safe(u'''
            <script type="text/javascript">  
            jQuery(function() {
                function set_value(selected, n){
                    if (selected != "") {
                        var a = selected.split('_');
                        var o_id = a[3];
                        var ct_id = a[1];
                        var o = document.getElementById('id_object' + n + '_id');
                        o.value = o_id;
                        var ct = document.getElementById('id_content_type' + n + '_id');
                        ct.value = ct_id;
                    }
                }            
                jQuery( "#%s" ).autocomplete({
                    source: "%s",
                    minLength: 2,
                    select: function( event, ui ) {
                        set_value(ui.item ? ui.item.id : "", this.id[this.id.length-1]);
                    }
                });
            });
            </script>        
            ''' %(attrs['id'], url))
    
    class Media:
        css = {
            'all': (
                atlsettings.MEDIA_URL + 'relations/css/jquery-ui/base/jquery.ui.all.css',
                atlsettings.MEDIA_URL + 'relations/css/autocomplete.css',
            )
        }
        js = (
            atlsettings.MEDIA_URL + 'relations/js/jquery.js',
            atlsettings.MEDIA_URL + 'relations/js/jquery.ui.core.js',
            atlsettings.MEDIA_URL + 'relations/js/jquery.ui.widget.js',
            atlsettings.MEDIA_URL + 'relations/js/jquery.ui.position.js',
            atlsettings.MEDIA_URL + 'relations/js/jquery.ui.autocomplete.js',        
        )