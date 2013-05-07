#coding=UTF-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from atlcore import settings as atlsettings
from atlcore.site.mediaenvironment import MediaEnvironment
from atlcore.contenttype.models import Node, Container, Content

use_atl_workflow = False
if 'atlcore.workflows' in settings.INSTALLED_APPS:
    try:
        from atlcore.workflows.models import Workflow, Transition, State
    except ImportError:
        pass
    else:
        use_atl_workflow = True

class ComponentManager(object):
    
    def __init__(self, request, admin_site, instance=None, context={}):
        self.request = request
        self.user = self.request.user
        self.instance = instance
        self.media_environment = MediaEnvironment()
        self.context = context
        self.is_container = False
        self.is_index = not bool(self.instance)
        self.content_type = None
        self.opts = None
        self.admin_model = None
        self.admin_site = admin_site
        self.container = None
        self.workflow = None     
        if self.instance is not None:
            self.is_container = isinstance(self.instance, Container)
            self.container = self.instance if self.is_container else self.instance.parent
            self.content_type = self.instance.content_type
            self.opts = self.instance._meta
            self.info = self.opts.app_label, self.opts.module_name
            self.admin_model = self.admin_site._registry.get(self.content_type.model_class(), None)
            if use_atl_workflow:
                self.workflow = Workflow.get_workflow_for_model(self.content_type)
        self.transitions = None
        self.current_state = None
        if self.workflow is not None:
            self.transitions = Transition.get_allowed_transitions(self.instance, self.user)
            self.current_state = State.get_state(self.instance)
        self.container_id = self.container.id if self.container is not None else None
        self.context['container_id'] = self.container_id
        self.request.session['container_id'] = self.container_id          
        self.nodes_models = []
        self.contents_models = []
        self.containers_models = []
        for model, model_admin in self.admin_site._registry.items():
            if issubclass(model, Node): 
                self.nodes_models.append(model)
                if issubclass(model, Container):
                    self.containers_models.append(model)
                elif issubclass(model, Content):
                    self.contents_models.append(model)   
        self.can_add = self.__can_add__()                    
            
    def __allowed_models__(self):
        if self.is_index:
            models = [m for m in self.containers_models if self.user.has_perm(u"%s.add_%s" % (m._meta.app_label, m._meta.module_name))]
        else:
            #return self.containers_models + self.contents_models
            #user.has_perm(u"%s.change_%s" % (folder._meta.app_label, folder._meta.module_name), folder):
            self.instance.load_registry()
            models = [m[1] for m in self.instance._registry.items() if self.user.has_perm(u"%s.add_%s" % (m[1]._meta.app_label, m[1]._meta.module_name))]
        models.sort()
        return models
        
    def get_context(self, obj=None):
        self.context.update(self.__get_edit_toolbar__())
        self.context.update(self.__get_nav_tree__(self.container))
        self.context.update(self.__get_add_toolbar__())
        self.context.update(self.__get_jqgrid__())
        self.context.update(self.__get_clipboard_toolbar__())
        self.context.update(self.__get_workflow_toolbar__())
        self.context.update(self.__get_transition_toolbar__())
        self.context.update(self.__get_permissions_toolbar__())
        self.context.update(self.__get_settings_toolbar__())
        self.context.update({'media_environment': self.media_environment})        
        return self.context
    
    
    def get_jqgrid_provider(self):
        from atlcore.vcl.dataproviders.jqgrid import JQGridNodeProvider
        return JQGridNodeProvider(self.container_id)
    
    def __get_jqgrid__(self):
        from atlcore.vcl.components import JQGrid        
        grid = JQGrid(self.get_jqgrid_provider())
        if self.container is not None:
            grid.caption = str('%s: %s' % (self.container.content_type.model, self.container.title))
        else:    
            grid.caption = _('Root')    
        grid.id = 'node_list'
        grid._js_behavior = '/static/cms/js/components_behavior/JQGrid.%s.js' % grid.id
        grid.sortname = 'order'
        grid.sortorder = 'desc'
        grid.multiselect = True
        grid.toolbar = [True, 'top']
        grid.rowNum = 20
        grid.height = "100%" 
        grid.stylelist += [{'css_jqgrid_cms' :  '/common/js/jquery.plugins/jqgrid/css/ui.jqgrid_cms.css'}]
        #object_list = result['object_list']
        #result['grid'] = grid
        self.media_environment.append_media(grid)
        return {'grid': grid}
    
    def __get_nav_tree__(self, container_active):
        from atlcore.contenttype.models import Container
        from atlcore.vcl.components import JSTree
        from atlcore.vcl.dataproviders import JSTreeContainerProvider
        from django.utils.translation import get_language
        jstree_provider = JSTreeContainerProvider(container_active)
        nav_tree = JSTree(jstree_provider)
        nav_tree.id = 'nav_tree'
        nav_tree.themes.theme = "apple"
        nav_tree.themes.url = "/static/common/js/jquery.plugins/jstree/themes/apple/style.css"
        nav_tree.plugins.append('json_data')

        self.media_environment.append_media(nav_tree)
        return {'nav_tree': nav_tree}
    
    def __can_add__(self):
        can_add = self.is_index or (self.is_container and self.user.has_perm(u"%s.change_%s" % (self.opts.app_label, self.opts.module_name), self.instance))
        if not can_add: return False
        
        return bool(self.__allowed_models__()) 

    
    def __get_add_toolbar__(self):

        if self.can_add:
            from atlcore.vcl.components import Button, ToolBar
            tool_bar = ToolBar()
            models = self.__allowed_models__()
            for model in models:
                name = model._meta.module_name
                verbose_name = model._meta.verbose_name_raw
                label = model._meta.app_label 
                button = Button()
                button.id = 'button_%s' %name
                button.theme = atlsettings.THEME
                #button.on_click = mark_safe('location.href="%s"' %reverse('admin:%s_%s_add'%(label, name)));
                button.on_click = mark_safe('location.href="/%s/%s/container/%s/%s_add"' % (atlsettings.ADMIN_PREFIX, label, self.container_id, name, ));
                button.text = name.capitalize()
                button.label = unicode(verbose_name.capitalize()) 
                #button.icons = {'primary': 'ui-icon-document'}
                tool_bar.button_list.append(button)
            return {'add_toolbar': tool_bar}   
        return {}
    
    def __get_edit_toolbar__(self):
        from atlcore.vcl.components import Button, ToolBar
        tool_bar = ToolBar()
        self.media_environment.append_media(tool_bar)
        tool_bar.id = 'tool_bar'
        tool_bar.html_class = 'tool_bar'
        button_new = Button()
        button_new.id = 'button_new'
        button_new.theme = atlsettings.THEME
        button_new.disabled = not self.can_add
        self.media_environment.append_media(button_new)
        button_new._js_behavior = '/static/cms/js/components_behavior/tool_bar.button.new.js'
        button_new.text = False  
        button_new.label = 'New' 
        button_new.icons = {'primary': 'ui-icon-document'}
        tool_bar.button_list.append(button_new)
        button_edit = Button()
        button_edit._js_behavior = '/static/cms/js/tool_bar.button.edit.js'
        button_edit.id = 'button_edit'
        button_edit.theme = atlsettings.THEME
        button_edit.text = False
        button_edit.label = 'Edit'
        button_edit.icons = {'primary': 'ui-icon-pencil'}
        tool_bar.button_list.append(button_edit)
        button_delete = Button()
        button_delete.id = 'button_delete'
        button_delete.theme = atlsettings.THEME
        button_delete.text = False
        button_delete.label = 'Delete'
        button_delete.icons = {'primary': 'ui-icon-trash'}
        if self.instance is not None: 
            button_delete.on_click = mark_safe('location.href="/%s/%s/%s/%s/delete/"' % (atlsettings.ADMIN_PREFIX, self.instance._meta.app_label, self.instance._meta.module_name, self.instance.id))
        else:
            button_delete.disabled = True        
        tool_bar.button_list.append(button_delete)       
        return {'edit_toolbar': tool_bar}
    
    def __can_paste__(self):
        return True#self.admin_site.clipboard.can_paste(self.container)

    def __get_clipboard_toolbar__(self):
        from atlcore.vcl.components import Button, ToolBar
        tool_bar = ToolBar()
        self.media_environment.append_media(tool_bar)
        tool_bar.id = 'clipboard_tool_bar'
        tool_bar.html_class = 'tool_bar'
        #Copy
        button_copy = Button()
        button_copy.id = 'button_copy'
        button_copy.theme = atlsettings.THEME
        button_copy._js_behavior = '/static/cms/js/components_behavior/clipboard_tool_bar.button.copy.js'
        button_copy.on_click = mark_safe('copy_to_clipboard("%s");'%reverse('admin:copy-to-clipboard'));
        button_copy.text = False
        button_copy.icons = {'primary': 'ui-icon-copy'}  
        button_copy.label = 'copy'
        #button_copy.icons = {'primary': 'ui-icon-document'}
        tool_bar.button_list.append(button_copy)   
        #Cut
        button_cut = Button()
        button_cut.id = 'button_cut'
        button_cut.theme = atlsettings.THEME
        button_cut._js_behavior = '/static/cms/js/components_behavior/clipboard_tool_bar.button.copy.js'
        button_cut.on_click = mark_safe('copy_to_clipboard("%s");'%reverse('admin:cut-to-clipboard'));
        button_cut.text = False
        button_cut.icons = {'primary': 'ui-icon-scissors'}
        button_cut.label = 'cut'
        #button_cut.icons = {'primary': 'ui-icon-document'}
        tool_bar.button_list.append(button_cut)
        #Paste
        button_paste = Button()
        button_paste.id = 'button_paste'
        button_paste.disabled = not self.__can_paste__()
        button_paste.theme = atlsettings.THEME
        button_paste._js_behavior = '/static/cms/js/components_behavior/clipboard_tool_bar.button.paste.js'
        button_paste.on_click = mark_safe('paste_from_clipboard("%s");'%reverse('admin:paste-from-clipboard', args=[self.container.id if self.container is not None else 0]));
        button_paste.text = False  
        button_paste.label = 'paste'
        button_paste.icons = {'primary': 'ui-icon-clipboard'}
        #button_paste.icons = {'primary': 'ui-icon-document'}
        tool_bar.button_list.append(button_paste)                          
        return {'clipboard_toolbar': tool_bar}
    
    def __get_workflow_toolbar__(self):
        if self.workflow is not None:
            from atlcore.vcl.components import Button, ToolBar
            tool_bar = ToolBar()
            self.media_environment.append_media(tool_bar)
            tool_bar.id = 'workflow_tool_bar'
            tool_bar.html_class = 'tool_bar'
            #Change transition
            button_transition = Button()
            button_transition.id = 'button_transition'
            button_transition.theme = atlsettings.THEME
            button_transition._js_behavior = '/static/cms/js/components_behavior/workflow_tool_bar.button.transition.js'
            #button_transition.on_click = mark_safe('transition_to_clipboard("%s");'%reverse('admin:transition-to-clipboard'));
            button_transition.text = False  
            button_transition.label = 'transition'
            button_transition.icons = {'primary': 'ui-icon-transfer-e-w'}
            tool_bar.button_list.append(button_transition)
            return {'workflow_toolbar': tool_bar}
        return {}
        
        
    def __get_transition_toolbar__(self):
        if self.transitions is not None:
            from atlcore.vcl.components import Button, ToolBar
            tool_bar = ToolBar()
            self.media_environment.append_media(tool_bar)
            tool_bar.id = 'workflow_tool_bar'
            #Change State buttons
            for transition in self.transitions:
                button_transition = Button()
                button_transition.id = 'button_transition_%s' %transition.id
                button_transition.theme = atlsettings.THEME
                #button_transition._js_behavior = '/static/cms/js/components_behavior/transition_tool_bar.button.transition.js'
                button_transition.on_click = mark_safe('location.href="%s"' % reverse('admin:transition_to', args=[self.instance.id, transition.id]));
                button_transition.text = False
                button_transition.label = transition.name
                #button_transition.icons = {'primary': 'ui-icon-transfer-e-w'}
                tool_bar.button_list.append(button_transition)
            return {'transition_toolbar': tool_bar}
        return {}
    
    def __get_permissions_toolbar__(self):
        if self.instance:
            from atlcore.vcl.components import Button, ToolBar
            tool_bar = ToolBar()
            self.media_environment.append_media(tool_bar)
            tool_bar.id = 'permissions_tool_bar'
            tool_bar.html_class = 'tool_bar'
            #Change transition
            button_permission = Button()
            button_permission.id = 'button_permission'
            button_permission.theme = atlsettings.THEME
            #button_permission._js_behavior = '/static/cms/js/components_behavior/workflow_tool_bpermissionpermission.js'
            button_permission.on_click = mark_safe('location.href="%s"' % reverse('admin:%s_%s_permissions'%self.info, args=[self.instance.id]));
            button_permission.text = False
            button_permission.icons = {'primary': 'ui-icon-key'}
            button_permission.label = 'permission'
            #button_permission.icons = {'primary': 'ui-icon-document'}
            tool_bar.button_list.append(button_permission)
            return {'permissions_toolbar': tool_bar}
        return {}
    
    def __get_settings_toolbar__(self):
        if self.is_container:
            from atlcore.vcl.components import Button, ToolBar
            self.instance.load_registry()
            tool_bar = ToolBar()
            self.media_environment.append_media(tool_bar)
            tool_bar.id = 'settings_tool_bar'
            tool_bar.html_class = 'tool_bar'
            #Change transition
            button_settings = Button()
            button_settings.id = 'button_settings'
            button_settings.theme = atlsettings.THEME
            #button_settings._js_behavior = '/static/cms/js/components_behavior/workflow_tool_bar.button.settings.js'
            button_settings.on_click = mark_safe('location.href="%s"' % reverse('admin:%s_%s_settings'%self.info, args=[self.instance.id]));
            button_settings.text = False  
            button_settings.label = 'settings'
            button_settings.icons = {'primary': 'ui-icon-wrench'}
            tool_bar.button_list.append(button_settings)
            return {'settings_toolbar': tool_bar}
        return {}
        
                  
     
