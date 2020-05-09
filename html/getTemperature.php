<?php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', 'localhost');
define('DB_USERNAME', 'stu');
define('DB_PASSWORD', 'korona2020');
define('DB_NAME', 'bakalarka');

function is_datetime($dt) {
    if (isset($_GET['dt'])) {
        if (is_string($dt)) {
            if (strptime($dt, '%Y-%m-%d %H-%M-%S') || strptime($dt, '%Y-%m-%d %H:%M:%S')) {
                return TRUE;
            }
        }
    }
    return FALSE;
}

//variables
$showAll = False;

//clean up GET action $_GET['dt']
if (is_datetime(urldecode($_GET['dt']))) {
    $setDateTime = TRUE;
    $lastDateTime = urldecode($_GET['dt']);
}
else {
    $setDateTime = FALSE;
}

//clean up GET action $_GET['limit']
if(isset($_GET['limit'])) {
	if(is_numeric($_GET['limit'])) {
		switch ($_GET['limit']) {
			case '50':
				$limit = 50;
                break;
            case '10':
			default:
				$limit = 10;			
				break;
        }
        $showAll = False;
	}
	else {
        $showAll = True;
	}
}
else {
    $showAll = True;
}

//build query
if ($setDateTime) {
    if ($showAll) {
        $query = sprintf("SELECT * FROM (SELECT * FROM temperature WHERE datetime > '%s') t ORDER BY datetime asc", $lastDateTime);
    }
    else {
        $query = sprintf("SELECT * FROM (SELECT * FROM temperature WHERE datetime > '%s' ORDER BY datetime desc LIMIT %d) t ORDER BY datetime asc", $lastDateTime, $limit);
    }
}
else {
    if ($showAll) {
        $query = "SELECT * FROM temperature";
    }
    else {
        $query = sprintf("SELECT * FROM (SELECT * FROM temperature ORDER BY datetime desc LIMIT %d) t ORDER BY datetime asc", $limit);
    }
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