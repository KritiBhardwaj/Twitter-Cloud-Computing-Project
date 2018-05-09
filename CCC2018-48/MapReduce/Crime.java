/*Map*/
function(doc) {
  	if(doc.crime>1)
		emit(doc.suburb, 1);
}

/*Reduce*/
function (key, values, rereduce){
return sum(values);
}