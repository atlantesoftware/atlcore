#coding=UTF-8
from atlcore.aspect.models import Aspect

from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

class AspectForm(forms.ModelForm):    
    class Meta:
        model = Aspect

    def clean(self):
        cleaned_data = self.cleaned_data
        parent = cleaned_data.get("parent")
        if parent:
            err = False
            if parent != self.instance:
                ancestors = parent.get_ancestors()
                if self.instance in ancestors:
                    err = True
            else:
                err = True
            if err:
                msg = _("Recursive nesting")
                self._errors["parent"] = ErrorList([msg])
                del cleaned_data["parent"]      
        return cleaned_data