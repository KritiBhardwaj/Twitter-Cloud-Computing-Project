<!DOCTYPE html>
<html lang="en">
<?php
$responseAurin = file_get_contents('http://115.146.95.134:5984/aurin_born_overseas/_design/percentage/_view/percentage_overseas_aus');
$responseAurin = json_decode($responseAurin, true);
$result=$responseAurin['rows'];
$responsePositive = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/positive?group_level=1&reduce=true&sorted=true');
$responseNegative = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/negative?group_level=1&reduce=true&sorted=true');
$responsePositive = json_decode($responsePositive, true);
$resultPositive=$responsePositive['rows'];
$responseNegative = json_decode($responseNegative, true);
$resultNegative=$responseNegative['rows'];

$np=0;
$columnBasic="[";
$ignoredsuburb = 'N/A';
$twitterActivity=array();
$percentageArray=array();
$bornOverseas=array();

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
			if($np==0)
			{
                $happiness[$sub]=$sentPosPerc;
            }
			else
            {
                $happiness[$sub]=$sentPosPerc;
            }			
            $np=$np+1;
			break;
        }
        
    }
}

foreach($result as $item){
    $overseasPercentage = $item['value'][0]; 
    $suburbKey = $item['key'];
    //echo $overseasPercentage."<br>";
    if($suburbKey==$ignoredsuburb)
    {
        continue;
    }

    if($overseasPercentage<50)
    {
        continue;
    }

    $percentageArray[$suburbKey] = $overseasPercentage;  
}


asort($percentageArray);
$subData ="[";
$percData ="[";
$happinessOut="[";
foreach($percentageArray as $x => $x_value) 
{
    if(!is_nan($x_value))
	{
        foreach($happiness as $y => $y_value) 
        {
			if($y==$x)
			{
                $subData=$subData."'".$x."',";
                $percData=$percData.$x_value.",";
                $happinessOut = $happinessOut.$y_value.",";
			}
		}
    }
}

$subData=rtrim($subData,",");
$subData=$subData."]";
$percData=rtrim($percData,",");
$percData=$percData."]";
$happinessOut=rtrim($happinessOut,",");
$happinessOut=$happinessOut."]";
?>

<?php include 'header.php';?>

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
                    <h3 class="text-primary">Scenarios</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item"><a href="javascript:void(0)"></a>Sentiments</li>
                        <li class="breadcrumb-item active">Born Overseas</li>
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
                    <div class="col-lg-12">
						<div id="containerBO" ></div>	
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

Highcharts.chart('containerBO', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Born Overseas - Sentiment Analysis of Greater Melbourne'
    },
    subtitle: {
        text: '(Suburbs with highest Born Overseas Percentage vs the happiness levels)'
    },
    xAxis: {
        categories: <?php echo $subData;?>,
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
            '<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
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
    series: [
    {
        name: 'Happiness',
        data: <?php echo $happinessOut;?>
    },
    {
        name: 'Overseas',
        data: <?php echo $percData;?>

    }]
});
		</script>
	</body>
</html>
