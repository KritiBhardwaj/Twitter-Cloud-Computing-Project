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
                    <div class="col-lg-6">
					  <div id="containerStatsEco"></div>
						
                    </div>
                    <!-- column -->

                    <!-- column -->
                    <div class="col-lg-6">
     
						  <div id="containerStatsEdu"></div>
                    </div>
					   </div>
					   
					    <div class="row bg-white m-l-0 m-r-0 box-shadow ">
					<div class="col-lg-6">
     
						  <div id="containerStatsMar"></div>
                    </div>
					
					<div class="col-lg-6">
     
						  <div id="containerStatsOve"></div>
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

	
	    <?php 
	
	arsort($percentageArrayEducation);
	$u=0;
	$topEduK=array();
	$topEduV=array();
	foreach($percentageArrayEducation as $z => $z_value) {
	$topEduK[$u]=$z;
	$topEduV[$u]=$z_value;
	if($u==5)
	{break;}
	$u=$u+1;
	} 
	?>
	
	
    <?php 
	
	arsort($percentageArrayEconomic);
	$e=0;
	$topEcoK=array();
	$topEcoV=array();
	foreach($percentageArrayEconomic as $a => $a_value) {
	$topEcoK[$e]=$a;
	$topEcoV[$e]=$a_value;
	if($e==5)
	{break;}
	$e=$e+1;
	} 
	?>
	
console.log("<?php echo $topEduK[0]."=>".$topEduV[0]?>");	

Highcharts.chart('containerStatsEco', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Economic Index'
    },
    subtitle: {
        text: 'Aurin'
    },
    xAxis: {
        categories: [
            'Economic Index'
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
        name: '<?php echo $topEcoK[0]?>',
        data: [<?php echo $topEcoV[0]?>]

    }
	, {
        name: '<?php echo $topEcoK[1]?>',
        data: [<?php echo $topEcoV[1]?>]
    
    }
	, {
        name: '<?php echo $topEcoK[2]?>',
        data: [<?php echo $topEcoV[2]?>]
    
    }, {
        name: '<?php echo $topEcoK[3]?>',
        data: [<?php echo $topEcoV[3]?>]
    
    },
	{
        name: '<?php echo $topEcoK[4]?>',
        data: [<?php echo $topEcoV[4]?>]
    
    }
	]
});


Highcharts.chart('containerStatsEdu', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Education/Occupation Index'
    },
    subtitle: {
        text: 'Aurin'
    },
    xAxis: {
        categories: [
            'Economic Index'
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
        name: '<?php echo $topEduK[0]?>',
        data: [<?php echo $topEduV[0]?>]

    }
	, {
        name: '<?php echo $topEduK[1]?>',
        data: [<?php echo $topEduV[1]?>]
    
    }
	, {
        name: '<?php echo $topEduK[2]?>',
        data: [<?php echo $topEduV[2]?>]
    
    }, {
        name: '<?php echo $topEduK[3]?>',
        data: [<?php echo $topEduV[3]?>]
    
    },
	{
        name: '<?php echo $topEduK[4]?>',
        data: [<?php echo $topEduV[4]?>]
    
    }
	]
});


Highcharts.chart('containerStatsMar', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Marital Status'
    },
    subtitle: {
        text: 'Aurin'
    },
    xAxis: {
        categories: [
            'Economic Index'
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
        name: 'Suburb1',
        data: [100]

    }
	, {
        name: 'Suburb2',
       data: [80]
    
    }
	, {
        name: 'Suburb3',
        data: [60]
    
    }, {
        name: 'Suburb4',
        data: [40]
    
    },
	{
        name: 'Suburb5',
        data: [20]
    
    }
	]
});


Highcharts.chart('containerStatsOve', {
    chart: {
        type: 'column'
    },
    title: {
        text: 'Born Overseas'
    },
    subtitle: {
        text: 'Aurin'
    },
    xAxis: {
        categories: [
            'Economic Index'
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
        name: 'Suburb1',
        data: [100]

    }
	, {
        name: 'Suburb2',
       data: [80]
    
    }
	, {
        name: 'Suburb3',
        data: [60]
    
    }, {
        name: 'Suburb4',
        data: [40]
    
    },
	{
        name: 'Suburb5',
        data: [20]
    
    }
	]
});



</script>

</html>