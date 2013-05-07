function gup(name)
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}

function set_initial(){
	var id = document.getElementById('id_relation').value;
	var href = window.location.href;
	if (href.indexOf("?") > -1){
		var relation_parm = gup('relation');
		if (relation_parm == "" ){
			var p = "";
			if (id != "") {
			    p = '&relation=' + id;
			}
			window.location = href + p;
		}
		else{
			var oldstr = 'relation='+relation_parm;
            if(id != ""){
                var newstr = 'relation='+id;
				href = href.replace(oldstr, newstr);
            }
			else{
				var pos = href.indexOf(oldstr) - 1;
				var newstr = '';
				if( href[pos] == '&'){
					href = href.replace('&'+oldstr, newstr);
				}
				else{
					if (href.indexOf("&") > -1) {
						href = href.replace(oldstr, newstr);
					}
					else{
						href = href.replace('?'+oldstr, newstr);
					}
				}
			}			
			window.location = href;
		}
	}
	else{
		if (id != "") {
			window.location = href + '?relation=' + id;
		}
		else{
			window.location = href;
		}
	}
}

django.jQuery(document).ready(function(){
	show_hidden();
});


function show_hidden(){
	var readonly = document.getElementById('id_readonly').value;
	if(readonly != ''){
        django.jQuery('.relation').addClass('hidden');
        django.jQuery('.readonly').removeClass('readonly');
    }
    var readonly_obj1 = document.getElementById('id_readonly_obj1').value;
    if(readonly_obj1 != ''){
        django.jQuery('.object1').addClass('hidden');
        django.jQuery('.readonly_obj1').removeClass('readonly_obj1');
    }   
    var readonly_obj2 = document.getElementById('id_readonly_obj2').value;
    if(readonly_obj2 != ''){
        django.jQuery('.object2').addClass('hidden');
        django.jQuery('.readonly_obj2').removeClass('readonly_obj2');
    }   
}
