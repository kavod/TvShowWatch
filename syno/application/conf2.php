<?
if (!TSW)
	die('Not in TSW');

	if (file_exists(CONF_FILE))
	{
		if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
		$conf = $TSW->auth();
		$conf = $TSW->getConf();
		if ($conf['rtn']!='200')
		{
			$msg = 'Error during configuration reading: ' . $conf['error'];
			$javascript .= "var conf_status = false;";
		}
		else
		{
			$javascript .= "var conf_status = true;";
			if (isset($conf['result']['keywords']))
			{
				foreach($conf['result']['keywords'] as $key => $keyword)
					$keywords[] = array('key' => $key, 'value' => $keyword);
			}
			else
				$keywords = array();
		}
	} else 
	{
		$javascript .= "var conf_status = false;";
	}

$tracker_id = array(
					array('value' => 't411', 'text' => 'T411')
					);

$tpl->assign( "l_conf_title", 'Configuration parameters');
$tpl->assign( "l_conf_tracker", 'Tracker');
$tpl->assign( "l_conf_tracker_provider", 'Tracker Povider:');
$tpl->assign( "l_conf_tracker_username", 'Tracker username:');
$tpl->assign( "l_conf_tracker_password", 'Tracker password:');
$tpl->assign( "l_conf_transmission", 'Transmission');
$tpl->assign( "l_conf_transmission_server", 'Transmission server:');
$tpl->assign( "l_conf_transmission_port", 'Transmission port:');
$tpl->assign( "l_conf_transmission_username", 'Transmission username:');
$tpl->assign( "l_conf_transmission_password", 'Transmission password:');
$tpl->assign( "l_conf_transmission_slot", 'Transmission maximum slots:');
$tpl->assign( "l_conf_transmission_folder", 'Local Transfer directory:');
$tpl->assign( "l_conf_email", 'Email notifications');
$tpl->assign( "l_conf_enable", 'Enable:');
$tpl->assign( "l_conf_email_server", 'SMTP server:');
$tpl->assign( "l_conf_email_port", 'SMTP port:');
$tpl->assign( "l_conf_email_ssltls", 'SSL/TLS encryption:');
$tpl->assign( "l_conf_email_username", 'Authentification username:');
$tpl->assign( "l_conf_email_password", 'Authentification password:');
$tpl->assign( "l_conf_email_sender", 'Sender email:');
$tpl->assign( "l_conf_import", 'Import configuration file');
$tpl->assign( "l_conf_import_file", 'Import file (*.xml):');

$tpl->assign( "l_keywords_title", 'Keywords configuration Management');

$tpl->assign( "l_yes", 'Yes');
$tpl->assign( "l_no", 'No');
$tpl->assign( "l_submit", 'Submit');
$tpl->assign( "l_send", 'Send');

$tpl->assign( "l_conf_username_here", 'Username here');
$tpl->assign( "l_conf_password_here", 'Password here');
$tpl->assign( "l_conf_server_here", 'Server address here');
$tpl->assign( "l_conf_port_here", 'Server port here');
$tpl->assign( "l_conf_slot_here", 'Maximum slot number');
$tpl->assign( "l_conf_keep_blank", 'Keep blank for disable');
$tpl->assign( "l_conf_keep_blank_noauth", 'Keep blank if no authentification');
$tpl->assign( "l_conf_keep_test_email", 'Email will be sent to it for test');

if (isset($keywords))
	$tpl->assign( "keywords", $keywords);

$tpl->assign( "conf_tracker_id", $tracker_id);

?>
