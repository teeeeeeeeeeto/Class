<?php
//require_once 'login2.php';
//$db_server = mysql_connect($db_hostname, $db_username, $db_password);
//
//if(!$db_server){
//	mysql_fatal_error(mysql_error());
//}
//$db_server = mysql_connect($db_hostname, $db_username, $db_password);
//if (!$db_server) die("Unable to connect to MySQL: " . mysql_error());
//mysql_select_db($db_database, $db_server)
//or die("Unable to select database: " . mysql_error());

#$result = shell_exec('python /Users/tobioleye/Desktop/test6.py ');
$result = file_get_contents('info.txt');
$resultData = json_decode($result, true);
for ($x=0; $x<count($resultData); $x++)
  {
        $courseNumber = $resultData[$x][coursenum];
        $course = $resultData[$x][Program];
        $type = $resultData[$x][type];
        $startTime = $resultData[$x][start];
        $endTime = $resultData[$x][end];
        $building = $resultData[$x][building];
        $location = $resultData[$x][classNum];
        $date = $resultData[$x][date];
        $lastName = $resultData[$x][firstName];
        $firstName = $resultData[$x][lastName];
        $days = $resultData[$x][days];
        if(strpos($firstName,'\''))
        {
            str_replace('\'', '', $lastName);
        } 
        

        if($date == "NULL")
        {
           $date = "2014-02-25";
        }
        
         if (strpos($days,'1') !== false) 
         {
            echo "Monday";
          }
         if (strpos($days,'2') !== false) 
         {
            echo "Tuesday";
          }
          if (strpos($days,'3') !== false) 
         {
            echo "Wednesday";
          }
          if (strpos($days,'4') !== false) 
         {
            echo "Thursday";
          }
         if (strpos($days,'5') !== false) 
         {
            echo "Friday";
         }
    }
?>