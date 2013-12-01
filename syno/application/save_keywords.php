<?
if (!TSW)
	die('Not in TSW');

	$page = 'keywords';
	check_conf(CONF_FILE,$page);
	$result = '{"keywords":[';
	$keywords = array();	
	for ($i=0;$_POST['keywords_'.$i]!='';$i++)
		$result .= '"' . str_replace('"','\"',$_POST['keywords_'.$i]) . '",';
	if ($_POST['keywords_new'] != '')
		$result .= '"' . str_replace('"','\"',$_POST['keywords_new']) . '",';

	if ($_POST['keywords_0']!='' or $_POST['keywords_new'] != '')
		$result = substr($result,0,-1);
	$result .= ']}';

	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$TSW->auth();
	$res = $TSW->setConf($result);
	if ($res['rtn']!='200')
		$msg = 'Error while updating keywords<br />'.$res['error'];
	include('keywords.php');
?>
