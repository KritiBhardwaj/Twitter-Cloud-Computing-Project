<?php
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


arsort($twitterActivity);
$formattedString="{ ";
$i=0;
foreach($twitterActivity as $x => $x_value) 
{
    if($i==5)
    {break;}
    if($i==0)
        $formattedString= $formattedString."name: '".$x."',"."y: ".$x_value." },";
    else
        $formattedString= $formattedString."{"."name: '".$x."',"."y: ".$x_value." },";
    $i=$i+1;
}
rtrim($formattedString);
// echo $formattedString;



?>




<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Highcharts Example</title>

		<style type="text/css">

		</style>
	</head>
	<body>
<script src="../../code/highcharts.js"></script>
<script src="../../code/modules/exporting.js"></script>
<script src="../../code/modules/export-data.js"></script>

<div id="container" style="min-width: 310px; height: 400px; max-width: 600px; margin: 0 auto"></div>
        <script type="text/javascript">
            Highcharts.chart('container', {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: 'pie'
                },
                title: {
                    text: 'TOP 5 Tweeting Suburbs'
                },
                subtitle: {
                    text: '(Suburbs of Greater Melbourne)'
                },
                tooltip: {
                    pointFormat: '{series.name}'
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            format: '<b>{point.name}</b>',
                            style: {
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                            }
                        }
                    }
                },
                series: [{
                    name: 'Brands',
                    colorByPoint: true,
                    data: [<?php echo $formattedString;?>]
                }]
            });
        </script>
	</body>
</html>
