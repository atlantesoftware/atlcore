function paste_from_clipboard(url){
	$.ajax({
	    url: url,
	    beforeSend: function( xhr ) {
		    $.blockUI();
		},
	    success: function(response, status, request){
	    	location.href=response;
	    },
	    error: function(request, status, err){
	    	alert('Error!')
	    }
	});
}