function copy_to_clipboard(url){
	var nodes = []
	jQuery.each(jQuery("#node_list").jqGrid('getGridParam','selarrrow'), function(k, v){
		nodes[k] = v.substring(5);
	});
	var nodes_raw = nodes.join('_');
	if(nodes.length>0){
		jQuery.ajax({
		    url: url,
		    type: 'POST',
		    beforeSend: function( xhr ) {
		    	$.blockUI();
			},
		    data: ({'nodes': nodes_raw}),
		    error: function(request, status, err){
		    	alert('Error!');
		    }
		});
	}
}