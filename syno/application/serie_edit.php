<?
if (!TSW)
	die('Not in TSW');

	$page = 'series';
	check_conf(CONF_FILE,$page);
	check_series(SERIES_FILE,$page);
	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$conf = $TSW->getSeries();
	check_result($conf,'Error while reading TV Show schedule',$page);
	
	$found = false;
	foreach($conf['result'] as $serie)
	{
		if ($serie['id'] == $_GET['id'])
		{
			$found = true;
			break;
		}
	}
	if (!$found)
	{
		$msg = 'TV Show not scheduled';
		display_error($page,$msg);
		break;
	} else
	{
		$emails = array();
		for ($i=0;$i<count($serie['emails']);$i++)
		{
			$emails[]= array('i'=>$i,'email'=>$serie['emails'][$i],'u_del'=>'index.php?page=del_email&mail_id='.$i.'&id='.$serie['id'].$debug);
		}
	}
	try
	{
		$tvdb = new TvDB(($debug != ''));
		$data = $tvdb->getSerie($serie['id']);
		$episodes = $tvdb->getEpisodes($serie['id']);
		$episodes = $episodes['episodes'];
		$episodes = array_filter($episodes,'filter_series');
		if ($episodes != null)
		{
			usort($episodes,'cmp_serie');
			$next_episode = array('season'=>$episodes[0]['seasonnumber'],'episode'=> $episodes[0]['episodenumber']);
		} else
			$next_episode = array('season'=>'','episode'=> '');
	}
	catch (Exception $e) {
		$msg = 'TV Show unfounable';
		display_error($page,$msg);
		break;
	}
	if (isset($_POST['season']) or isset($_POST['episode']))
	{
		if ((int)$_POST['season'] * (int)$_POST['episode'] != 0)
		{
			try
			{
				$episode = $tvdb->getEpisode($serie['id'], (int)$_POST['season'], (int)$_POST['episode'], 'en');
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
				$update = $TSW->setSerie($serie['id'],array('season'=>(int)$_POST['season'],'episode'=>(int)$_POST['episode'],'expected'=>$episode['firstaired']));
				if ($update['rtn'] != '200')
					$msg = 'Error during TV Show update<br />'.$update['error'];
				else
				{
					$conf = $TSW->getSeries();
					$found = false;
					foreach($conf['result'] as $serie)
					{
						if ($serie['id'] == $_GET['id'])
						{
							$found = true;
							break;
						}
					}
					$msg = 'TV Show updated';
				}
			}
			catch (Exception $e)
			{
				$msg = 'Episode S' . sprintf("%02s", $_POST['season']) . 'E'. sprintf("%02s", $_POST['episode']) . ' does not exist';
			}

		} else
		{
			$msg='You must indicate both of Season and Episode numbers';
		}
	}
	$content = array();
	$content[] = array(
				'type' => 'h1',
				'title' => $data['seriesname']
			);
	$content[] = array(
				'type' => 'banner',
				'u_banner' => str_replace("banners/graphical","banners/_cache/graphical",$data['banner'])
			);
	$content[] = array(
				'type' => 'longtext',
				'text' => $data['overview']
			);
	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=serie_edit&id='.$serie['id'].$debug,
				'class' => 'myForm',
				'content' => array(
								array(
								'type' => 'line',
								'visible' => true,
								'col1' => array(
									'type' => 	'text',
									'label' => 	'Next scheduled episode:',
									'sublabel'=>'Retrieve next broadcast',
									'subonclick'=>"return set_last(document.getElementById('season'),document.getElementById('episode'),'".$next_episode['season']."','".$next_episode['episode']."')",
									'subhref'=>	"http://github.com/kavod/TvShowWatch",
									'subclass'=>"sublabel"
												),
								'col2' => array(
									'type' => 'episodechoice',
									's_name' => 'season', 
									's_id'=>'season', 
									'season'=>sprintf("%02s", $serie['season']),
									'e_name' => 'episode', 
									'e_id'=>'episode', 
									'episode'=>sprintf("%02s", $serie['episode']),
												),
								'col3' => array('type' => 'submit', 'label' => 'Change')
									)
								)
					);
	$content[] = array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => 'Expected on:'),
						'col2' => array('type' => 'text','label' => $serie['expected'])
							);
	$content[] = array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => 'Status:'),
						'col2' => array('type' => 'text','label' => serieStatus($serie['status']))
							);
	foreach($emails as $email)
	{
		$content[] = array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => 'Email '.($email['i']+1)),
						'col2' => array('type' => 'text','label' => $email['email']),
						'col3' => array('type' => 'input_button', 'name' => 'mail'.$email['i'],'value'=>'Delete','onclick'=>"location.href='".$email['u_del']."'")
							);
	}
	
	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=email_add&id='.$serie['id'].$debug,
				'class' => 'myForm',
				'content' => array(
								array(
									'type' => 'line',
									'visible' => true,
									'col1' => array('type' => 'text', 'label' => 'Add an email:'),
									'col2' => array('type' => 'input_text', 'name' => 'addmail'),
									'col3' => array('type' => 'submit', 'label' => 'Add email')
									)
								)
			);
	$content[] = array(
						'type' => 'line',
						'visible' => true,
						'col1' => array('type' => 'text','label' => 'Unschedule TV Show download:'),
						'col2' => array('type' => 'input_button','name' => 'del', 'value'=>'Unschedule!', 'onclick'=>"location.href='".'index.php?page=del_serie&id='.$serie['id'].$debug."'")
							);
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'series');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "home" ); // draw the template

?>
