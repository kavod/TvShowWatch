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
	{
		$msg = 'Error during SerieList reading: ' . $conf['error'];
		display_error($page,$msg);
	}
	else
	{
		$msg = 'Deletion OK';
	}
	include('series_list.php');
?>
