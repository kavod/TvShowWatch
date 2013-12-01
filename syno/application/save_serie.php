<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	if(isset($_FILES['serieFile']))
	{ 
	     if(move_uploaded_file($_FILES['serieFile']['tmp_name'], SERIES_FILE)) //Si la fonction renvoie TRUE, c'est que ça a fonctionné...
	     {
		  $msg =  'Upload of TvShow file completed!';
	     }
	     else //Sinon (la fonction renvoie FALSE).
	     {
		  $msg =  'Failed to upload TvShow file!';
	     }
	}
	include('series_list.php');
?>
