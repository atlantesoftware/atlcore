function format(key){
    var pos = key.indexOf('__');
    var info = [];
    info['app_label'] = key.substring(0, pos);
    info['model_name'] = key.substring(pos+2);
	return info
}

function model_url(info, url){
    var app_label = info['app_label'];
    var model_name = info['model_name'];
    return url+app_label+'/'+model_name+'/';
}

function add(key, url, container){
	var qs = '';
	var container_id = parseInt(container);
	if (container_id != NaN){
		qs = '?parent=' + container_id;
	}
    var info = format(key);
    var m_url = model_url(info, url);
    window.location = m_url + 'add/' + qs;
}

function desactivate_all(){
	var admin_views = document.getElementById('admin_views');
	if(admin_views != null) {
		admin_views.style.display = 'none';
	}	
	var to_add_models = document.getElementById('to_add_models');
    if(to_add_models != null) {
        to_add_models.style.display = 'none';
    }
    var admin_translations = document.getElementById('admin_translations');
    if(admin_translations != null) {
        admin_translations.style.display = 'none';
    }
    var admin_transitions = document.getElementById('admin_transitions');
    if(admin_transitions != null) {
        admin_transitions.style.display = 'none';
    }	
}

function activate(selector){
	desactivate_all();
	var contents_type = document.getElementById(selector);
	contents_type.style.display = 'block';
}

function go_to(url){
	window.location = url;
}
