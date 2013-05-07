# coding=UTF-8
import sys
import logging

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models.base import ModelBase
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.contrib.auth.models import User
#from django.contrib.admin import site as panel

from atlcore.cms.admin import panel
from atlcore.site.base_page import ContentPage, VideoPage, ContainerPage
from atlcore.site.dublincore import DublinCore
from atlcore.siteprofile.models import SiteProfile
from atlcore.usersprofile.models import AtlUserProfile
from atlcore.skin.models import Skin
from atlcore.site.mediaenvironment import MediaEnvironment
from atlcore.contenttype.models import Node, Content, Video, Container, Link
from atlcore.site.forms import ContactFormWithCaptcha
from atlcore.site.forms import UserSubscriber
from atlcore.vcl.components import LanguageSwitch
from atlcore.vcl.components.search import Search

class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass


class BaseSite(object):
    ''' Clase base que tiene la responsabilidad de implementar las vistas del sitio
    
        En cada sitio que se implemente se creará una clase que herede de esta y se definirán métodos
        responsables de conformar los contextos que se consumirán desde las plantillas
    '''
    
    main_template = 'main.html'
    base_template = 'base.html'
    home_template = 'home.html'
    contact_template = 'contact.html'
    recipient_list = []
    
    def __init__(self, name=None, app_name='atl'):
        self.from_email = settings.DEFAULT_FROM_EMAIL
        if SiteProfile.objects.get(site__id=settings.SITE_ID).contact:
            self.recipient_list = [SiteProfile.objects.get(site__id=settings.SITE_ID).contact]
        self.index_template = ''
        self.aspect_template = 'aspect.html'
        self._registry = {} # model_class class -> admin_class instance
        self.root_path = None
        self.media_environment = MediaEnvironment()
        try:
            self.skin = SiteProfile.objects.get(site__id=settings.SITE_ID).skin
            self.skin_name = self.skin.slug
        except:
            self.skin = Skin()
            self.skin.slug = 'basesite'
            self.skin.name = 'basesite'
        if name is None:
            self.name = 'atl'
        else:
            self.name = name
        self.app_name = app_name
        self.original_template_dirs = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS += ('%s/siteapp/templates/%s' % (settings.PROJECT_ROOT, self.skin.slug), )
        settings.STATICFILES_DIRS += ('%s/siteapp/static/skins/%s' % (settings.PROJECT_ROOT, self.skin.slug), )
        # regristro todos los componentes que están registrados en el panel de control
        for model_and_admin in panel._registry.items():
            model = model_and_admin[0]
            if issubclass(model, Node): 
                if issubclass(model, Video):
                    self.register(model, VideoPage)
                elif issubclass(model, Container):
                    self.register(model, ContainerPage)
                else:
                    self.register(model, ContentPage)

        
    def get_base_context(self, request):
        ''' 
        Construye el contexto base que todo sitio debe tener. 
        Cuando se extienda esta clase, se debe extender este método añadiendo las particularidades del sitio 
        '''
        context = {}
        try:
            context['site_profile'] = SiteProfile.objects.get(site__id=settings.SITE_ID)
            self.skin = context['site_profile'].skin
            self.skin_name = self.skin.slug
        except:
            self.skin = Skin()
            self.skin.slug = 'basesite'
            self.skin.name = 'basesite'
        settings.TEMPLATE_DIRS = self.original_template_dirs + ('%s/../siteapp/templates/%s' % (settings.PROJECT_ROOT, self.skin.slug), )
        context['skin'] = self.skin
        context['SKIN_MEDIA_URL'] = self.skin_media_url
        context['SKIN_STATIC_URL'] = '%sskins/%s/' % (settings.STATIC_URL, self.skin.slug)
        context['media_environment'] = MediaEnvironment()
        context['TEMPLATE_DIRS'] = settings.TEMPLATE_DIRS
        context['DEBUG'] = settings.DEBUG
        context['dc'] = self.__get_metadata_from_profile__()
        context['request'] = request
        if len(settings.LANGUAGES) > 0:
            context['language_switch'] = LanguageSwitch()
            context['language_switch'].flag_url = "%simages/flags/" % context['SKIN_MEDIA_URL']
            context['media_environment'].append_media(context['language_switch'])
        return context
    
    def get_skin_media_url(self):
        return '%sskins/%s/' % (settings.MEDIA_URL, self.skin.slug)
    skin_media_url = property(get_skin_media_url)
    
    def __get_metadata_from_profile__(self):
        '''
        Construye una instancia de la clase DublinCore dándole como propiedades, la información genérica del sitio
        '''
        dc = DublinCore()
        siteprofile = SiteProfile.objects.get(site__id=settings.SITE_ID)
        dc.title = siteprofile.site.name
        dc.description = siteprofile.description
        dc.keywords = siteprofile.keywords
        return dc
                
    def register(self, model_or_iterable, site_class=None, **options):
        """
        """
        if not site_class:
            site_class = BasePage

        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                raise AlreadyRegistered('The model %s is already registered' % model.__name__)

            if options:
                options['__module__'] = __name__
                site_class = type("%sSite" % model.__name__, (site_class,), options)

            self._registry[model] = site_class(model, self)

    def unregister(self, model_or_iterable):
        """
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model not in self._registry:
                raise NotRegistered('The model %s is not registered' % model.__name__)
            del self._registry[model]    
        
        
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url, include
        urlpatterns = patterns('',
            #url(r'^$', self.index, name='site_index'),
            url(r'^css_font_code/(?P<font_name>.+)/$', self.css_font_code, name='css_font_code'),
            url(r'^section/(?P<aspect_id>[a-fA-F0-9]+)/$', self.aspect_view, name='aspect_view'),
            url(r'^section/(?P<aspect_id>[a-fA-F0-9]+)/(?P<slug>.+)/$', self.aspect_view, name='aspect_view_width_slug'),
            url(r'^context/$', self.view_context, name= 'view_context'),
            
            url(r'^contact/$', self.view_contact, name= 'view_contact'),
            url(r'^subscribe/$', self.subscribe_view, name= 'subscribe_view'),
            url(r'activate_user/(?P<activation_code>[a-fA-F0-9]+)/$', self.activate_user, name= 'activate_user'),
            url(r'^search/$', self.basic_search, name= 'basic_search')
            
            
        )
        
        for model, model_site in self._registry.items():
            urlpatterns += patterns('',
                url(r'^%s/' % (model._meta.module_name), include(model_site.get_urls()))
            )

            
        #urlpatterns += patterns('', url(r'^(?P<slug>[a-zA-Z0-9-]+)/$', self.slug_details_view, name='slug_details'),)
        return urlpatterns
        
    def basic_search(self, request):
        context = self.get_base_context(request)
        template='site/search.html'
        context_class=RequestContext
        try:
            from haystack.query import EmptySearchQuerySet
            from haystack.forms import ModelSearchForm
            from haystack.views import RESULTS_PER_PAGE
            
            load_all=True
            form_class=ModelSearchForm
            searchqueryset=None
            
            extra_context=None
            results_per_page=None
            query = ''
            results = EmptySearchQuerySet()
            
            if request.GET.get('q'):
                form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)
                if form.is_valid():
                    query = form.cleaned_data['q']
                    list_models = form.cleaned_data['models']
                    query_models = ""
                    for model in list_models:
                        query_models += "&models=" + model
                    context['query_models'] =query_models
                    results = form.search()
            else:
                form = form_class(searchqueryset=searchqueryset, load_all=load_all)
            
            paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE )
            
            try:
                page = paginator.page(int(request.GET.get('page', 1)))
            except InvalidPage:
                raise Http404("No such page of results!")
            context ['form'] = form
            context ['page'] = page
            context ['paginator'] = paginator
            context ['query'] = query
            context ['suggestion'] = None
            
            componentSearch = Search(page, "Búsquedas")
            
            context ['component'] = componentSearch
            
            if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
                context['suggestion'] = form.get_suggestion()
            
            if extra_context:
                context.update(extra_context)
        except:
            cad = "No se tiene el haystack correctamente instalado"
            context["errors"] = cad + str(sys.exc_info())
            pass
        return render_to_response(template, context, context_instance=context_class(request))
    
    def slug_details_view(self, request, slug):
        context= self.get_base_context(request)
        node = Node.objects.filter(slug=slug)
        context['message'] = slug + ' ' + node[0].content_type.model
        context['message'] = self.__registry__
        
        return render_to_response('site/message.html', context, context_instance=RequestContext(request))
    
    def view_contact(self, request, extra_context=None):
        context = self.get_base_context(request)
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            country = request.POST.get('country')
            message = request.POST.get('message')
            next = request.POST.get('next',"")
            form = ContactFormWithCaptcha(request.POST)
            messagetext= ""
            if form.is_valid():
                subject = "Contacto: " + name
                message_heading = "Nombre: " + name +  "\nEmail: " + email + "\nPaís: " + str(country) + "\nHa enviado el siguiente mensaje:\n"
                
                if self.recipient_list:
                    try:
                        send_mail(subject, message_heading + message, self.from_email, self.recipient_list, fail_silently=False)
                        messagetext = "<p>El mensaje fue enviado correctamente, le responderemos a la mayor brevedad.</p>"
                        context["message"] = messagetext
                        return render_to_response(['site/message.html',
                    ], context, context_instance=RequestContext(request))

                    except:
                        #No se puede hacer print hay que loguear el error.
                        cad = "Unexpected error:" +  str(sys.exc_info()[0]) + "   " + str(sys.exc_info()[1]) + "   " + str(sys.exc_info()[2])
                        # Get an instance of a logger
                        logger = logging.getLogger('atlcms')
                        logger.error(cad)
                        messagetext = "Ocurrio un error enviando el mensaje" + cad
                else:
                    messagetext = "No hay correos definidos."
            context["form"] = form
            
        else:
            form = ContactFormWithCaptcha()
        context["form"] = form
        return render_to_response([
            'site/%s' % self.contact_template,
        ], context, context_instance=RequestContext(request))
        
    def __send_email__(self, subject, text_content, html_content, to):
        from django.core.mail import EmailMultiAlternatives
        from_email = settings.DEFAULT_FROM_EMAIL
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
    def subscribe_view(self, request):
        context = self.get_base_context(request)
        if request.method == 'POST':
            form = UserSubscriber(request.POST)
            if form.is_valid():
                try:
                    user = User.objects.get(email=form.cleaned_data['email'])
                    context['message'] = 'El usuario %s ya se ha suscrito anteriormente' % form.cleaned_data['email']
                except:
                    user = User()
                    user.username= form.cleaned_data['email'][:30]
                    user.is_active = False
                    user.email = form.cleaned_data['email']
                    user.save()
                    context['site_profile'].site.name
                    text_content = 'Usted se ha suscrito al boletín del sitio %s. Para activar su suscripción debe pinchar el siguiente enlace: http://%s/activate_user/%s' % (context['site_profile'].site.name, context['site_profile'].site.domain, user.atluserprofile.activation_code)
                    html_content = '<p>Usted se ha suscrito al boletín del sitio %s.</p><p>Para activar su suscripción debe pinchar el siguiente enlace: <a href="http://%s/activate_user/%s">Activar suscripción</a></p>' % (context['site_profile'].site.name, context['site_profile'].site.domain, user.atluserprofile.activation_code)
                    self.__send_email__('Activación de suscripción', text_content, html_content, user.email )
                    context['message'] = 'Se ha enviando un mensaje a %s para validar la suscripción' % form.cleaned_data['email']
            else:
                context['message'] = 'Error: debe especificar una dirección de correo válida'
        else:
            form = UserSubscriber()
        return render_to_response('site/ajax_message.html', context)
    
    def activate_user(self, request, activation_code):
        context = self.get_base_context(request)
        try:
            user = User.objects.get(atluserprofile__activation_code = activation_code)
            user.atluserprofile.activation_code = ''
            user.is_active = True
            user.atluserprofile.save()
            user.save()
            context['message'] = 'Se ha activado correctamente el usuario'
        except:
            context['message'] = 'El código de activación es erróneo'
        return render_to_response('site/user_message.html', context, context_instance=RequestContext(request))
        
    def css_font_code(self, request, font_name):
        context = {'font_name': font_name,}
        browser_type = 'mozilla'
        return render_to_response('site/%s_font_code.css' % browser_type, 
                                  context)    
    
    def index(self, request, extra_context=None):
        context = self.get_base_context(request)
        context = extra_context or {}
        return render_to_response(self.index_template or ['site/%s' % self.home_template,], 
                                  context, context_instance=RequestContext(request))    
        
    def aspect_view(self, request, aspect_id, slug=None):
        context = self.get_base_context(request)
        context['contents'] = Content.objects.filter(aspect__id=aspect_id)
        return render_to_response('site/%s' % self.aspect_template, context, context_instance=RequestContext(request))    
        

    def view_context(self, request):
        context = {'core_message': 'message',
                   'skin_name': self.skin_name}
        context.update({'context': context})
        return render_to_response('%s/context.html' % self.skin_name,
            context, context_instance=RequestContext(request))

    def list(self, request, extra_context=None, aspect_slug=None):
        context = {
            'atl_site':self,
            'title':'content list',
            'description':'content list',
            'keywords': 'atlantesoftware',
        }
        objects = AtlGeneric.atl_objects.by_aspect(aspect_slug)
        base_context = self.__base_collection_view__(request, objects, aspect_slug=aspect_slug)
        context.update(base_context)
        context.update(extra_context or {})
        return render_to_response(self.index_template or [
                #self.skin + '/summaries.html',
                self.default_skin + '/summaries.html',
            ], context, context_instance=RequestContext(request))
