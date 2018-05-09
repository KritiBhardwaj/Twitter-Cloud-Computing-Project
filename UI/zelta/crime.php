<!DOCTYPE html>
<html lang="en">

<?php 

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
echo $highMapDataCrimePerc;

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
                    <h3 class="text-primary">Dashboard</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="javascript:void(0)">Home</a></li>
                        <li class="breadcrumb-item active">Dashboard</li>
                    </ol>
                </div>
            </div>
            <!-- End Bread crumb -->
            <!-- Container fluid  -->
            <div class="container-fluid">
                <!-- Start Page Content -->

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


// Prepare random data
var data = <?php echo $highMapDataCrimePerc; ?>;

$.getJSON('allsuburbsTagged.geo.json', function (geojson) {

    // Initiate the chart
    Highcharts.mapChart('containerMap', {
        chart: {
            map: geojson
        },

        title: {
            text: 'Crime Rate Suburb Wise!'
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
					
					//chart.series[1].data[0].update(55);
                    }
                }
            }
        }]
    });
});


		
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
        name: 'Marriage Percentage',
        data: [0]

    }
	, {
        name: 'Overseas Percentage',
       data: [0]
    
    }
	//, {
    //    name: 'London',
    //    data: [48.9]
    //
    //}, {
    //    name: 'Berlin',
    //    data: [42.4]
    //
    //}
	]
});

</script>

<style>
.f32 .flag {
    vertical-align: middle !important;
}
</style>

</html>