#coding=UTF-8
from atlcore.relations.forms import AtlRelationsInstanceForm
from atlcore.relations.models import AtlRelation, AtlRelationsInstance

from django import forms, template
from django.forms.formsets import all_valid
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.contrib.admin import widgets, helpers, ModelAdmin
from django.contrib.admin.util import unquote, flatten_fieldsets, get_deleted_objects, model_ngettext, model_format_dict
from django.contrib import messages, admin
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied, ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.fields import BLANK_CHOICE_DASH
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.utils.datastructures import SortedDict
from django.utils.functional import update_wrapper
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.functional import curry
from django.utils.text import capfirst, get_text_list
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext, ugettext_lazy
from django.utils.encoding import force_unicode

csrf_protect_m = method_decorator(csrf_protect)

def get_content(ct_id, obj_id):
    if ct_id != '0' and obj_id != '0':
        try:
            ct = ContentType.objects.get(pk=ct_id)
        except (MultipleObjectsReturned, ObjectDoesNotExist):
            pass
        else:
            model = ct.model_class()
            try:
                content = model.objects.get(pk=obj_id)
            except (MultipleObjectsReturned, ObjectDoesNotExist):
                pass
            else:
                return content
    return None 

class AtlRelInstanceAdmin(ModelAdmin):
    
    form = AtlRelationsInstanceForm
    
    def __base_response__(self, request, obj):
        pk_value = escape(obj._get_pk_val())
        ct_id = escape(request.GET.get("ct_id") if request.GET.has_key("ct_id") else 0)
        obj_num = 1
        obj_id = escape(request.GET.get("obj1_id") if request.GET.has_key("obj1_id") else '0')
        if obj_id == '0':
            obj_num = 2
            obj_id = escape(request.GET.get("obj2_id") if request.GET.has_key("obj2_id") else '0')
        qstring = '?ct_id=%s&obj%s_id=%s'%(ct_id, obj_num, obj_id)
        url = reverse('admin:relations_atlrelationsinstance_change', args=[pk_value])
        up_url = escape(url+qstring)
        del_url = escape(url+'delete'+qstring)    
        obj = escape(obj)
        return HttpResponse('<script type="text/javascript">opener.dismissPopup(window, "%s", "%s", "%s", "%s");</script>' %(pk_value, obj, up_url, del_url))
    
    def response_change(self, request, obj):
        """
        Rescribiendo el método para que en la opción de salvar regrese para el contenedor
        """
        if request.POST.has_key("_popup"): return self.__base_response__(request, obj)
        return super(AtlRelInstanceAdmin, self).response_change(request, obj)
    
    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Rescribiendo el método para que en la opción de salvar regrese para el contenedor
        """
        if request.POST.has_key("_popup"): return self.__base_response__(request, obj)
        return super(AtlRelInstanceAdmin, self).response_add(request, obj, post_url_continue)
    
    @csrf_protect_m
    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, perms_needed) = get_deleted_objects((obj,), opts, request.user, self.admin_site)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            obj.delete()

            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})
            
            ct_id = escape(request.GET.get("ct_id") if request.GET.has_key("ct_id") else '0')
            obj_id = escape(request.GET.get("obj1_id") if request.GET.has_key("obj1_id") else '0')
            if obj_id == '0':
                obj_id = escape(request.GET.get("obj2_id") if request.GET.has_key("obj2_id") else '0')            
            content = get_content(ct_id, obj_id)
            if content is not None:
                return HttpResponseRedirect(content.admin_change_url())
            if not self.has_change_permission(request, None):
                return HttpResponseRedirect("../../../../")
            return HttpResponseRedirect("../../")

        context = {
            "title": _("Are you sure?"),
            "object_name": force_unicode(opts.verbose_name),
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "opts": opts,
            "root_path": self.admin_site.root_path,
            "app_label": app_label,
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, context_instance=context_instance)
    

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        "The 'add' admin view for this model."
        model = self.model
        opts = model._meta

        if not self.has_add_permission(request):
            raise PermissionDenied

        ModelForm = self.get_form(request)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES)
            if form.is_valid():
                new_object = self.save_form(request, form, change=False)
                form_validated = True
            else:
                form_validated = False
                new_object = self.model()
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request), self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(data=request.POST, files=request.FILES,
                                  instance=new_object,
                                  save_as_new=request.POST.has_key("_saveasnew"),
                                  prefix=prefix, queryset=inline.queryset(request))
                formsets.append(formset)
            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=False)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=False)

                return self.response_add(request, new_object)
        else:
            # Prepare the dict of initial data from the request.
            # We have to special-case M2Ms as a list of comma-separated PKs.
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")                
            form = ModelForm(initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=self.model(), prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, list(self.get_fieldsets(request)),
            self.prepopulated_fields, self.get_readonly_fields(request),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request))
            readonly = list(inline.get_readonly_fields(request))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Add %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'is_popup': request.REQUEST.has_key('_popup'),
            'show_delete': False,
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, form_url=form_url, add=True)

    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, extra_context=None):
        "The 'change' admin view for this model."
        model = self.model
        opts = model._meta

        obj = self.get_object(request, unquote(object_id))

        if not self.has_change_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        if request.method == 'POST' and request.POST.has_key("_saveasnew"):
            return self.add_view(request, form_url='../add/')

        ModelForm = self.get_form(request, obj)
        formsets = []
        if request.method == 'POST':
            form = ModelForm(request.POST, request.FILES, instance=obj)
            if form.is_valid():
                form_validated = True
                new_object = self.save_form(request, form, change=True)
            else:
                form_validated = False
                new_object = obj
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, new_object),
                                       self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(request.POST, request.FILES,
                                  instance=new_object, prefix=prefix,
                                  queryset=inline.queryset(request))

                formsets.append(formset)

            if all_valid(formsets) and form_validated:
                self.save_model(request, new_object, form, change=True)
                form.save_m2m()
                for formset in formsets:
                    self.save_formset(request, form, formset, change=True)

                change_message = self.construct_change_message(request, form, formsets)
                self.log_change(request, new_object, change_message)
                return self.response_change(request, new_object)

        else:
            initial = dict(request.GET.items())
            for k in initial:
                try:
                    f = opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")
            form = ModelForm(instance=obj, initial=initial)
            prefixes = {}
            for FormSet, inline in zip(self.get_formsets(request, obj), self.inline_instances):
                prefix = FormSet.get_default_prefix()
                prefixes[prefix] = prefixes.get(prefix, 0) + 1
                if prefixes[prefix] != 1:
                    prefix = "%s-%s" % (prefix, prefixes[prefix])
                formset = FormSet(instance=obj, prefix=prefix,
                                  queryset=inline.queryset(request))
                formsets.append(formset)

        adminForm = helpers.AdminForm(form, self.get_fieldsets(request, obj),
            self.prepopulated_fields, self.get_readonly_fields(request, obj),
            model_admin=self)
        media = self.media + adminForm.media

        inline_admin_formsets = []
        for inline, formset in zip(self.inline_instances, formsets):
            fieldsets = list(inline.get_fieldsets(request, obj))
            readonly = list(inline.get_readonly_fields(request, obj))
            inline_admin_formset = helpers.InlineAdminFormSet(inline, formset,
                fieldsets, readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
            media = media + inline_admin_formset.media

        context = {
            'title': _('Change %s') % force_unicode(opts.verbose_name),
            'adminform': adminForm,
            'object_id': object_id,
            'original': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'media': mark_safe(media),
            'inline_admin_formsets': inline_admin_formsets,
            'errors': helpers.AdminErrorList(form, formsets),
            'root_path': self.admin_site.root_path,
            'app_label': opts.app_label,
        }
        context.update(extra_context or {})
        return self.render_change_form(request, context, change=True, obj=obj)
    
    
class AtlRelationAdmin(ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(AtlRelation, AtlRelationAdmin)
admin.site.register(AtlRelationsInstance, AtlRelInstanceAdmin)