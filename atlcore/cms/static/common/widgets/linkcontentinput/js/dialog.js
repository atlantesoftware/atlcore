//tinyMCEPopup.requireLangPack();

var ImageBrowserDialog = {
	
	init : function(ed, url) {
		//var f = document.forms[0];
		var that = this;
		// Get the selected contents as text and place it in the input
		//f.someval.value = tinyMCEPopup.editor.selection.getContent({format : 'text'});
		//f.somearg.value = tinyMCEPopup.getWindowArg('some_custom_arg');

		$(".node-content").live("click", function(){
			var pk = $('input',this).val();
			that.update(pk);
		});
		
		$("div.ui-small-content").live("click", function(){
			var picture_url = $(this).attr('rel');
			window.opener.document.getElementById('id_url').value = picture_url; 
			window.close();
		});

		
		this.update();
		
	},
	
	update : function(pk) {
		
		$.ajax({
			type: "GET",
			url: "/tinymce/contentbrowser/",
			data: {id : pk},
			success: function(data) {
				$('#gallery-content').html(data);												
			}			
		});
		
	},

	insert : function() {
		// Insert the contents from the input into the document
		//tinyMCEPopup.editor.execCommand('mceInsertContent', false, document.forms[0].someval.value);
		//tinyMCEPopup.close();
	}
};

ImageBrowserDialog.init();
//tinyMCEPopup.onInit.add(ImageBrowserDialog.init, ImageBrowserDialog);
