#coding=UTF-8
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.forms.util import ErrorList
from django.utils.translation import ugettext as _

from atlcore.relations.models import AtlRelation, AtlRelationsInstance
from atlcore.relations.widgets import AtlAutocompleteWidget

class AtlRelationsInstanceForm(forms.ModelForm):
    
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList, label_suffix=':', empty_permitted=False, instance=None):
        super(AtlRelationsInstanceForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance)
        if data is None and instance is not None and (not initial or '_popup' in initial):
            if initial is None: initial = {}
            if not 'relation' in initial: initial['relation']=instance.relation_id
            if '_popup' in initial: self.fields['readonly'].initial = instance.relation.title
        if initial is not None and 'relation' in initial:
            r_id = initial['relation']
            obj = None
            obj_position = None
            obj_id = None
            if 'obj1_id' in initial:
                obj_position = 1
                obj_id = initial['obj1_id']
            elif 'obj2_id' in initial:
                obj_position = 2
                obj_id = initial['obj2_id']
            if obj_position is not None and 'ct_id' in initial:
                try:
                    obj = ContentType.objects.get(pk=initial['ct_id']).get_object_for_this_type(pk=obj_id)
                except (MultipleObjectsReturned, ObjectDoesNotExist):
                    pass
            try:
                r = AtlRelation.objects.get(pk=r_id)
                if '_popup' in initial:
                    self.fields['readonly'].initial = r.title
                init1 = init2 = None
                if obj_position == 2:
                    cts2 = r.content_types_group2.all()                    
                    stop = False
                    for ct in cts2:
                        model = ct.model_class()
                        if '_popup' in initial and obj is not None and obj in model.objects.all():
                            self.fields['readonly_obj2'].initial = obj.title
                            self.fields['object2_id'].initial = obj.id
                            self.fields['content_type2_id'].initial = ct.id
                            stop = True
                            break
                    if not stop:
                        models2 = []
                        for ct in cts2:
                            models2.append(ct.model)                    
                        self.fields['object2'] = forms.CharField(widget=AtlAutocompleteWidget(models=models2), required=False)
                else:
                    cts2 = r.content_types_group2.all()
                    models2 = []                                        
                    for ct in cts2:
                        models2.append(ct.model)                    
                    self.fields['object2'] = forms.CharField(widget=AtlAutocompleteWidget(models=models2), required=False)                    
                if obj_position == 1:
                    cts1 = r.content_types_group1.all()
                    stop = False
                    for ct in cts1:
                        model = ct.model_class()
                        if '_popup' in initial and obj is not None and obj in model.objects.all():
                            self.fields['readonly_obj1'].initial = obj.title
                            self.fields['object1_id'].initial = obj.id
                            self.fields['content_type1_id'].initial = ct.id
                            stop = True
                            break
                    if not stop:
                        models1 = []
                        for ct in cts1:
                             models1.append(ct.model)                    
                        self.fields['object1'] = forms.CharField(widget=AtlAutocompleteWidget(models=models1), required=False)
                else:
                    cts1 = r.content_types_group1.all()
                    models1 = []                    
                    for ct in cts1:
                        models1.append(ct.model)                       
                    self.fields['object1'] = forms.CharField(widget=AtlAutocompleteWidget(models=models1), required=False)                                      
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
        if data is not None:
            if 'object1' in data: del data['object1']
            if 'object2' in data: del data['object2']
            
    relation = forms.ModelChoiceField(queryset=AtlRelation.objects.all(), widget=forms.Select(attrs={'onchange':'set_initial();'})) 
    object1 = forms.CharField(widget=AtlAutocompleteWidget, required=False) 
    object2 = forms.CharField(widget=AtlAutocompleteWidget, required=False)
    object1_id = forms.CharField(initial=0, widget=forms.HiddenInput)
    object2_id = forms.CharField(initial=0, widget=forms.HiddenInput)
    content_type1_id = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    content_type2_id = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    readonly = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False, initial='', label=_('Relation'))
    readonly_obj1 = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False, initial='', label=_('Object')+'1')
    readonly_obj2 = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required=False, initial='', label=_('Object')+'2')

    class Meta:
        model = AtlRelationsInstance
        fields = ('readonly', 'relation', 'readonly_obj1', 'object1', 'readonly_obj2', 'object2', 'object1_id', 'object2_id', 'content_type1_id', 'content_type2_id')
        
    def clean(self):
        cleaned_data = self.cleaned_data
        relation = cleaned_data.get("relation") 
        object1_id = cleaned_data.get("object1_id")
        object2_id = cleaned_data.get("object2_id")
        content_type1_id = cleaned_data.get("content_type1_id")
        content_type2_id = cleaned_data.get("content_type2_id")
        if object1_id == object2_id and content_type1_id == content_type2_id:
             msg = _("Object1 and Object2 cannot be the same!")
             self._errors["object1_id"] = ErrorList([msg])        
             del cleaned_data["object1_id"]             
        return cleaned_data
