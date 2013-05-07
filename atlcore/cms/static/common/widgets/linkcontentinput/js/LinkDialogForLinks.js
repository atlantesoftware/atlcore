

var LinkDialog = {
	preInit : function() {
		var url;

			},

	init : function() {
		
		$('#atlbrowsercontent-button').click(function(event){
			var dialog_url = "http://" + window.location.hostname + ":" + window.location.port + "/atlante_core_media/common/widgets/linkcontentinput/dialog.htm";
			window.open (dialog_url,"mywindow","menubar=1,resizable=1,scrollbars=1,width=800,height=600");
		});
	},

};
