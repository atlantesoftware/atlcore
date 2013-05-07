#encoding=UTF-8

from django.conf.urls.defaults import patterns, url
from atlcore.contenttype.models import Node
from django.shortcuts import render_to_response
from django.utils import simplejson

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.translation import get_language
from atlcore.settings import ADMIN_PREFIX
from django.db.models import Q

class JQGridNodeProvider(object):
    
    def __init__(self, container_id=None):
        self.container_id = container_id
        if container_id:
            self.url = '/%s/jqgridnode/%s/getdata/' % (ADMIN_PREFIX, self.container_id)
        else:
            self.url = '/%s/jqgridnode/getdata/' % ADMIN_PREFIX
        self.sortorder_url = '/%s/jqgridnode/sortorder/' % ADMIN_PREFIX
        self.colnames = ['title', 
                         'slug', 
                         'description', 
                         'date', 
                         'update', 
                         'image', 
                         'owner', 
                         'state', 
                         'created_on', 
                         'updated_on', 
                         'parent', 
                         'class_name', 
                         'order',
                         'view_count', 
                         'admin_url', 
                         'admin_change_url', 
                         'admin_delete_url']
        self.editurl = '/edit/' 
    
    @classmethod    
    def get_urls(self):
        my_urls = patterns('',
            url(r'^jqgridnode/getdata/$', self.get_data, name='getdata'),
            url(r'^jqgridnode/(?P<container_id>.+)/getdata/$', self.get_data, name='getdata'),
            url(r'^jqgridnode/sortorder/$', self.sortorder, name="sortorder"),
            url(r'^jqgridnode/deletedata/$', self.delete_data, name="deteledata"),

        )
        return my_urls
    
    @classmethod
    def delete_data(self, request):
        node_list = simplejson.JSONDecoder().decode(request.GET.get('node_list'))
        for node_id in node_list:
            node = Node.objects.get(pk = node_id.replace('node_', ''))
            if node:
                node.get_instance().delete();            
        response = {
           "state": "succes"
        } 
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    
    @classmethod
    def sortorder(self, request):
        node_list = []
        order_list = []
        for node_id in request.GET.getlist('node[]'):
            node_list.append(Node.objects.get(id=node_id).get_instance())
            order_list.append(node_list[len(node_list) - 1].order)
        order_list.sort(reverse=True)
        for i in range(len(order_list)):
            node_list[i].order = order_list[i]
            node_list[i].save()
        context = {
            'node_list': node_list,
            'order_list' : order_list,
        }
        return render_to_response('vcl/dataproviders/jqgrid/node/sort.html', context)

    
    @classmethod
    def get_data(self,  request, container_id=None):
        language = get_language()
        if 'page' in request.GET: 
            page = request.GET['page']
        else:
            page = 1
        if 'rows' in request.GET: 
            rows = int(request.GET['rows'])
        else:
            rows = 20
        if 'sidx' in request.GET: 
            sidx = request.GET['sidx']
        else:
            sidx = 'order'
        if 'sord' in request.GET: 
            sord = request.GET['sord']
        else:
            sord = 'desc'
        if sord == 'asc':
            nodes = Node.objects.filter(parent=container_id).filter(Q(language=language) | Q(neutral = True)).order_by(sidx)
        else:
            nodes = Node.objects.filter(parent=container_id).filter(Q(language=language) | Q(neutral = True)).order_by("-"+sidx)
        paginator = Paginator(nodes, rows)
        rows = paginator.page(page).object_list
        json_data = {}
        json_data['total'] = paginator.num_pages
        json_data['page'] = page
        json_data['records'] = len(nodes)
        json_data['rows'] = []

        for row in rows:
            row_data = {}
            row_data['id'] = 'node_%s' % row.pk
            row_data['cell'] = [row.title, 
                                row.slug, 
                                row.description, 
                                str(row.date), 
                                str(row.update_date), 
                                str(row.image), 
                                str(row.owner),
                                row.state,
                                str(row.created_on),
                                str(row.updated_on),
                                'row.parent',
                                row.content_type.name,
                                row.order,
                                row.view_count,
                                row.admin_url(), 
                                row.admin_change_url(),
                                row.admin_delete_url()
                                 ]
            json_data['rows'].append(row_data)
        context = {
                   'json_data' : simplejson.dumps(json_data)
        }
        return render_to_response('vcl/dataproviders/jqgrid/node/getdata.html', context)
    