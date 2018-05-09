<!DOCTYPE html>
<html lang="en">

<?php 

//Education
$responseAurinEducation = file_get_contents('http://115.146.95.134:5984/aurin_edu_occ_index/_design/view/_view/edu_occ_percentile');
$responseAurinEducation = json_decode($responseAurinEducation, true);
$resultEducation=$responseAurinEducation['rows'];
$ignoredsuburbEducation = 'N/A';
$percentageArrayEducation=array();
foreach($resultEducation as $itemEducation){
    $percentageEducation = $itemEducation['value']; 
    $suburbKeyEducation = $itemEducation['key'];
    //echo $item['key']."=>".$item['value'][0]."=>".$item['value'][1]."<br>";
    if($suburbKeyEducation==$ignoredsuburbEducation)
    {
        continue;
    }

    $percentageArrayEducation[$suburbKeyEducation] = $percentageEducation;  
}


//Economic
$responseAurinEconomic = file_get_contents('http://115.146.95.134:5984/aurin_eco_res_index/_design/view/_view/eco_res_percentile');
$responseAurinEconomic = json_decode($responseAurinEconomic, true);
$resultEconomic=$responseAurinEconomic['rows'];
$ignoredsuburbEconomic = 'N/A';
$percentageArrayEconomic=array();
foreach($resultEconomic as $itemEconomic){
    $percentageEconomic = $itemEconomic['value']; 
    $suburbKeyEconomic = $itemEconomic['key'];
    //echo $item['key']."=>".$item['value'][0]."=>".$item['value'][1]."<br>";
    if($suburbKeyEconomic==$ignoredsuburbEconomic)
    {
        continue;
    }

    $percentageArrayEconomic[$suburbKeyEconomic] = $percentageEconomic;  
}


//Born Overseas
$responseAurin = file_get_contents('http://115.146.95.134:5984/aurin_born_overseas/_design/percentage/_view/percentage_overseas_aus');
$responseAurin = json_decode($responseAurin, true);
$result=$responseAurin['rows'];
$ignoredsuburb = 'N/A';
$percentageArray= array();
foreach($result as $item){
    $overseasPercentage = $item['value'][0]; 
    $suburbKey = $item['key'];
    //echo $item['key']."=>".$item['value'][0]."=>".$item['value'][1]."<br>";
    if($suburbKey==$ignoredsuburb)
    {
        continue;
    }

    $percentageArray[$suburbKey] = $overseasPercentage;  
}


//Marital Code.
$responseMarital = file_get_contents('http://115.146.95.134:5984/aurin_marital/_design/suburbs/_view/details');
$responseMarital = json_decode($responseMarital, true);
$resultMarital=$responseMarital['rows'];
//echo '------>'.$responseMarital;

$maritalArray=array();
$i=0;
foreach($resultMarital as $itemMarital) {
	$sub=$itemMarital['key'];
	$p_tot_total=$itemMarital['value']['p_tot_total'];
	$p_tot_not_married=$itemMarital['value']['p_tot_not_married'];
	$p_tot_marrd_reg_marrge=$itemMarital['value']['p_tot_marrd_reg_marrge'];
	$p_tot_married_de_facto=$itemMarital['value']['p_tot_married_de_facto'];
	$totalPeople=$p_tot_total;
	$notMarriedPeoplePerc=round((($p_tot_not_married*100)/$totalPeople),2);
	$regMarriedPeoplePerc=round((($p_tot_marrd_reg_marrge*100)/$totalPeople),2);
	$defMarriedPeoplePerc=round((($p_tot_married_de_facto*100)/$totalPeople),2);
	//echo $sub.': Not Married %'.$notMarriedPeoplePerc.' | Reg Married %'.$regMarriedPeoplePerc.' | Fed Married %'.$defMarriedPeoplePerc.'<br>';
	$maritalArray[$sub]=$regMarriedPeoplePerc+$defMarriedPeoplePerc;																								;
	$i=$i+1;
 }

