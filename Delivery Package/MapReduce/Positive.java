/*Map*/
function(doc) {
  if(doc.sentiment=="positive")
   {
     emit(doc.suburb,1);
   }
}

/*Reduce*/
function (key, values, rereduce){
return sum(values);
}