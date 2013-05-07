#encoding=UTF-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.http import HttpResponse
from django.conf.urls import patterns, url
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from dajax.core import Dajax

from atlcore.settings import JSLIBRARY
from atlcore.vcl.components import Component
from atlcore.utils.email import send_email 
from captcha.fields import CaptchaField

from dajaxice.utils import deserialize_form
from dajaxice.decorators import dajaxice_register

class ContactFormWithCaptcha(forms.Form):
    
    name = forms.CharField(label=_("Name"), max_length=50)
    email = forms.EmailField(label=_("Email address"), required=True)
    message = forms.CharField(label=_('Comment'), widget=forms.Textarea, max_length=200)
    
    #captcha = CaptchaField(error_messages = {   'required': 'Este campo es requerido.',     'invalid': 'Captcha incorrecto.', })

class AtlContactForm(Component):
    
    def __init__(self, data_provider=None, version=None, skin=None):
        super(AtlContactForm, self).__init__(data_provider, version, skin)
        self.title = 'Contacto' #Title show in h2 html tag if not None
        self._theme = 'base'
        self.form = ContactFormWithCaptcha()
        self.submit_button_text = "Enviar"
        self._librarylist += [{'lib_jquery' : JSLIBRARY['lib_jquery']}]
        self._librarylist += [{'lib_dajax' : 'dajax/jquery.dajax.core.js'}]
        if skin: 
            self._librarylist += [{'lib_atlcontactform' : 'skins/%s/vcl/atlcontactform/base/js/script.js' % skin}]
        else:
            self._librarylist += [{'lib_atlcontactform' : 'vcl/atlcontactform/base/js/script.js'}]
            
    @classmethod
    def urls(cls):
        urlpatterns = patterns('',
            url(r'^atlcontactform/$',
                AtlContactForm.contact,
                name='AtlContactForm.contact'),
        )
        return urlpatterns
    
    
    @classmethod     
    @dajaxice_register(method='POST')  
    def contact(request, form):
        dajax = Dajax()
        if request.method == 'POST':
            form = ContactFormWithCaptcha(deserialize_form(form))
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']
                email_subject = 'Contacto de lec572'
                email_text_body = 'El usuario %s (%s) ha enviado el siguiente mensaje: %s' % (name, email, message)
                email_html_body = '<p>El usuario %s(%s) ha enviado el siguiente mensaje:</p><p>%s</p>' % (name, email, message)
                send_email(email_subject, email_text_body, email_html_body, 'juangarciamolla@gmail.com')
                dajax.alert('El mensaje ha sido enviado')
                dajax.remove_css_class('#AtlContactForm_form input', 'error')
                dajax.assign('#id_name', 'value', 'Nombre')
                dajax.assign('#id_email', 'value', 'nombre@dominio.com')
                dajax.assign('#id_message', 'value', 'Mensaje')
            else:
                dajax.alert('Corrija los errores en el formulario')
                dajax.remove_css_class('#AtlContactForm_form input', 'error')
                for error in form.errors:
                    dajax.add_css_class('#id_%s' % error, 'error')
            return dajax.json()
    