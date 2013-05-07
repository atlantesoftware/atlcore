/*!
 * AtlanteSoftware JavaScript Core Library
 * http://www.atlantesoftware.com/js/atlcore
 *
 * Copyright 2011, AtlanteSoftware
 * licensed under GPL Version 2 licenses.
 *
 */

// *************DEPRECATE**************
function atl_includelibrary(library_id, library_url){
	if (document.getElementById(library_id) == null) {
		var head = document.getElementsByTagName('head').item(0);
		var script = document.createElement('script');
		script.id= library_id;
		script.type = 'text/javascript';
		script.src = library_url;
		//script.onload = function (){alert(library_url)};
		head.appendChild(script);
		//$.getScript(library_url, function (){jQuery('#home_carousel').jcarousel();}); 
	};
};

function atl_includestyle(style_id, style_url){
	if (document.getElementById(style_id) == null) {
		var head = document.getElementsByTagName('head').item(0);
		var link = document.createElement('link');
		link.id= style_id;
		link.rel = "stylesheet"
		link.type = "text/css";
		link.href = style_url;
		head.appendChild(link);
	};
};

atl_context = Object();

function atl_ajax_panel(component){
	return '#' + component + '_ajax_panel';
}

function atl_ajax_loading_panel(component){
	return '#' + component + '_ajax_loading';
}

function atl_ajax_success_panel(component){
	return '#' + component + '_ajax_success';
}

function atl_ajax_error_panel(component){
	return '#' + component + '_ajax_error';
}

function atl_ajax_error_message_panel(component){
	return '#' + component + '_ajax_error_message';
}

function atl_ajax_close_message(component){
	$('#' + component + '_ajax_success').css('display', 'none');
	$('#' + component + '_ajax_panel').css('display', 'none');
	$('#' + component + 'ajax_panel button').css('display', 'none');
}

function atl_ajax_request(url, data, component){
	  $.ajax({
	  type: 'POST',
	  url: url,
	  data: data,
	  beforeSend:function(){
	    // this is where we append a loading image
	    $(atl_ajax_panel(component)).css('display', 'Block');
	    $(atl_ajax_loading_panel(component)).css('display', 'Block');
	  },
	  success:function(data){
	    // successful request; do something with the data
	    //$('#ajax-panel').empty();
	    //$(data).find('item').each(function(i){
	      //$('#ajax-panel').append('<h4> OK</h4><p>texto de OK</p>');
	      $(atl_ajax_loading_panel(component)).css('display', 'none');
	      $(atl_ajax_panel(component)+' button').css('display', 'block');
	      $(atl_ajax_success_panel(component)).css('display', 'block');
	      $(atl_ajax_error_message_panel(component)).html(data);
	    //});
	  },
	  error:function(){
	    // failed request; give feedback to user
	      $(atl_ajax_loading_panel(component)).css('display', 'none');
	      $(atl_ajax_error_panel(component)).css('display', 'block');
	      
	  }
	});
}

