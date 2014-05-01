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

$tpl = new raintpl(); //include Rain TPL

check_conf(CONF_FILE);
if (file_exists(SERIES_FILE))
{
	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
	$conf = $TSW->getSeries();
	check_result($conf,'Error while reading TV Show schedule');
	
	$found = false;
	foreach($conf['result'] as $serie)
	{
		if ($serie['id'] == $_POST['id'])
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
		$emails = array();
		for ($i=0;$i<count($serie['emails']);$i++)
		{
			$emails[]= array('i'=>$i,'email'=>$serie['emails'][$i],'u_del'=>'index.php?page=del_email&mail_id='.$i.'&id='.$serie['id'].$debug);
		}
	}
	foreach($emails as $key => $email)
	{
		$content[] = array(
						'l_email_num' => 'Email '.($key+1),
						'email_id' => 		'email'.$key,
						'email' =>			$email['email']
							);
	}
}
$tpl->assign( "email", $content);

$tpl->draw( "email_line");

?>
