

from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.forms.util import flatatt
from atlcore import base_conf

class LinkContentInput(AdminTextInputWidget):
    
    class Media:
        js = (
#              base_conf.MEDIA_URL + "common/tiny_mce/tiny_mce_popup.js",
#              base_conf.MEDIA_URL + "common/tiny_mce/utils/mctabs.js",
#              base_conf.MEDIA_URL  + "common/tiny_mce/utils/validate.js",
              "/static/common/widgets/linkcontentinput/js/LinkDialogForLinks.js",
)
        
        



    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s rel="esto" /><input type="button" id="atlbrowsercontent-button" name="atlbrowsercontent-button" value="Buscar en Contenidos" /> <script type="text/javascript">jQuery(function() { LinkDialog.init();});</script> ' % flatatt(final_attrs))

