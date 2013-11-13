<?php
 echo system("/usr/syno/synoman/webman/authenticate.cgi");

define('VERSION','1.7');

function tracker_conf($tracker_id,$username,$password,$keywords)
{
	$config_out = "<tracker><id>";
	$config_out .= $tracker_id;
	$config_out .= "</id><user>";
	$config_out .= $username;
	$config_out .= "</user><password>";
	$config_out .= $password;
	$config_out .= "</password>";
	if ($keywords != "")
	{
		$config_out .= "<keywords>";
		$config_out .= $keywords;
		$config_out .= "</keywords>";
	}
	$config_out .= "</tracker>";
	return $config_out;
}

function transmission_conf($server,$port,$username,$password,$slotNumber,$folder)
{
	$config_out = "<transmission><server>";
	$config_out .= $server;
	$config_out .= "</server><port>";
	$config_out .= $port;
	$config_out .= "</port><user>";
	$config_out .= $username;
	$config_out .= "</user><password>";
	$config_out .= $password;
	$config_out .= "</password><slotNumber>";
	$config_out .= $slotNumber;
	$config_out .= "</slotNumber>";
	if ($folder != "")
	{
		$config_out .= "<folder>";
		$config_out .= $folder;
		$config_out .= "</folder>";
	}
	$config_out .= "</transmission>";
	return $config_out;
}

function email_conf($server,$port,$ssltls,$username,$password,$emailSender)
{
	$config_out = "<smtp><server>";
	$config_out .= $server;
	$config_out .= "</server><port>";
	$config_out .= $port;
	$config_out .= "</port><ssltls>";
	$config_out .= ($ssltls==1) ? 'True' : 'False';
	$config_out .= "</ssltls>";
	if ($username != "")
	{
		$config_out .= "<user>";
		$config_out .= $username;
		$config_out .= "</user><password>";
		$config_out .= $password;
		$config_out .= "</password>";
	}
	$config_out .= "<emailSender>";
	$config_out .= $emailSender;
	$config_out .= "</emailSender>";
	$config_out .= "</smtp>";
	return $config_out;
}

$format = "<conf><version>%s</version>%s%s%s</conf>";
$traker_conf = tracker_conf($_POST['tracker_id'],$_POST['tracker_username'],$_POST['tracker_password'],$_POST['tracker_keywords']);
$transmission_conf = transmission_conf($_POST['trans_server'],$_POST['trans_port'],$_POST['trans_username'],$_POST['trans_password'],$_POST['trans_slotNumber'],$_POST['trans_folder']);
$email_conf = email_conf($_POST['smtp_server'],$_POST['smtp_port'],$_POST['smtp_ssltls'],$_POST['smtp_username'],$_POST['smtp_password'],$_POST['smtp_emailSender']);
$config_out = sprintf($format, VERSION,$traker_conf, $transmission_conf, $email_conf);

$fp = fopen('/var/packages/TvShowWatch/etc/config.xml', 'w');
fwrite($fp, $config_out);
fclose($fp);

if(isset($_FILES['config']))
{ 
	
     $dossier = '/var/packages/TvShowWatch/etc/';
     $fichier = basename($_FILES['config']['name']);

     if(move_uploaded_file($_FILES['config']['tmp_name'], $dossier . $fichier)) //Si la fonction renvoie TRUE, c'est que ça a fonctionné...
     {
          echo 'Upload of TvShow file completed!';
     }
     else //Sinon (la fonction renvoie FALSE).
     {
          echo 'Failed to upload TvShow file!';
     }
}
?>
