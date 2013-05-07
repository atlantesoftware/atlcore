$(document).ready(function(){
	jQuery("#node_list").jqGrid('sortableRows', {
		update: function(event, ui){
			//Si en algun momento no funciona, chequear que los id de los nodos 
			//se esten creados en el formado node_<id> donde id es el identificador
			//del resgistro
			var ajax_request = {};
			ajax_request.url = "/atlcms/jqgridnode/sortorder/";
			ajax_request.type = "GET";
			ajax_request.data = $(this).sortable('serialize');
			ajax_request.context = document.body;
			$.ajax(ajax_request);
		}});
		
		
	jQuery("#node_list").jqGrid("setGridParam", {
		//onSelectRow: function(rowid, iRow, iCol, e){
		//	var row = jQuery("#node_list").jqGrid("getRowData", rowid);
	//		window.location = row.admin_url;
		//},	
		onCellSelect: function(rowid, iCol, cellcontent, e){
			if (iCol > 0) {
				var row = jQuery("#node_list").jqGrid("getRowData", rowid);
				window.location = row.admin_url;
			}
			else {							
				var s; 
				s = $('#node_list').jqGrid('getGridParam','selarrrow'); 
				if (s.length > 0) {
					jQuery("#button_delete").button({"disabled": true });
					$("#t_node_list").show();
				} 					
				else {
					jQuery("#button_delete").button({"disabled": false });
					$("#t_node_list").hide();
				}
					
			};
		},
		loadError: function(xhr,status, error){
			alert(error);
		},
	}).trigger("reloadGrid");
	
	jQuery("#t_node_list").append('<button id="node_list_delete_button">delete</button>');
	jQuery("#node_list_delete_button").button({"disabled": false, "text": 0, "label": "Delete", "icons": {"primary": "ui-icon-trash"}});	
	jQuery("#t_node_list").hide();
	
	
	jQuery("#node_list_delete_button").click(function() {
		
		var node_list = jQuery("#node_list").jqGrid('getGridParam','selarrrow');		
		var confirmMessage = '<ul>'; 
		for (var i = 0; i < node_list.length; i++) {
			var rowdata = $("#node_list").getRowData(node_list[i]);
			confirmMessage += '<li> '+ rowdata.title + '</li>';			
		}
		confirmMessage +='</ul>';
		
		var dialogOpts = {
			title: '¿Está seguro que desea borrar?',
			modal: true,
			bgiframe : true,
			autoOpen : false,
			buttons: {
				"Ok": function() {					
					$.ajax({
						url: "/atlcms/jqgridnode/deletedata/",
						data: {node_list : $.toJSON(node_list)},
						success: function(data) {
							jQuery("#node_list").trigger("reloadGrid");	
							jQuery("#button_delete").button({"disabled": false });
							jQuery("#t_node_list").hide();						
						},
						error: function() {
							alert('Ha ocurrido un error');
						}
					});
					jQuery('#atlcms-dialog').dialog('close');
				},
				"Cancelar": function() {
					jQuery('#atlcms-dialog').dialog('close');
				}				
			}
		};
		
		jQuery('#atlcms-dialog').html(confirmMessage);
		jQuery("#atlcms-dialog").dialog(dialogOpts); 
		jQuery('#atlcms-dialog').dialog('open');
		return false;
	});
	
	jQuery("#node_list").hideCol("slug");
	jQuery("#node_list").hideCol("image");
	jQuery("#node_list").hideCol("language");
	jQuery("#node_list").hideCol("neutral");
	jQuery("#node_list").hideCol("image");
	jQuery("#node_list").hideCol("parent");
	jQuery("#node_list").hideCol("admin_url");
	jQuery("#node_list").hideCol("admin_change_url");
	jQuery("#node_list").hideCol("admin_delete_url");
	jQuery("#node_list").hideCol("updated_on");
	jQuery("#node_list").hideCol("created_on");
	jQuery("#node_list").hideCol("description");
}) 