<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	check_series(SERIES_FILE,$page);
	if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$serie_id = (int)$_POST['serie_id'];
	$result = $TSW->addSerie($serie_id);
	if ($result['rtn']!='200')
		$msg = 'Error while adding TV Show<br />'.$result['error'];
	else
		$msg = 'TV Show '.$serie_id.' added';
	$_GET['id'] = $serie_id;
	include('serie_edit.php');
?>
