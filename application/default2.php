<?
if (!TSW)
	die('Not in TSW');

	$debug = (isset($_GET['debug'])) ? $_GET['debug'] : '';
	$print_conf = array(
			'0' => '<span class="mandatory">Fail</span>',
			'1' => '<span class="OK">OK</span>'
			);
if (file_exists(CONF_FILE))
{
    if (!isset($TSW))
            $TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
    $conf = $TSW->auth();
    $conf = $TSW->getConf();
    if ($conf['rtn']!='200')
	{
		$conf = '0';//'<span class="mandatory">Fail</span>';
		$run = 'Not configured';
    }
	else
	{
		$run = $TSW->testRunning();
		$conf = '1';
	}
}
else
{
	$conf = '0';//'<span class="mandatory">Fail</span>';
	$run = 'Not configured';
}

$tpl->assign( "l_home_welcome", 'Welcome on TvShowWatch');
$tpl->assign( "l_home_conf_status", 'Configuration status:');
$tpl->assign( "l_home_run_status", 'Run status:');
$tpl->assign( "l_home_run_now", 'Run now:');
$tpl->assign( "l_home_run", 'run');

$tpl->assign( "home_conf_status", $print_conf[$conf]);
$tpl->assign( "home_run_status", $run);

?>
