var list;
var add_permissions;
var change_permissions;
var delete_permissions;

jQuery(document).ready(function(){
	list = jQuery('input[type="checkbox"][name="s_objects"]');
	add_permissions = jQuery('input[type="hidden"][name="add_permission"]');
	change_permissions = jQuery('input[type="hidden"][name="change_permission"]');
	delete_permissions = jQuery('input[type="hidden"][name="delete_permission"]');
    change_all();
});

jQuery('input[type="checkbox"][name="s_objects"]').live('click', function(){
    change_all();
});

function get_change_permission(pos){
	if(change_permissions.length){
		return 'True' == change_permissions[pos].value;
	}
	return false
}

function get_add_permission(pos){
	if(add_permissions.length){
		return 'True' == add_permissions[pos].value;
	}
	return false
}

function get_delete_permission(pos){
	if(delete_permissions.length){
		return 'True' == delete_permissions[pos].value;
	}
	return false
}

function activate_option(elem1, elem2){
    elem2.addClass('hidden');
    elem1.removeClass('hidden');	
}

function desactivate_option(elem1, elem2){
    elem2.removeClass('hidden');
    elem1.addClass('hidden');
}

function change_all(){
    var count = 0;
	
	// delete
    var e_del = jQuery('#enable_delete');
    var d_del = jQuery('#disable_delete');
    // copy
    var e_copy = jQuery('#enable_copy');
    var d_copy = jQuery('#disable_copy');
    // cut
    var e_cut = jQuery('#enable_cut');
    var d_cut = jQuery('#disable_cut');
    // translation
    //var e_translation = jQuery('#enable_translation');
    //var d_translation = jQuery('#disable_translation');
	
	var can_delete = true;
	var can_copy = true;
	var can_cut = true;
	var can_add = true;
    var can_change = true;
	
    for(var i=0; i<list.length; i++){
        if(list[i].checked){
			if(!get_delete_permission(i)){
				can_delete = false;
			}
            if(!get_change_permission(i)){
                can_change = false;
            }
            if(!get_add_permission(i)){
                can_add = false;
            }
            count++;
        }
    }
	
    if(count > 0 && can_delete){
        activate_option(e_del, d_del);
    }
    else{			
        desactivate_option(e_del, d_del);
    }
	
    if(count > 0 && can_copy){
        activate_option(e_copy, d_copy);
    }
    else{
        desactivate_option(e_copy, d_copy);
    }
	
    if(count > 0 && can_cut){
        activate_option(e_cut, d_cut);
    }
    else{
        desactivate_option(e_cut, d_cut);
    }
	/*
    if(count == 1 && can_add){
        activate_option(e_translation, d_translation);
    }
    else{
        desactivate_option(e_translation, d_translation);
    }  */ 
}

function submit_to(url){
	my_form = jQuery('#objects_list');
	my_form.attr('action', url);
	my_form.submit();
}