//Sentiments
$responsePositive = file_get_contents('http://115.146.95.134:5984/harvester/_design/suburbwisesents/_view/positive?group_level=1&reduce=true&sorted=true');
$responseNegative = file_get_contents('http://115.146.95.134:5984/harvester/_design/suburbwisesents/_view/negative?group_level=1&reduce=true&sorted=true');
$responsePositive = json_decode($responsePositive, true);
$resultPositive=$responsePositive['rows'];

$highMapDataPosPerc="[";
$np=0;
/*Negative tweets process!*/
$responseNegative = json_decode($responseNegative, true);
$resultNegative=$responseNegative['rows'];
$highMapDataPosPercOnly=array();
foreach($resultNegative as $itemNegative) {
	foreach($resultPositive as $itemPositive) {
		if($itemNegative['key']==$itemPositive['key'])
		{
			
			$sub=$itemNegative['key'];
			$sentPos=$itemPositive['value'];
			$sentNeg=$itemNegative['value'];
			$sentTotal=$sentPos+$sentNeg;
			$sentPosPerc=round((($sentPos*100)/$sentTotal),2);
			$sentNegPerc=round((($sentNeg*100)/$sentTotal),2);
			//echo "Suburb has positive and negative tweets: ".$itemNegative['key']."|".$itemPositive['key']."|".$sentTotal."=".$sentPos."+".$sentNeg."->Pos%:".$sentPosPerc."->Neg%:".$sentNegPerc."<br>";
			if($np==0)
			{
				$highMapDataPosPerc=$highMapDataPosPerc."["."'".$sub."',".$sentPosPerc."]";
				$highMapDataPosPercOnly[$sub]=$sentPosPerc;
			}
			else
			{
				$highMapDataPosPerc=$highMapDataPosPerc.",['".$sub."',".$sentPosPerc."]";
				$highMapDataPosPercOnly[$sub]=$sentPosPerc;
			}
			$np=$np+1;
			break;
		}
	}
}
$highMapDataPosPerc=$highMapDataPosPerc."]";

?>

<style>
* {
  box-sizing: border-box;
}
body {
  font: 16px Arial;  
}
.autocomplete {
  /*the container must be positioned relative:*/
  position: relative;
  display: inline-block;
}
input {
  border: 1px solid transparent;
  background-color: #f1f1f1;
  padding: 10px;
  font-size: 16px;
}
input[type=text] {
  background-color: #f1f1f1;
  width: 100%;
}
input[type=submit] {
  background-color: DodgerBlue;
  color: #fff;
  cursor: pointer;
}
.autocomplete-items {
  position: absolute;
  border: 1px solid #d4d4d4;
  border-bottom: none;
  border-top: none;
  z-index: 99;
  /*position the autocomplete items to be the same width as the container:*/
  top: 100%;
  left: 0;
  right: 0;
}
.autocomplete-items div {
  padding: 10px;
  cursor: pointer;
  background-color: #fff; 
  border-bottom: 1px solid #d4d4d4; 
}
.autocomplete-items div:hover {
  /*when hovering an item:*/
  background-color: #e9e9e9; 
}
.autocomplete-active {
  /*when navigating through the items using the arrow keys:*/
  background-color: DodgerBlue !important; 
  color: #ffffff; 
}
</style>


<?php include 'header.php';?>

