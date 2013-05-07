from atlcore.contenttype.models import Container, Node

from django.conf.urls.defaults import patterns, url, include
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

class Clipboard(object):
    
    def get_urls(self):
        return patterns('',
            url(r'^copy/$', self.copy, name="copy-to-clipboard"),
            url(r'^cut/$', self.copy, {'action': 'cut'}, name="cut-to-clipboard"),
            url(r'^paste/(?P<id>[a-fA-F0-9]+)/$', self.paste, name="paste-from-clipboard"),
        )
        
    @csrf_exempt
    def copy(self, request, action='copy'):
        if request.is_ajax() and request.method == "POST":
            nodes = request.POST.get('nodes');
            request.session['copy_to_clipboard'] = (nodes, action)
            return HttpResponse()
        raise Http404
    
    def can_paste(self, container):
        return True
    
    def paste(self, request, id):
        if request.is_ajax():
            url = None
            container = None
            if id==u'0' or id is None:              
                url = reverse('admin:index')
            else:
                try:
                    container = Container.objects.get(pk=id)
                except:
                    pass
                else:
                    url = container.admin_url()
            if url is not None:
                raw_nodes_ids, action = request.session['copy_to_clipboard']
                nodes_ids = raw_nodes_ids.split('_')
                nodes = Node.objects.filter(pk__in=nodes_ids)
                for node in nodes:
                    first_check = False 
                    if container is not None:
                        # chequeando que no haya recursividad.
                        anc = container.get_ancestors() + [container.get_instance()]                        
                        first_check = node.get_instance() not in anc
                    if first_check or (container is None and isinstance(node.get_instance(), Container)):
                        if action == 'cut':
                            node.parent = container
                            node.order = 0
                            node.save()
                        else:
                            node.get_instance().clone(container)
                return HttpResponse(url)
        raise Http404
    
    