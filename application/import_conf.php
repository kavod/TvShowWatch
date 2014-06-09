<?
if (!TSW)
	die('Not in TSW');

	$page = 'config';
	if(isset($_FILES['configFile']))
	{ 
	     if(move_uploaded_file($_FILES['configFile']['tmp_name'], CONF_FILE))
	     {
		  $msg =  'Upload of configuration file completed!';
	     }
	     else //Sinon (la fonction renvoie FALSE).
	     {
		  $msg =  'Failed to upload configuration file!';
	     }
	} 
	else
		$msg =  'Failed to upload configuration file!';
	include('conf.php');
?>