<body class="fix-header fix-sidebar">
    <!-- Preloader - style you can find in spinners.css -->
    <div class="preloader">
        <svg class="circular" viewBox="25 25 50 50">
			<circle class="path" cx="50" cy="50" r="20" fill="none" stroke-width="2" stroke-miterlimit="10" /> </svg>
    </div>
    <!-- Main wrapper  -->
    <div id="main-wrapper">
        <!-- header header  -->
        <div class="header">
			<?php include 'nav.php';?>
        </div>
        <!-- End header header -->
			<?php include 'leftside.php';?>
        <!-- Page wrapper  -->
        <div class="page-wrapper">
            <!-- Bread crumb -->
            <div class="row page-titles">
                <div class="col-md-5 align-self-center">
                    <h3 class="text-primary">Dashboard</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">Home</li>
                        <!-- <li class="breadcrumb-item active">Dashboard</li> -->
                    </ol>
                </div>
            </div>
            <!-- End Bread crumb -->
            <!-- Container fluid  -->
            <div class="container-fluid">
                <!-- Start Page Content -->
				
				<div class="row">
				<span class="input-group-btn"><button class="btn btn-primary" type="submit"><i class="ti-search"></i></button></span>
				  <div class="autocomplete">
					<input id="myInput" type="text" name="myCountry" placeholder="Search Suburb">
				  </div>
				</div>
				<br><br>
				
                <div class="row bg-white m-l-0 m-r-0 box-shadow ">

                    <!-- column -->
                    <div class="col-lg-8">
						<div id="containerMap"></div>
						
                    </div>
                    <!-- column -->

                    <!-- column -->
                    <div class="col-lg-4">
     
						  <div id="containerStats"></div>
                    </div>
                    <!-- column -->
                </div>
 
                <!-- End PAge Content -->
            </div>
            <!-- End Container fluid  -->
            <!-- footer -->
			<?php include 'footer.php';?>
            <!-- End footer -->
        </div>
        <!-- End Page wrapper  -->
    </div>
    <!-- End Wrapper -->
<?php include 'footerScripts.php';?>

<script src="code/highcharts.js"></script>
<script src="code/map.js"></script>

</body>

<script>

  var pausecontent = new Array();
    <?php foreach($maritalArray as $x => $x_value) {?>
        pausecontent['<?php echo $x; ?>']= '<?php echo $x_value; ?>';
    <?php } ?>

	  var overseas = new Array();
    <?php foreach($percentageArray as $y => $y_value) {?>
        overseas['<?php echo $y; ?>']= '<?php echo $y_value; ?>';
    <?php } ?>

		  var education = new Array();
    <?php foreach($percentageArrayEducation as $z => $z_value) {?>
        education['<?php echo $z; ?>']= '<?php echo $z_value; ?>';
    <?php } ?>

		  var economic = new Array();
    <?php foreach($percentageArrayEconomic as $a => $a_value) {?>
        economic['<?php echo $a; ?>']= '<?php echo $a_value; ?>';
    <?php } ?>
	
			  var happy = new Array();
    <?php foreach($highMapDataPosPercOnly as $item => $item_value) {?>
        happy['<?php echo $item; ?>']= '<?php echo $item_value; ?>';
    <?php }
	echo $responsePositive;
	?>
	
	console.log("===>"+happy);
	
	<?php 
	$allSuburbs="[";
	foreach($percentageArrayEconomic as $a => $a_value) {
	$allSuburbs=$allSuburbs.'"'.$a.'",';
	}
	$allSuburbs=rtrim($allSuburbs);
	$allSuburbs=$allSuburbs."]";
	?>
	

// Prepare random data
var data = <?php echo $highMapDataPosPerc; ?>;

