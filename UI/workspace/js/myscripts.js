$( "#tab li" ).click(function() {
    var checkid = $(this).attr("id");
$(".container .wrapper").hide();
switch(checkid) {
    case "Map1":
        $("#container1").show();
        break;
    case "Chart2":
        $("#container2").show();
        break;
    case "Chart3":
        $("#container3").show();
        break;
    case "Chart4":
        $("#container4").show();
        break;
        
}
  console.log(checkid);
});