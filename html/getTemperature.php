<?php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', 'localhost');
define('DB_USERNAME', 'stu');
define('DB_PASSWORD', 'korona2020');
define('DB_NAME', 'bakalarka');

//variables
$query = "SELECT * FROM temperature";
$onlyLast = True;
$onlyRecent = True;
$showAll = False;

//clean up GET action
if(isset($_GET['limit'])) {

	if(is_numeric($_GET['limit'])) {

		switch ($_GET['limit']) {
			case '10':
				$limit = 10;
				break;
			case '50':
				$limit = 50;
				break;	
			default:
				$limit = 20;			
				break;
		}		
	}
	else {
		$onlyRecent = False;
		switch ($_GET['limit']) {
			case 'lastTen':
				$limit = 10;				
				break;
			case 'lastFifty':
				$limit = 50;
				break;	
			default:
				//we get all the data
				//$query = "SELECT * FROM temperature";
				$onlyLast = False; //pointless
				$showAll = True;
				break;
		}	
	}
}

//build query
if(!($showAll)) {
	$query = 
		"SELECT * FROM (
			SELECT * 
			FROM temperature "
			. ($onlyRecent ? "WHERE datetime > timestamp(DATE_SUB(NOW(), INTERVAL 30 MINUTE)) " : "") .
			"ORDER BY datetime desc "
			. ($onlyLast ? ("LIMIT " . $limit . " ") : "") . 
		") t 
		ORDER BY datetime asc";
}

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

//execute query
$result = $mysqli->query($query);

//copy returned data
$data = array();
foreach ($result as $row) {
	$data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

//now print the data
echo json_encode($data);
?>