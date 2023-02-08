<?php

require_once("/home/tko/mopsi/WebRank/common.php");
error_reporting(E_ALL);								// this is for diplaying all errors
ini_set('Diplay errors',1); 						// this is for ini file file errors

$url="http://usindh.edu.pk";

$model="mac"; // which model to use
$classifier="dtree";//"knn","svm","mlp","forest","bayes"
$fold=1; // which fold to use
$top=5; // services should have 5

if (isset($_GET["url"])){
	$url=$_GET["url"];
}
if (isset($_GET["classifier"])){
	$classifier=$_GET["classifier"];
}
if (isset($_GET["top"])){
	$top=intval($_GET["top"]);
}

$file =fopen('io/url.txt','w') or die("unable to open file!");
fwrite($file,$url);
fclose($file);

echo $url;

//exec('python3 p100-B 2>&1', $output, $err);
exec('python3.6 drank_v2.py 2>&1', $output, $err);
if($err==1) {
    echo "PYTHON FAILED\n";
var_dump($output);
echo "<pre>   $err</pre>";
	die();
}

chdir("/home/tko/mopsi/WebRank");
$inputCSV="single_site_csv/wordFeatures.csv";
copy("/home/tko/himat/web-docs/Webrank/io/Score.txt",$inputCSV);



$pages=readPageWords($inputCSV);

$name="single_site";
if(!file_exists($featureVectorDirectory."/".$name)){
	mkdir($featureVectorDirectory."/".$name);
	chmod($featureVectorDirectory."/".$name,0777);
}

// generate the feature vector file
$featureVectorsFile=$featureVectorDirectory."/".$name."/testing_1.txt";
$myfile = fopen($featureVectorsFile, "w") or die("Unable to open file!");
fwrite($myfile, formatFileContents($pages));
fclose($myfile);

// generate the word mapping file
$wordFile=$featureVectorDirectory."/".$name."/testing_kw_1.txt";
$myfile = fopen($wordFile, "w") or die("Unable to open file!");
fwrite($myfile, formatKeywordFileContents($pages));
fclose($myfile);

if(!file_exists($resultDirectory."/".$name)){
	mkdir($resultDirectory."/".$name);
	chmod($resultDirectory."/".$name,0777);
}


$output = shell_exec('python3 '.$classifiersDirectory.$classifier."_test.py ".$model." ".$fold." ".$top." True");


$results=readResults($resultDirectory.$name."/".$classifier."_testing_1.txt");
$keywords=readKeywords($featureVectorDirectory."/".$name."/testing_kw_1.txt"); // reads keywords from separate file
for($i=0;$i<count($results);$i++){
	for($j=1;$j<count($results[$i]);$j++){ // skipping webpage ID (first)
		$results[$i][$j]=$keywords[$results[$i][$j]];
	}
}


$outFile=$resultDirectory.$name."/".$classifier."_result.txt";
$myfile = fopen($outFile, "w") or die("Unable to open file!");
fwrite($myfile, formatResultFileContents($results));
fclose($myfile);

$result="";
for($i=1;$i<count($results[0]);$i++){
	$result.= $results[0][$i]." ";
}


$outfile = fopen("/home/tko/himat/web-docs/Webrank/io/Keywords.txt", "w") or die("Unable to open file!");
fwrite($outfile, $result);
fclose($outfile);



//$link ="http://www.intersport.co.uk/en/stores/bristol-dw-sports-s10271";



?>
