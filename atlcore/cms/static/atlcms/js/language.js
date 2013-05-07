function change_language(lang){
	var language = document.getElementById('language');
	language.value = lang;
	var language_form = document.getElementById('language_form');/*
	var url = document.getElementById('lang_'+lang+'_id');
	var next_trans_url = document.getElementById('next_trans_url');
	if(url!=undefined && url!=null && next_trans_url!=undefined && next_trans_url!=null){
		next_trans_url.setAttribute('value', url.value);
	}*/
	language_form.submit();
}
