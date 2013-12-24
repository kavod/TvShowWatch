<?
error_reporting(E_ERROR | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

include "inc/rain.tpl.class.php"; //include Rain TPL
include "functions.php";
require_once "api/TvShowWatch.php";
require_once("api/tvdb.php");

define('TSW',true);
define("CONF_VERSION", '1.8');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("SERIES_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("API_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define('CMD','PATH=/var/packages/python/target/bin:$PATH ; python /var/packages/TvShowWatch/target/tvShowWatch.py -c"' . CONF_FILE . '"');

raintpl::$tpl_dir = "tpl/"; // template directory
raintpl::$cache_dir = "tmp/"; // cache directory

$debug = ($_GET['debug']=='1') ? '&debug=1' : '';
$msg = (isset($_GET['msg'])) ? $_GET['msg'] : '';

switch($_GET['page'])
{
case 'serie_edit':
	include('serie_edit.php');
	break;

case 'add_serie':
	include('add_serie.php');
	break;

case 'del_serie':
	include('del_serie.php');
	break;
	
case 'del_email':
	include('del_email.php');
	break;
	
case 'email_add':
	include('email_add.php');
	break;

case 'save_serie':
	include('save_serie.php');
	break;

case 'series_list':
	include('series_list.php');
	break;

case 'save_keywords':
	include('save_keywords.php');
	break;

case 'keywords':
	include('keywords.php');
	break;

case 'import_conf':
	include('import_conf.php');
	break;

case 'save_conf':
	include('save_conf.php');
	break;

case 'conf':
	include('conf.php');
	break;
default:
	include('default.php');	
}

?>
