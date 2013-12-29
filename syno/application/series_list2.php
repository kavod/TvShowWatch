<?
if (!TSW)
	die('Not in TSW');

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
			$javascript .= "show_error('Error during SerieList reading: " . str_replace("'","\'",$conf['error'])."');";
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
		$serielist[] = array(
							'series_id' => $serie['id'],
							'series_name' => $serie['name'],
							'series_episode' => sprintf("S%1$02dE%1$02d",$serie['season'],$serie['episode']),
							'series_status' => serieStatus($serie['status']),
							'series_expected' => $serie['expected']
							);
		/*array_push($serielist,array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => $serie['name'],'href'=> 'index.php?page=serie_edit&id='.$serie['id'].$debug),
						'col2' => array('type' => 'text','label' => serieStatus($serie['status'])),
						'col3' => array('type' => 'text','label' => $serie['expected'])
							));*/
	}
	usort($serielist, "cmp_serie_az");
	$tpl->assign( "series", $serielist);
/*
	$content = array();
	$content[] = array(
				'type' => 'h1',
				'title' => 'TV Shows list'
			);
	$content = array_merge($content,$serielist);

	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=add_serie'.$debug,
				'class' => 'myForm',
				'onsubmit' => 'return validateForm(this)',
				'content' => array(
							array('type' => 'h2', 'title' => 'Add TV Show'),
							array(
								'type' => 'line',
								'visible' => true,
								'col1' => array('type' => 'text', 'label' => 'TvDB show ID'),
								'col2' => array('type' => 'input_text', 'name' => 'serie_id'),
								'col3' => array('type' => 'submit', 'label' => 'Add')
								)
						)

			);
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
	$tpl->draw( "home" ); // draw the template*/
?>
