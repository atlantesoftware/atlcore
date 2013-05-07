

function AtlContactForm_clear_data(id, value){
	input = $('#' + id);
	if (input.val() == value) {
		$('#' + id).val('');	
	}
}

function AtlContactForm_update_data(id, value){
	input = $('#' + id);
	if (input.val() == '') {
		$('#' + id).val(value);	
	}
}
