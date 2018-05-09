/*Map*/
function(doc) {
emit([doc.suburb,doc.sentiment],1);
  
}

/*Reduce*/
function (key, values, rereduce){
return sum(values);
}