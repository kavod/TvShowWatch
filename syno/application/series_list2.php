<?
/*if (!TSW)
	die('Not in TSW');*/
error_reporting(E_ALL | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

if (!isset($path))
	$path = './';

require_once("inc/constants.php");
include "inc/rain.tpl.class.php"; //include Rain TPL
require_once($path . "functions.php");
require_once "api/TvShowWatch.php";

raintpl::$tpl_dir = "tpl/"; // template directory
raintpl::$cache_dir = "tmp/"; // cache directory

$debug = (isset($_GET['debug'])) ? $_GET['debug'] : '';
$noTvShow = '';

$tpl = new raintpl(); //include Rain TPL

check_conf(CONF_FILE);
if (file_exists(SERIES_FILE))
{
	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
	$conf = $TSW->getSeries();
	if ($conf['rtn']=='300')
	{
		$series = array();
		$noTvShow = 'No TV Show scheduled';
	}
	else
	{
		if (isset($conf['result']))
			$series = $conf['result'];
		else
			$series = array();
	}
} else
{
	$series = array();
	$noTvShow = 'No TV Show scheduled';
}
$serielist = array();
foreach ($series as $serie)
{
	$serielist[] = array(
						'series_id' => $serie['id'],
						'series_name' => $serie['name'],
						'series_episode' => sprintf("S%1$02dE%2$02d",$serie['season'],$serie['episode']),
						'series_status' => serieStatus($serie['status']),
						'series_expected' => $serie['expected']
						);
}
usort($serielist, "cmp_serie_az");
$tpl->assign( "noTvShow", $noTvShow);
$tpl->assign( "series", $serielist);

$tpl->draw( "serie_line");

?>
