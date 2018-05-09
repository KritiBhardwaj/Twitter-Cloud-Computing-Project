<!DOCTYPE html>
<html lang="en">
<?php
//Sentiment Code;
$responsePositive = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/positive?group_level=1&reduce=true&sorted=true');
$responseNegative = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/negative?group_level=1&reduce=true&sorted=true');
$responsePositive = json_decode($responsePositive, true);
$resultPositive=$responsePositive['rows'];

$highMapDataPosPerc="[";
$np=0;
$sentimentArray=array();
/*Negative tweets process!*/
$responseNegative = json_decode($responseNegative, true);
$resultNegative=$responseNegative['rows'];
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
				$sentimentArray[$sub]=$sentPosPerc;
			}
			else
			{
				$highMapDataPosPerc=$highMapDataPosPerc.",['".$sub."',".$sentPosPerc."]";
				$sentimentArray[$sub]=$sentPosPerc;
			}
			$np=$np+1;
			break;
		}
	}
}
$highMapDataPosPerc=$highMapDataPosPerc."]";


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

asort($maritalArray);
$xAxisM="[";
$yAxisM="[";
$yAxisS="[";
foreach($maritalArray as $x => $x_value) {
    
	if(!is_nan($x_value))
	{
		foreach($sentimentArray as $y => $y_value) {
			if($y==$x)
			{
				//echo "Subub Matched!";
				$xAxisM=$xAxisM."'".$x."',";
				$yAxisM=$yAxisM.$x_value.",";
				$yAxisS=$yAxisS.$y_value.",";
			}
		}

		//echo "Key=" . $x . ", Value=" . $x_value."<br>";
	}
}
$xAxisM=rtrim($xAxisM,",");
$xAxisM=$xAxisM."]";
$yAxisM=rtrim($yAxisM,",");
$yAxisM=$yAxisM."]";
$yAxisS=rtrim($yAxisS,",");
$yAxisS=$yAxisS."]";
//echo $yAxisM;

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
                    <h3 class="text-primary">Sentiments</h3> </div>
                <div class="col-md-7 align-self-center">
                    <ol class="breadcrumb">
                        <li class="breadcrumb-item">Sentiments</li>
                        <li class="breadcrumb-item active">Marital Status</li>
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
						<div id="containerMA" ></div>	
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
Highcharts.chart('containerMA', {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Marriage Percentage of Suburbs'
    },
    subtitle: {
        text: 'Source: Aurin.com.au | Twitter.com'
    },
    xAxis: {
        categories: <?php echo $xAxisM; ?>
    },
    yAxis: {
        title: {
            text: 'Percentage Married'
        }
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
        name: 'Married %',
        data: <?php echo $yAxisM; ?>,
		color: '#88cae0'
    },
	{
        name: 'Sentiments +ve %',
        data: <?php echo $yAxisS; ?>,
		color: '#abf282'
    }
	]
}
);

		</script>
	</body>
</html>
