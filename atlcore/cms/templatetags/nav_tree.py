#coding=UTF-8
from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext as _, get_language

register = template.Library()

def __branch__(container, user=None, trace=None, level=0, reached=False):
    if container:
        html_class = 'level%d' %level
        if trace is not None and trace and __are_equal__(container, trace[0]):
                if len(trace) == 1:
                    html_class += ' active'
                elif trace:
                    trace = trace[1:]
        else:
            reached = True
        chtml = mark_safe('')
        if trace is not None and not reached:
            level += 1
            html_class += ' expanded'
            chtml = mark_safe('<ul class="menu">\n')
            children = container.get_container_children(filter_by='language')
            if user is not None:
                children = read_access_filter(user, children)            
            for child in children:
                chtml += __branch__(child, user=user, trace=trace, level=level, reached=reached)
            chtml += mark_safe('</ul>\n')
        else:
            html_class += ' colapsed'
        html = mark_safe('<li class="%s"><a href="%s">%s</a></li>\n' %(html_class, container.admin_url(), container.title)) + chtml
        return html
    return None 

class ShowTreeNode(template.Node):
    def __init__(self, object_expr, node_expr, user_expr, tree_name):
        self.node_expr = node_expr
        self.user_expr = user_expr
        self.object_expr = object_expr
        self.tree_name = tree_name
        
    def render(self, context):
        try:
            object = self.object_expr.resolve(context)
        except template.VariableDoesNotExist:
            object = None
        try:
            user = self.user_expr.resolve(context)
        except template.VariableDoesNotExist:
            user = None
        node = None
        if self.node_expr is not None:
            try:
                node = self.node_expr.resolve(context)
            except template.VariableDoesNotExist:
                pass
        node_list = []
        if node is not None:
            node_list = node.get_ancestors() + [node]
        context[self.tree_name] = __branch__(object, user=user, trace=node_list)       
        return ''

#@register.tag
def get_tree(parser, token):
    """
    Showing a container as a tree.

    Syntax::

        {% get_tree [container] activating [node] for [user] as [tree_name] %}
        {% get_tree [container] for [user] as [tree_name] %}
    """
    try:
        tokens = token.contents.split()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    if not len(tokens) == 8 and not len(tokens) == 6:
        raise template.TemplateSyntaxError("%r tag requires 5 or 7 arguments" % tokens[0])
    if len(tokens) == 8:
        if tokens[2] != 'activating':
            raise template.TemplateSyntaxError("Second argument in %r tag when is used with 7 parameters must be 'activating'" % tokens[0])    
        if tokens[4] != 'for':
            raise template.TemplateSyntaxError("Fourth argument in %r tag when is used with 7 parameters must be 'for'" % tokens[0])
        if tokens[6] != 'as':
            raise template.TemplateSyntaxError("Sixth argument in %r tag when is used with 7 parameters must be 'as'" % tokens[0])
        node_expr = parser.compile_filter(tokens[3])
        user_expr = parser.compile_filter(tokens[5])
        tree_name = tokens[7]
    else:
        if tokens[2] != 'for':
            raise template.TemplateSyntaxError("Second argument in %r tag when is used with 5 parameters must be 'for'" % tokens[0])
        if tokens[4] != 'as':
            raise template.TemplateSyntaxError("Fourth argument in %r tag when is used with 5 parameters must be 'as'" % tokens[0])
        node_expr = None
        user_expr = parser.compile_filter(tokens[3])
        tree_name = tokens[5]
    object_expr = parser.compile_filter(tokens[1])
    return ShowTreeNode(object_expr, node_expr, user_expr, tree_name)

register.tag(get_tree)
