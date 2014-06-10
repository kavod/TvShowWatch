<?
$file = $path.'../directory.json';
$directories = json_decode(file_get_contents($file), true);

define('TSW',true);
define("ARCH", $directories['arch']);
define("CONF_VERSION", '1.8');
define("CONF_FILE", $directories['configpath'].'/config.xml');
define("SERIES_FILE", $directories['seriepath'].'/series.xml');
define("API_FILE", $directories['scriptpath'].'/TSW_api.py');
define("RUN_FILE", $directories['scriptpath'].'/tvShowWatch.py');
define("TMP_DIR", 'tmp');
define("PYTHON_EXEC", $directories['python_exec']);
define('CMD',PYTHON_EXEC . ' ' . RUN_FILE . ' -c"' . CONF_FILE . '"');

?>
