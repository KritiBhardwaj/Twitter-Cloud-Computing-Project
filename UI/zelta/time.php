<!DOCTYPE html>
<html lang="en">
<?php
$response = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/total?group_level=1&reduce=true');
$response = json_decode($response, true);
$result=$response['rows'];
$columnBasic="[";
$totalMelb=0;
$ignoredsuburb = 'N/A';

$totalsuburbs;
foreach($result as $item){
    $subTweets = $item['value']; 
    $test = $item['key']; 
    if($test == $ignoredsuburb)
            continue; 
    $totalMelb = $totalMelb+$subTweets;
    $totalsuburbs++;   
}

$suburbIterator=0;
$OutputString="{ ";
foreach($result as $item) { 
    $formattedString="{ ";
    $suburb = $item['key'];
    $subTweets = $item['value']; 
    if($suburb == $ignoredsuburb)
        continue;
    $suburbPerc = round((($subTweets*100)/$totalMelb),2);
    
    if(!empty($suburb))
    {
        if($suburbPerc>0.5)
        {
            $suburbIterator++;
            if($suburbIterator < $totalsuburbs-1)
                $formattedString= $formattedString."name: '".$suburb."',"."y: ".$suburbPerc." },";
            else
                $formattedString= $formattedString."name: '".$suburb."',"."y: ".$suburbPerc." }";
        
            $outputString = $outputString.$formattedString;
        }
    }
}

//echo $outputString;

//format: {name:'value',y:value},{key:value,key:value},{key:value,key:value}
?>



<?php
$response1 = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/timebased/_view/time?reduce=true&group=true');

$response1 = json_decode($response1, true);
// echo $response1['rows'];

$count="[";
$countX="[";
foreach($response1['rows']as $test) {
    // echo $test['key']."=>".$test['value']."<br>";
    $count=$count.$test['value'].",";
	$countX=$countX."'".$test['key']."',";
}
$count=rtrim($count,",");
$count=$count."]";

$countX=rtrim($countX,",");
$countX=$countX."]";

?>


<?php include 'header.php';?>
	<head>

		<style type="text/css">
#container {
	min-width: 310px;
	max-width: 800px;
	height: 400px;
	margin: 0 auto
}
		</style>
	</head>
<body class="fix-header fix-sidebar">
    <!-- Preloader - style you can find in spinners.css -->
    <div class="preloader">
        <svg class="circular" viewBox="25 25 50 50">
			<circle class="path" cx="50" cy="50" r="20" fill="none" stroke-width="2" stroke-miterlimit="10" /> </svg>
    </div>
	
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
                    <h3 class="text-primary">General</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="javascript:void(0)">General</a></li>
                        <li class="breadcrumb-item active">Activity</li>
                    </ol>
                </div>
            </div>
            <!-- End Bread crumb -->
            <!-- Container fluid  -->
            <div class="container-fluid">
                <!-- Start Page Content -->
                <div class="row">
 
                </div>

                <div class="row bg-white m-l-0 m-r-0 box-shadow ">

                    <!-- column -->
                    <div class="col-lg-6">
						<div id="containerAct"></div>		
                    </div>
                    <!-- column -->

                    <!-- column -->
                    <div class="col-lg-6">
                  <div id="containerPie"></div>
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
	


<?php include 'footerScripts.php';?>
<script src="charts/code/highcharts.js"></script>
<script src="charts/code/modules/series-label.js"></script>
<script src="charts/code/modules/exporting.js"></script>
<script src="charts/code/modules/export-data.js"></script>




<script type="text/javascript">

 Highcharts.chart('containerPie', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'Twitter Activity Profile of Greater Melbourne'
                },
                subtitle: {
                    text: '(Suburbs with greater than 0.5% Tweets)'
                },
                tooltip: {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Brands',
                    colorByPoint: true,
                    data: [<?php echo $outputString;?>]
                }]
            });

Highcharts.chart('containerAct', {

    title: {
        text: 'Twitter Activity by the Hour in Greater Melbourne'
    },

    subtitle: {
        text: 'Source: Twitter'
    },
	xAxis: {
        categories: <?php echo $countX; ?>
    },
    yAxis: {
        title: {
            text: 'Number of Tweets'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
           line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true,
			allowPointSelect:true,
			pointStart:0
        }
    },

    series: [{
        name: 'Twitter Activity',
        data: <?php echo $count; ?>
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

});
		</script>
	</body>
</html>
