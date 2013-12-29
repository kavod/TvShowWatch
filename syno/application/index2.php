<?
error_reporting(E_ALL | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

if (!isset($path))
	$path = './';

require_once("inc/constants.php");
include "inc/rain.tpl.class.php"; //include Rain TPL
require_once($path . "functions.php");
require_once "api/TvShowWatch.php";
require_once("api/tvdb.php");

raintpl::$tpl_dir = "tpl/"; // template directory
raintpl::$cache_dir = "tmp/"; // cache directory

$debug = ($_GET['debug']=='1') ? '&debug=1' : '';
$msg = (isset($_GET['msg'])) ? $_GET['msg'] : '';

$javascript = "";

$tpl = new raintpl(); //include Rain TPL
include "default2.php";
include "conf2.php";
include "series_list2.php";
$tpl->assign( "msg", $msg);
$tpl->assign( "javascript", $javascript);
$tpl->draw( "index" ); // draw the template

?>