$.getJSON('allsuburbsTagged.geo.json', function (geojson) {

    // Initiate the chart
    Highcharts.mapChart('containerMap', {
        chart: {
            map: geojson
        },

        title: {
            text: 'Happiness at Suburb Level'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            tickPixelInterval: 100,
			minColor: '#62de62', 
			maxColor: '#059805'
        },
		/*
		tooltip: {
            backgroundColor: '#BDE1EF',
            borderWidth: 5,
            shadow: false,
            useHTML: true,
            pointFormat: '<span class="f32"><span class="flag {point.flag}"></span></span>' +
                ' {point.name}: <b>{point.value}</b>/km²'
        },
		*/
        series: [{
            data: data,
            keys: ['name', 'value'],
            joinBy: 'name',
            name: 'Happiness%',
            states: {
                hover: {
                    color: '#a4edba'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.properties.postal}'
            },
			point:{
                events:{
                    click: function(){
                        //alert(this.name);
						var chart = $('#containerStats').highcharts();
						 chart.xAxis[0].update({
						title:{
						text: this.name
						}
					});
					
					for (var x in pausecontent)
					{
						if(x==this.name)
						{
						var intvalue = Math.trunc( pausecontent[this.name] );
						console.log("Hello: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[0].data[0].update(intvalue);
	
						break;
						}
						
					}
					
					for (var y in overseas)
					{
						if(y==this.name)
						{
						var intvalue = Math.trunc( overseas[this.name] );
						console.log("Overseas%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[1].data[0].update(intvalue);
						break;
						}
						
					}
					
					console.log(education);
					for (var z in education)
					{
						if(z==this.name)
						{
						var intvalue = Math.trunc( education[this.name] );
						console.log("education%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[2].data[0].update(intvalue);
						break;
						}
						
					}
					
					console.log(economic);
					for (var a in economic)
					{
						if(a==this.name)
						{
						var intvalue = Math.trunc( economic[this.name] );
						console.log("economic%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[3].data[0].update(intvalue);
						break;
						}
						
					}
					
					console.log(happy);
					for (var a in happy)
					{
						if(a==this.name)
						{
						var intvalue = Math.trunc( happy[this.name] );
						console.log("happy%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[4].data[0].update(intvalue);
						break;
						}
						
					}
					
					//chart.series[1].data[0].update(55);
                    }
                }
            }
        }]
    });
});


		var a;
Highcharts.chart('containerStats', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Comparision Indexes'
    },
    subtitle: {
        text: 'Aurin'
    },
    xAxis: {
        categories: [
            'Suburb'
        ],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Percentage'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} % </b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        }
    },
    series: [{
        name: 'Marriage',
        data: [0]

    }
	, {
        name: 'Overseas',
       data: [0]
    
    }
	, {
        name: 'Education/Occupation',
        data: [0]
    
    }, {
        name: 'Economic',
        data: [0]
    
    },{
        name: 'Happiness',
        data: [0]
    
    }
	]
});

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
	  mySuburb=e.target.textContent;
	  console.log(e.target.textContent);
	  					for (var x in pausecontent)
					{
						if(x==mySuburb)
						{
						var intvalue = Math.trunc( pausecontent[mySuburb] );
						console.log("Hello: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[0].data[0].update(intvalue);
	
						break;
						}
						
					}
					
					for (var y in overseas)
					{
						if(y==mySuburb)
						{
						var intvalue = Math.trunc( overseas[mySuburb] );
						console.log("Overseas%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[1].data[0].update(intvalue);
						break;
						}
						
					}
					
					console.log(education);
					for (var z in education)
					{
						if(z==mySuburb)
						{
						var intvalue = Math.trunc( education[mySuburb] );
						console.log("education%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[2].data[0].update(intvalue);
						break;
						}
						
					}
					
					console.log(economic);
					for (var a in economic)
					{
						if(a==mySuburb)
						{
						var intvalue = Math.trunc( economic[mySuburb] );
						console.log("economic%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[3].data[0].update(intvalue);
						break;
						}
						
					}
					
					
					console.log(happy);
					for (var a in happy)
					{
						if(a==mySuburb)
						{
						var intvalue = Math.trunc( happy[mySuburb] );
						console.log("happy%: "+intvalue);
						
						chart = $('#containerStats').highcharts();
						chart.series[4].data[0].update(intvalue);
						break;
						}
						
					}
	  
      closeAllLists(e.target);
      });
}

/*An array containing all the country names in the world:*/
var countries = <?php echo $allSuburbs?>;

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("myInput"), countries);
</script>



<style>
.f32 .flag {
    vertical-align: middle !important;
}
</style>

</html>