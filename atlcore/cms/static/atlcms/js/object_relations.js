function showInPopup(triggeringLink, action){
    name = id_to_windowname(action);
    href = triggeringLink.href
    if (href.indexOf('?') == -1) {
        href += '?_popup=1';
    } else {
        href  += '&_popup=1';
    }
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}

function dismissPopup(win, newId, newRepr, url, durl) {
    // newId and newRepr are expected to have previously been escaped by
    // django.utils.html.escape.
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var action = windowname_to_id(win.name);
	var elem = document.getElementById('relation_list');
	var a1 = '<a onclick="return showInPopup(this, \'change\');" id="change_relation_'+newId+'" class="changelink" href="'+url+'"></a>';
	var a2 = '<a id="delete_relation_'+newId+'" class="deletelink" href="'+durl+'"></a>';
	var htm = newRepr+a1+a2;
	if (action == 'add'){
		var li = '<li class="related_item">'+htm+'</li>';
		elem.innerHTML += li;
	}
	else{
		var cli = document.getElementById('change_relation_'+newId).parentNode;
		cli.innerHTML = htm;
	}
	var relations = document.getElementById('relations');
	relations.style.display = 'block';
    win.close();
	//window.location.reload(true);
}