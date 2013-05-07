#coding=UTF-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.widgets import SelectMultiple, Select
from django.utils.safestring import mark_safe

#from atlcore.settings import MEDIA_URL
MEDIA_URL = "/static/" # CHEQUEAR ESTE PARCHE QUE CUANDO QUITO EL COMENTARIO DE LA LÍNEA DE ARRIBA DA ERROR DE IMPORT CIRCULAR

class AtlAspectWidget(SelectMultiple):
    
    def render(self, name, value, attrs=None, choices=()):
        list_view = reverse('root-aspects')
        html = super(AtlAspectWidget, self).render(name, value, attrs, choices) + mark_safe('<div id="aspect_tree"></div>')
        return html + mark_safe(u'''
            <script type="text/javascript">
            jQuery(function(){ 
                function get_id(){
                    return '%s';
                }
                function get_original_id(){
                    var id = get_id();
                    return id.replace('id_', 'id_original_');
                }
                function unique(arr) {
                  var a = [];
                  var l = arr.length;
                  for(var i=0; i<l; i++) {
                    for(var j=i+1; j<l; j++) {
                      // If arr[i] is found later in the array
                      if (arr[i] === arr[j])
                        j = ++i;
                    }
                    a.push(arr[i]);
                  }
                  return a;
                }    
                function build_option_element(node_id){
                        var id = node_id.replace("node_","");
                        var css_id = '#' + node_id + ' > a';
                        var text = jQuery(css_id).text().trim();
                        return '<option value="' + id + '" selected="selected">' + text + '</option>';                
                }       
                function set_values(){
                    var l = Array();
                    var ext_l = Array();
                    jQuery(".jstree-checked").each(function(){
                        var node_id = jQuery(this).attr('id');
                        var opt = build_option_element(node_id);
                        l.push(opt);
                        var node = jQuery('#' + node_id);
                        ext_l = ext_l.concat(jQuery("#aspect_tree").jstree("get_path", node, true));             
                    });
                    jQuery("#"+get_original_id()).html(l.join(','));
                    ext_l = unique(ext_l);
                    var f = Array();
                    for(var i=0; i<ext_l.length; i++){
                        var opt = build_option_element(ext_l[i]);
                        f.push(opt);
                    }
                    jQuery("#"+get_id()).html(f.join(','));
                }                        
                function current_values(){
                    var ids = Array();
                    jQuery("#"+get_original_id()+" > option").filter("[selected]='selected'").each(function(){
                        ids.push('node_' + jQuery(this).val());
                    });
                    return ids;             
                }
                function to_open(){
                    var ids = Array();
                    jQuery("#"+get_original_id()+" > option").each(function(){
                        ids.push('node_' + jQuery(this).val());
                    });
                    return ids;                      
                }
                jQuery("#aspect_tree")
                .bind("loaded.jstree", function (event, data) {
                    jQuery("#"+get_original_id()).parent().parent().css('display', 'none');
                    jQuery("#"+get_id()).css('display', 'none');
                })        
                .bind('change_state.jstree', function (event, data) {
                    set_values();
                })                    
                .jstree({ 
                    "json_data" : {
                        "ajax" : {
                            "url" : function (n) {
                                var id = n.attr ? n.attr("id").replace("node_","") : 0;
                                return "%s" + id;
                            },
                            "data" : function (n) { 
                                var node_id = n.attr ? n.attr("id").replace("node_","") : 0;
                                return { id : node_id };
                            }
                        }
                    },
                    "core" : {
                        "initially_open" : to_open()
                    },                      
                    "ui" : {
                        "initially_select" : current_values(),
                        "selected_parent_close": false
                    },                             
                    "plugins" : [ "themes", "json_data", "ui", "checkbox"]
                });              
            });
            </script>        
        ''' % (attrs['id'], list_view))
    
    class Media:
        css = {
            'all': (MEDIA_URL + 'aspect/css/jstree.css',)
        }
        js = (
            MEDIA_URL + 'aspect/js/jquery.js',
            MEDIA_URL + 'aspect/js/jquery.cookie.js',
            MEDIA_URL + 'aspect/js/jquery.hotkeys.js',
            MEDIA_URL + 'aspect/js/jquery.jstree.js',
        )
        
class AtlAspectForeignKeyWidget(Select):
    
    def render(self, name, value, attrs=None, choices=()):
        list_view = reverse('root-aspects')
        html = super(AtlAspectForeignKeyWidget, self).render(name, value, attrs, choices=()) + mark_safe('<div id="aspect_tree"></div>')
        return html + mark_safe(u'''
            <script type="text/javascript">
            var clicked = false;
            jQuery(function(){ 
                function get_id(){
                    return '%s';
                }
                function to_open(){
                    var ids = Array();
                    jQuery("#"+get_id()+" > option").each(function(){
                        ids.push('node_' + jQuery(this).val());
                    });
                    return ids;                      
                }      
                function set_value(node_id){
                    jQuery("#"+get_id()).val(node_id.replace("node_",""));
                }
                function rm_value(){
                    jQuery("#"+get_id()).val('');
                }                
                jQuery("#aspect_tree") 
                .bind("loaded.jstree", function (event, data) {
                    jQuery("#"+get_id()).css('display', 'none');
                })
                .bind('select_node.jstree', function (event, data) {
                    if(clicked){
                        set_value(data.rslt.obj.attr('id'));
                    }
                    clicked = false;
                })                                      
                .bind('click.jstree', function (event, data) {
                    clicked = true;
                    rm_value();
                })                  
                .jstree({ 
                    "json_data" : {
                        "ajax" : {
                            "url" : function (n) {
                                var id = n.attr ? n.attr("id").replace("node_","") : 0;
                                return "%s" + id;
                            },
                            "data" : function (n) { 
                                var node_id = n.attr ? n.attr("id").replace("node_","") : 0;
                                return { id : node_id };
                            }
                        }
                    },
                    "core" : {
                        "initially_open" : to_open()
                    },                      
                    "ui" : {
                        "initially_select" : ['#node_' + jQuery("#"+get_id()).val()],
                        "selected_parent_close": false,
                        "select_limit": 1
                    },                             
                    "plugins" : [ "themes", "json_data", "ui"]
                });              
            });
            </script>        
        ''' % (attrs['id'], list_view))
    
    class Media:
        css = {
            'all': (MEDIA_URL + 'aspect/css/jstree.css',)
        }
        js = (
            MEDIA_URL + 'aspect/js/jquery.js',
            MEDIA_URL + 'aspect/js/jquery.cookie.js',
            MEDIA_URL + 'aspect/js/jquery.hotkeys.js',
            MEDIA_URL + 'aspect/js/jquery.jstree.js',
        )
