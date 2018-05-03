<!DOCTYPE HTML>
<?php
//echo "hello";
$responsePositive = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/positive?group_level=1&reduce=true&sorted=true');
$responseNegative = file_get_contents('http://115.146.95.134:5984/harvest_final/_design/suburbwisesents/_view/negative?group_level=1&reduce=true&sorted=true');
$responsePositive = json_decode($responsePositive, true);
$resultPositive=$responsePositive['rows'];

$highMapDataPosPerc="[";
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
			if($np==0)
			{
				$highMapDataPosPerc=$highMapDataPosPerc."["."'".$sub."',".$sentPosPerc."]";
			}
			else
			{
				$highMapDataPosPerc=$highMapDataPosPerc.",['".$sub."',".$sentPosPerc."]";
			}
			$np=$np+1;
			break;
		}
	}
}
$highMapDataPosPerc=$highMapDataPosPerc."]";
//echo $highMapDataPosPerc;
?>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Highmaps Example</title>

<style type="text/css">
#container {
    height: 500px; 
    min-width: 310px; 
    max-width: 800px; 
    margin: 0 auto; 
}
.loading {
    margin-top: 10em;
    text-align: center;
    color: gray;
}
</style>
	</head>
	<body>
<script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
<script src="../../code/highmaps.js"></script>
<script src="../../code/modules/data.js"></script>
<script src="../../code/modules/exporting.js"></script>
<script src="../../code/modules/offline-exporting.js"></script>

<div id="container"></div>



		<script type="text/javascript">

// Prepare random data
var data = <?php echo $highMapDataPosPerc; ?>;

$.getJSON('allsuburbs2.geo.json', function (geojson) {

    // Initiate the chart
    Highcharts.mapChart('container', {
        chart: {
            map: geojson
        },

        title: {
            text: 'Positivity Suburb Wise!'
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

        series: [{
            data: data,
            keys: ['name', 'value'],
            joinBy: 'name',
            name: 'Random data',
            states: {
                hover: {
                    color: '#a4edba'
                }
            },
            dataLabels: {
                enabled: true,
                format: '{point.properties.postal}'
            }
        }]
    });
});

		</script>
	</body>
</html>
