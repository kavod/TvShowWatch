<?
error_reporting(E_ALL | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

include "functions.php";
require_once "api/TvShowWatch.php";

define("CONF_VERSION", '1.8');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("SERIES_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("API_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define('CMD','PATH=/var/packages/python/target/bin:$PATH ; python /var/packages/TvShowWatch/target/tvShowWatch.py -c"' . CONF_FILE . '"');

$debug = ($_GET['debug']=='1') ? '&debug=1' : '';
$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
$conf = $TSW->auth();
$TSW->run();

die($msg);
?>
