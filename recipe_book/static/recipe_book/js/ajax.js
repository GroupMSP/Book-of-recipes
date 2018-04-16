function httpGet(url, args) {
	var res = [];
	for (var arg in args){
	    res.push(arg+'='+args[arg])
	}
	var theUrl = url + '?' + res.join('&');
    
    var xmlHttp = null;
    xmlHttp = new XMLHttpRequest();

    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );

    return xmlHttp.responseText;
}