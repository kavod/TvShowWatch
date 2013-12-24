<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	check_series(SERIES_FILE,$page);
	if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$conf = $TSW->getSeries();
	check_result($conf,'Error while reading TV Show schedule',$page);
	
	$found = false;
	foreach($conf['result'] as $serie)
	{
		if ($serie['id'] == $_GET['id'])
		{
			$found = true;
			break;
		}
	}
	if (!$found)
	{
		$msg = 'TV Show not scheduled';
		display_error($page,$msg);
		break;
	} else
	{
		$serie['emails'][] = $_POST['addmail'];
		if (count($serie['emails'])>0)
			$result = $TSW->setSerie($serie['id'],array('emails'=>$serie['emails']));
		else
			$result = $TSW->setSerie($serie['id'],array('emails'=>array()));
		if ($result['rtn']!='200')
			$msg = 'Error during email insertion<br />'.$result['error'];
		else
			$msg = 'Email add OK';
		include('serie_edit.php');
		/*if ($_GET['debug'] != '1')
			header("Location:index.php?page=serie_edit&id=" . $serie['id'] . "&msg=".htmlentities($msg).$debug);*/
	}
?>
