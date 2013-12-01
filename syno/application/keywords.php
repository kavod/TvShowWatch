<?
if (!TSW)
	die('Not in TSW');

	$page = 'keywords';
	check_conf(CONF_FILE,$page);
	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$conf = $TSW->auth();
	$conf = $TSW->getConf();
	check_result($conf,'Error while reading configuration',$page);
	
	if (isset($conf['result']['keywords']))
		$keywords = $conf['result']['keywords'];
	else
		$keywords = array();

	$keywords_form = array();

	for ($i=0;$i<count($keywords);$i++)
	{
		$keywords_form[] = array(
								'type' 		=> 'line',
								'visible'	=> true,
								'col1' => array('type' => 'text', 'label' => 'Keywords '.($i+1)),
								'col2' => array('type' => 'input_text', 'name' => 'keywords_'.$i, 'value' => $keywords[$i])
								);
	}
	$keywords_form[] = array(
							'type' 		=> 'line',
							'visible'	=> true,
							'col1' => array('type' => 'text', 'label' => 'New keywords'),
							'col2' => array('type' => 'input_text', 'name' => 'keywords_new', 'value' => '')
							);
	$content = array();
	$content[] = array('type' => 'h1', 'title' => 'Keywords configuration Management');
	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=save_keywords'.$debug,
				'class' => 'myForm',
				'submit' => 'Submit',
				'content' => $keywords_form
						);
		
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'keywords');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "home" ); // draw the template
?>
