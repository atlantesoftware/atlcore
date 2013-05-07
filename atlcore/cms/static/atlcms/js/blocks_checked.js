var list;
var change_permissions;
var delete_permissions;
var columns_len;

jQuery(document).ready(function(){
	list = jQuery('input[type="checkbox"][name="s_objects"]');
    change_permissions = jQuery('input[type="hidden"][name="change_permission"]');
    delete_permissions = jQuery('input[type="hidden"][name="delete_permission"]');
	columns_len = jQuery('#columns_len').val();
    change_all();
});

function get_change_permission(pos){
    return 'True' == change_permissions[pos].value;
}

function get_delete_permission(pos){
    return 'True' == delete_permissions[pos].value;
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
    // change
    var e_chg = jQuery('#enable_change');
    var d_chg = jQuery('#disable_change');
    // move
    var e_mov = jQuery('#enable_move');
    var d_mov = jQuery('#disable_move');

    
    var can_delete = true;
    var can_change = true;
    
    for(var i=0; i<list.length; i++){
        if(list[i].checked){
            if(!get_delete_permission(i)){
                can_delete = false;
            }
            if(!get_change_permission(i)){
                can_change = false;
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
    
    if(count == 1 && can_change){
        activate_option(e_chg, d_chg);
    }
    else{
        desactivate_option(e_chg, d_chg);
    }
	
    if(count > 0 && can_change && (columns_len > 1)){
        activate_option(e_mov, d_mov);
    }
    else{           
        desactivate_option(e_mov, d_mov);
    }
}

function submit_to(url){
	my_form = jQuery('#objects_list');
	my_form.attr('action', url);
	my_form.submit();
}

