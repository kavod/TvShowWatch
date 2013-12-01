<?
if (!TSW)
	die('Not in TSW');

	$page = 'home';
	$print_conf = array(
			'0' => '<span class="mandatory">Fail</span>',
			'1' => '<span class="OK">OK</span>'
			);
        if (file_exists(CONF_FILE))
        {
                if (!isset($TSW))
                        $TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
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
                        $conf = '1'; //'<span class="OK">OK</span>';
			if ($_GET['action'] == 'run')
				$TSW->run();
		}

        }
	else
	{
		$conf = '0';//'<span class="mandatory">Fail</span>';
		$run = 'Not configured';
	}
	$content = array();
	$content[] = array(
				'type' => 'h1',
				'title' => 'Welcome on TvShowWatch'
			);
	$content[] = array(
				'type' => 'line',
				'visible' => true,
				'col1' => array('type' => 'text','label' => 'Configuration status:'),
				'col2' => array('type' => 'text','label' => $print_conf[$conf])
			);
	$content[] = array(
				'type' => 'line',
				'visible' => true,
				'col1' => array('type' => 'text','label' => 'Run status:'),
				'col2' => array('type' => 'text','label' => $run)
			);
	if ($conf == '1')
		$content[] = array(
				'type' => 'line',
				'visible' => true,
				'col1' => array('type' => 'text','label' => 'Run now:'),
				'col2' => array('type' => 'input_button','value' => 'Run', 'name'=> 'run', 'onclick'=> "window.location.href='index.php?action=run".$debug."'")
			);
	$content[] = array(
				'type' => 'h2',
				'title' => 'Last logs'
			);
	$content[] = array(
				'type' => 'iframe',
				'class' => 'log',
				'src' => 'log.php'
			);

	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'home');
	$tpl->assign( "msg", $msg);
        $tpl->draw( "home" ); // draw the template
?>
