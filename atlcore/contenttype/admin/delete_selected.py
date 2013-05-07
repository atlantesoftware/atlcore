#coding=UTF-8
from atlcore.contenttype.helper import add_list_to_session, delete_list_from_session, get_deleted_objects

from django import template
from django.core.exceptions import PermissionDenied
from django.contrib.admin import helpers
from django.contrib.admin.util import model_ngettext
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.csrf import csrf_protect
from django.http import Http404, HttpResponse, HttpResponseRedirect


@csrf_protect
def delete_selected(request, admin_site, url):
    """
    """

    if request.method == 'POST':
        if 's_objects' in request.POST:
            items = add_list_to_session(request, 's_objects')
        else:
            items = delete_list_from_session(request)

    # Populate deletable_objects, a data structure of all related objects that
    # will also be deleted.
    deletable_objects, perms_needed = get_deleted_objects(items, request.user)

    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    if request.POST.get('post'):
        if perms_needed:
            raise PermissionDenied
        n = len(items)
        if n:
            for obj in items:
                obj_display = force_unicode(obj)
                modeladmin = admin_site._registry[obj.__class__]
                modeladmin.log_deletion(request, obj, obj_display)
                obj.delete()
        return HttpResponseRedirect(url)

    context = {
        "title": _("Are you sure?"),
        "object_name": _("Objects"),
        "deletable_objects": deletable_objects,
        'queryset': items,
        "perms_lacking": perms_needed,
        "root_path": admin_site.root_path,
        'action_checkbox_name': _("Delete selected"),
    }
    context.update(csrf(request))

    return render_to_response("admin/cms/delete_selected_in_folder_confirmation.html", context, context_instance=template.RequestContext(request))