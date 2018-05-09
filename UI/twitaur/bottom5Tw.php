<!DOCTYPE html>
<html lang="en">
<?php

//Sentiments
$responsePositive = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/positive?group_level=1&reduce=true&sorted=true');
$responseNegative = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/negative?group_level=1&reduce=true&sorted=true');
$responsePositive = json_decode($responsePositive, true);
$resultPositive=$responsePositive['rows'];

$highMapDataPosPerc=array();
$highMapDataNegPerc=array();
$np=0;
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
			$highMapDataPosPerc[$sub]=$sentPosPerc;
			$highMapDataNegPerc[$sub]=$sentNegPerc;
			$np=$np+1;
			break;
		}
	}
}

asort($highMapDataPosPerc);
$p=0;
$topHapK=array();
$topHapV=array();
foreach($highMapDataPosPerc as $x => $x_value) 
{
	$topHapK[$p]=$x;
	$topHapV[$p]=$x_value;
    if($p==5)
    {break;}
    $p=$p+1;
}


asort($highMapDataNegPerc);
$p=0;
$topSadK=array();
$topSadV=array();
foreach($highMapDataNegPerc as $x => $x_value) 
{
	$topSadK[$p]=$x;
	$topSadV[$p]=$x_value;
    if($p==5)
    {break;}
    $p=$p+1;
}



//TwitterActivity
$response = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/total?group_level=1&reduce=true');
$response = json_decode($response, true);
$result=$response['rows'];
$columnBasic="[";
$totalMelb=0;
$ignoredsuburb = 'N/A';
$totalMelbTweets=0;

foreach($result as $item){
    $subTweets = $item['value'];
    $test = $item['key']; 
    if($test == $ignoredsuburb)
    { continue;}
    $totalMelbTweets = $totalMelbTweets+$subTweets;
}
 

$twitterActivity=array();
foreach($result as $item) { 
    $suburb = $item['key'];
    $subTweets = $item['value']; 
    if($suburb == $ignoredsuburb)
    {continue;}
    $suburbPerc = round((($subTweets*100)/$totalMelbTweets),2);
    $twitterActivity[$suburb]=$suburbPerc;
}

// echo $twitterActivity;


asort($twitterActivity);
$formattedString="{ ";
$i=0;
$toptTwitK=array();
$toptTwitV=array();
foreach($twitterActivity as $x => $x_value) 
{
	if($x_value>10)
	{
	$topTwitK[$i]=$x;
	$topTwitV[$i]=$x_value;
    if($i==5)
    {break;}
    $i=$i+1;
	}
}







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
                        <li class="breadcrumb-item">Home</li>
                        <!-- <li class="breadcrumb-item active">Dashboard</li> -->
                    </ol>
                </div>
            </div>
            <!-- End Bread crumb -->
            <!-- Container fluid  -->
            <div class="container-fluid">
                <!-- Start Page Content -->
<!--Make sure the form has the autocomplete function switched off:-->

               <div class="row bg-white m-l-0 m-r-0 box-shadow ">

                    <!-- column -->
                    <div class="col-lg-4">
					  <div id="containerStatsHap"></div>
						
                    </div>
                    <!-- column -->

                    <!-- column -->
                    <div class="col-lg-4">
     
						  <div id="containerStatsUnHap"></div>
                    </div>
					
					<div class="col-lg-4">
     
						  <div id="containerStatsTweet"></div>
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





Highcharts.chart('containerStatsHap', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Happiest'
    },
    subtitle: {
        text: 'Twitter'
    },
    xAxis: {
        categories: [
            'Top 5 Positive Suburbs'
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
        name: '<?php echo $topHapK[0]?>',
        data: [<?php echo $topHapV[0]?>]
                              
    }                         
	, {                       
        name: '<?php echo $topHapK[1]?>',
        data: [<?php echo $topHapV[1]?>]
                              
    }                         
	, {                       
        name: '<?php echo $topHapK[2]?>',
        data: [<?php echo $topHapV[2]?>]
                              
    }, {                      
        name: '<?php echo $topHapK[3]?>',
        data: [<?php echo $topHapV[3]?>]
                              
    },                        
	{                         
        name: '<?php echo $topHapK[4]?>',
        data: [<?php echo $topHapV[4]?>]
    
    }
	]
});

Highcharts.chart('containerStatsUnHap', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Unhappiest'
    },
    subtitle: {
        text: 'Twitter'
    },
    xAxis: {
        categories: [
            'Top 5 Sad Suburbs'
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
        name: '<?php echo $topSadK[0]?>',
        data: [<?php echo $topSadV[0]?>]
                              
    }                         
	, {                       
        name: '<?php echo $topSadK[1]?>',
        data: [<?php echo $topSadV[1]?>]
                              
    }                         
	, {                       
        name: '<?php echo $topSadK[2]?>',
        data: [<?php echo $topSadV[2]?>]
                              
    }, {                      
        name: '<?php echo $topSadK[3]?>',
        data: [<?php echo $topSadV[3]?>]
                              
    },                        
	{                         
        name: '<?php echo $topSadK[4]?>',
        data: [<?php echo $topSadV[4]?>]
    
    }
	]
});

Highcharts.chart('containerStatsTweet', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Most Tweets'
    },
    subtitle: {
        text: 'Twitter'
    },
    xAxis: {
        categories: [
            'Top 5 Tweeting Suburbs'
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
        name: '<?php echo $topTwitK[0]?>',
        data: [<?php echo $topTwitV[0]?>]

    }
	, {
        name: '<?php echo $topTwitK[1]?>',
        data: [<?php echo $topTwitV[1]?>]
                              
    }                         
	, {                       
        name: '<?php echo $topTwitK[2]?>',
        data: [<?php echo $topTwitV[2]?>]
                              
    }, {                      
        name: '<?php echo $topTwitK[3]?>',
        data: [<?php echo $topTwitV[3]?>]
                              
    },                        
	{                         
        name: '<?php echo $topTwitK[4]?>',
        data: [<?php echo $topTwitV[4]?>]
    
    }
	]
});



</script>

</html>