from django import forms
from captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _

class ContactFormWithCaptcha(forms.Form):
    
    name = forms.CharField(label=_("Name"), max_length=50)
    email = forms.CharField(label=_("Email address"), required=False)
    country = forms.CharField(label=_("Country"), max_length=50, required=False)
    message = forms.CharField(label=_('Comment'), widget=forms.Textarea, max_length=200)
    
    captcha = CaptchaField(error_messages = {   'required': 'Este campo es requerido.',     'invalid': 'Captcha incorrecto.', })
    
class UserSubscriber(forms.Form):
    email = forms.EmailField()