/*Map*/
function(doc) {
	var dt = new Date(doc.raw.created_at);
	time = dt.toGMTString().replace(',','').replace('GMT','').trim("").substring(4).replace(/ /g,"/");
	hour=dt.getUTCHours();
	emit(hour,1);
}

/*Reduce*/
function (key, values, rereduce){
return sum(values);
}