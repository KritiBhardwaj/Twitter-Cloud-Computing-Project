<!DOCTYPE html>
<html lang="en">

<?php 

//Sports
//REPLACE API LINK
$responseSports=file_get_contents('http://115.146.95.134:5984/harvester/_design/attribute/_view/sports?group_level=1&reduce=true&sorted=true');
$responseSports = json_decode($responseSports, true);
$resultSports=$responseSports['rows'];

$totalSports=0;
foreach($resultSports as $item) {
    $subSports=$item['value'];
    $totalSports=$totalSports+$subSports;
}
echo $totalSports;

$highMapDataSportsPerc="[";
$cr=0;
foreach($resultSports as $item) {
    $sub=$item['key'];
    $subSports=$item['value'];
    // echo $subSports."<br>";
    $subSportsPerc=round((($subSports*100)/$totalSports),2);
    if($cr==0)
    {
        $highMapDataSportsPerc=$highMapDataSportsPerc."["."'".$sub."',".$subSportsPerc."]";
    }
    else
    {
        $highMapDataSportsPerc=$highMapDataSportsPerc.",['".$sub."',".$subSportsPerc."]";
    }
    $cr=$cr+1;
}
$highMapDataSportsPerc=$highMapDataSportsPerc."]";
//echo $highMapDataSportsPerc;

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
                    <h3 class="text-primary">Sports</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">Sports</a></li>
                        <li class="breadcrumb-item active">Subrub Wise</li>
                    </ol>
                </div>
            </div>
            <!-- End Bread crumb -->
            <!-- Container fluid  -->
            <div class="container-fluid">
                <!-- Start Page Content -->
				
                <div class="row bg-white m-l-0 m-r-0 box-shadow ">

				                  <!-- column -->
                    <div class="col-lg-3" >
						
                    </div>
                    <!-- column -->

				
                    <!-- column -->
                    <div class="col-lg-7" >
						<div id="containerMap"></div>
						
                    </div>
                    <!-- column -->
					
							                  <!-- column -->
                    <div class="col-lg-2" >
						
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

// Prepare random data
var data = <?php echo $highMapDataSportsPerc; ?>;





$.getJSON('allsuburbsTagged.geo.json', function (geojson) {
	
	
	// Prepare the geojson
    var cities = Highcharts.geojson(geojson, 'mappoint'),
        specialCityLabels = {
            'Melbourne Cricket Ground': {
                align: 'right'
            },
			'Etihad Stadium': {
                align: 'right'
            },
			'Hisense Arena': {
                align: 'right'
            },
			'Flemington Racecourse': {
                align: 'right'
            },
			'Rod Laver Arena': {
                align: 'right'
            },
			'Olympic Park Stadium': {
                align: 'right'
            },
			'Princes Park': {
                align: 'right'
            },
			'Melbourne Uni Sport Centre': {
                align: 'right'
            }
        };

    $.each(cities, function () {
        if (specialCityLabels[this.name]) {
            this.dataLabels = specialCityLabels[this.name];
        }
    });
    // Initiate the chart
    Highcharts.mapChart('containerMap', {
        chart: {
            map: geojson,
			width: 500,
            height: 500
        },

        title: {
            text: 'Sports Tweets Suburb Wise'
        },

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },

        colorAxis: {
            tickPixelInterval: 100,
			minColor: '#4d4dff', 
			maxColor: '#000099'
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
        series: [
	
		{
            data: data,
            keys: ['name', 'value'],
            joinBy: 'name',
            name: 'Sports%',
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
                        concole.log(this.name);
					//chart.series[1].data[0].update(55);
                    }
                }
            }
        }
		,	
		{
            name: 'Venues',
            type: 'mappoint',
            data: cities,
            color: '#ADD8E6',
            marker: {
                radius: 5
            },
            dataLabels: {
                align: 'left',
                verticalAlign: 'middle'
            },
            animation: false,
            tooltip: {
                pointFormat: '{point.name}'
            }
        }
		
		]
    });
});

	

</script>

<style>
.f32 .flag {
    vertical-align: middle !important;
}
</style>

</html>