function desactivate_all(){
	var to_add_models = document.getElementById('to_add_models');
    if(to_add_models != null) {
        to_add_models.style.display = 'none';
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
