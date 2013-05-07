#coding=UTF-8
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Group
from models import AtlUserPermission, AtlGroupPermission

class AtlPermissionForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), empty_label=None)
    user_read = forms.BooleanField(label = _('Read'))
    user_write = forms.BooleanField(label = _('Write'))
    user_execute = forms.BooleanField(label = _('Execute'))
    Group = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label=None)
    group_read = forms.BooleanField(label = _('Read'))
    group_write = forms.BooleanField(label = _('Write'))
    group_execute = forms.BooleanField(label = _('Execute'))
    
class AtlUserPermissionForm(forms.ModelForm):    
    class Meta:
        model = AtlUserPermission
        
class AtlGroupPermissionForm(forms.ModelForm):    
    class Meta:
        model = AtlGroupPermission
