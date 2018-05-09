<!DOCTYPE html>
<html lang="en">

<?php 

//Crime
$responseCrime=file_get_contents('http://115.146.95.134:5984/aurin_born_overseas/_design/percentage/_view/percentage_overseas_aus');
$responseCrime = json_decode($responseCrime, true);
$resultCrime=$responseCrime['rows'];

$highMapDataCrimePerc="[";
$cr=0;
foreach($resultCrime as $item) {
    $sub=$item['key'];
    $sentCrime=$item['value'][0];
    // echo $sentCrime."<br>";

    if($cr==0)
    {
        $highMapDataCrimePerc=$highMapDataCrimePerc."["."'".$sub."',".$sentCrime."]";
    }
    else
    {
        $highMapDataCrimePerc=$highMapDataCrimePerc.",['".$sub."',".$sentCrime."]";
    }
    $cr=$cr+1;
}
$highMapDataCrimePerc=$highMapDataCrimePerc."]";
//echo $highMapDataCrimePerc;

?>

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
var data = <?php echo $highMapDataCrimePerc; ?>;





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
            text: 'Sports Tweets: Suburb Wise!'
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
        series: [
	
		{
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