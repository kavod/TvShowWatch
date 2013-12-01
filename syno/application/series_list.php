<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	if (file_exists(SERIES_FILE))
	{
		if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
		$conf = $TSW->getSeries();
		if ($conf['rtn']=='300')
		{
			$series = array();
			$msg = 'No TV Show scheduled';
		}
		elseif ($conf['rtn']!='200')
			$msg = 'Error during SerieList reading: ' . $conf['error'];
		else
		{
			if (isset($conf['result']))
				$series = $conf['result'];
			else
				$series = array();
		}
	} else
	{
		$series = array();
		$msg = 'No TV Show scheduled';
	}
	$serielist = array();
	foreach ($series as $serie)
	{
		array_push($serielist,array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => $serie['name'],'href'=> 'index.php?page=serie_edit&id='.$serie['id'].$debug),
						'col2' => array('type' => 'text','label' => serieStatus($serie['status'])),
						'col3' => array('type' => 'text','label' => $serie['expected'])
							));
	}
	usort($serielist, "cmp");


	$content = array();
	$content[] = array(
				'type' => 'h1',
				'title' => 'TV Shows list'
			);
	$content = array_merge($content,$serielist);
	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=save_serie'.$debug,
				'enctype' => 'file',
				'class' => 'myForm',
				'onsubmit' => 'return validateForm(this)',
				'content' => array(
							array('type' => 'h2', 'title' => 'TV Shows list file importation'),
							array(
								'type' => 'line',
								'visible' => true,
								'col1' => array('type' => 'text', 'label' => 'Import file (*.xml):'),
								'col2' => array('type' => 'input_file', 'name' => 'serieFile'),
								'col3' => array('type' => 'submit', 'label' => 'Import')
								)
						)

			);


	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'series');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "home" ); // draw the template
?>
