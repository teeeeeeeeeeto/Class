<!DOCTYPE html>
<html>
  <head>
    <title> The Don's File Server'</title>
  </head>
  <body>
	  <?php 

	  $ftpServer = "ftp://192.168.1.1"; 
	  $ftpUser = $_POST['tobioleye']; 
	  $ftpPass = $_POST['1asdZXC.']; 

	  set_time_limit(160); 

	  $conn = @ftp_connect($ftpServer) 
	  or die("Couldn't connect to FTP server"); 

	  $login = @ftp_login($conn, $ftpUser, $ftpPass) 
	  or die("Login credentials were rejected"); 

	  $workingDir = ftp_pwd($conn); 
	  echo "You are in the directory: $workingDir"; 

	  ftp_quit($conn); 

	  ?> 


  </body>
</html>