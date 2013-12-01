<?
if (!TSW)
	die('Not in TSW');

	$page = 'config';
	$result = '{"tracker":' . tracker_api_conf($_POST);
	$result .= ',"transmission":' . transmission_api_conf($_POST);
	$result .= ',"smtp":' . email_api_conf($_POST).'}';

	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$TSW->auth();

	if (file_exists(CONF_FILE))
	{
		$conf = $TSW->setConf($result);
		if ($conf['rtn']=='200')
			$msg = 'Configuration file saved';
		else
			$msg = 'Error during configuration save: ' . $conf['error'];
	} else
	{
		$conf = $TSW->createConf($result);
		if ($conf['rtn']=='200')
			$msg = 'Configuration file created';
		else
			$msg = 'Error during configuration creation: ' . $conf['error'];
	}
include('conf.php');
?>
