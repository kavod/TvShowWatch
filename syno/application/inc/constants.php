<?
define('TSW',true);
define("CONF_VERSION", '1.8');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("SERIES_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("API_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define("RUN_FILE", '/var/packages/TvShowWatch/target/tvShowWatch.py');
define("TMP_DIR", 'tmp');
define("PYTHON_EXEC", 'PATH=/var/packages/python/target/bin:$PATH ; python ');
define('CMD',PYTHON_EXEC . RUN_FILE . ' -c"' . CONF_FILE . '"');
define("LOGFILE", '/var/log/TSW.log');

?>
