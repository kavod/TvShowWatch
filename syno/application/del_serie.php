<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	check_series(SERIES_FILE,$page);
	if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$conf = $TSW->delSerie((int)$_GET['id']);
	if ($conf['rtn']!='200')
			$msg = 'Error during SerieList reading: ' . $conf['error'];
	else
	{
		$msg = 'Deletion OK';
		include('series_list.php');	
	//header("Location:index.php?page=series_list&msg=Deletion%20OK".$debug);
	}
	display_error($page,$msg);
?>
