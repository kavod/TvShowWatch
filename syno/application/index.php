<?
include "inc/rain.tpl.class.php"; //include Rain TPL
include "functions.php";
require_once "api/TvShowWatch.php";
require_once 'api/settings.php';
require_once 'api/TvDb/CurlException.php';
require_once 'api/TvDb/Client.php';
require_once 'api/TvDb/Serie.php';
require_once 'api/TvDb/Banner.php';
require_once 'api/TvDb/Episode.php';

use Moinax\TvDb\Client;

define("CONF_VERSION", '1.8');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("SERIES_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("API_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define('CMD','PATH=/var/packages/python/target/bin:$PATH ; python /var/packages/TvShowWatch/target/tvShowWatch.py -c"' . CONF_FILE . '"');

raintpl::$tpl_dir = "tpl/"; // template directory
raintpl::$cache_dir = "tmp/"; // cache directory

$debug = ($_GET['debug']=='1') ? '&debug=1' : '';
$msg = (isset($_GET['msg'])) ? $_GET['msg'] : '';

switch($_GET['page'])
{
case 'serie_edit':
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
		for ($i=0;$i<count($serie['emails']);$i++)
		{
			$emails[]= array('i'=>$i,'email'=>$serie['emails'][$i],'u_del'=>'index.php?page=del_email&mail_id='.$i.'&id='.$serie['id'].$debug);
		}
	}
	try
	{
		$tvdb = new Client(TVDB_URL, TVDB_API_KEY);
		$serverTime = $tvdb->getServerTime();
		// Search for a show
		$data = $tvdb->getSerie($serie['id']);
		$episodes = $tvdb->getSerieEpisodes($serie['id']);
		$episodes = $episodes['episodes'];
		$episodes = array_filter($episodes,'filter_series');
		if ($episodes != null)
		{
			usort($episodes,'cmp_serie');
			$next_episode = array('season'=>$episodes[0]->season,'episode'=> $episodes[0]->number);
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
				$update = $TSW->setSerie($serie['id'],array('season'=>(int)$_POST['season'],'episode'=>(int)$_POST['episode'],'expected'=>$episode->firstAired->format('Y-m-d')));
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
				'title' => $data->name
			);
	$content[] = array(
				'type' => 'banner',
				'u_banner' => TVDB_URL . '/banners/_cache/' . $data->banner
			);
	$content[] = array(
				'type' => 'longtext',
				'text' => $data->overview
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
	break;

case 'del_serie':
	$page = 'series';
	check_conf(CONF_FILE,$page);
	check_series(SERIES_FILE,$page);
	if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$conf = $TSW->delSerie((int)$_GET['id']);
	if ($conf['rtn']!='200')
			$msg = 'Error during SerieList reading: ' . $conf['error'];
	else
	{
	header("Location:index.php?page=series_list&msg=Deletion%20OK".$debug);
	}
	display_error($page,$msg);
	
case 'del_email':
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
		$nb = (int)$_GET['mail_id'];
		unset($serie['emails'][$i]);
		if (count($serie['emails'])>0)
			$result = $TSW->setSerie($serie['id'],array('emails'=>'["'.implode('","',$serie['emails']).'"]'));
		else
			$result = $TSW->setSerie($serie['id'],array('emails'=>'[]'));
		if ($result['rtn']!='200')
			$msg = 'Error during deletion<br />'.$result['error'];
		else
			$msg = 'Deletion OK';
		header("Location:index.php?page=serie_edit&id=" . $serie['id'] . "&msg=".htmlentities($msg).$debug);
	}
		
	display_error($page,$msg);
break;
	
case 'save_serie':
	$page = 'series';
	check_conf(CONF_FILE,$page);
	if(isset($_FILES['serieFile']))
	{ 
	     if(move_uploaded_file($_FILES['serieFile']['tmp_name'], SERIES_FILE)) //Si la fonction renvoie TRUE, c'est que ça a fonctionné...
	     {
		  $msg =  'Upload of TvShow file completed!';
	     }
	     else //Sinon (la fonction renvoie FALSE).
	     {
		  $msg =  'Failed to upload TvShow file!';
	     }
	}

case 'series_list':
	$page = 'series';
	check_conf(CONF_FILE,$page);
	if (file_exists(SERIES_FILE))
	{
		if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
		$conf = $TSW->getSeries();
		if ($conf['rtn']!='200')
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
	break;

case 'save_keywords':
	$page = 'keywords';
	check_conf(CONF_FILE,$page);
	$result = '{"keywords":[';
	$keywords = array();	
	for ($i=0;$_POST['keywords_'.$i]!='';$i++)
		$result .= '"' . str_replace('"','\"',$_POST['keywords_'.$i]) . '",';
	if ($_POST['keywords_new'] != '')
		$result .= '"' . str_replace('"','\"',$_POST['keywords_new']) . '",';

	if ($_POST['keywords_0']!='' or $_POST['keywords_new'] != '')
		$result = substr($result,0,-1);
	$result .= ']}';

	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$TSW->auth();
	$res = $TSW->setConf($result);
	if ($res['rtn']!='200')
		$msg = 'Error while updating keywords<br />'.$res['error'];

case 'keywords':
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
	break;

case 'save_conf':
	$page = 'config';
	$result = '{"tracker":' . tracker_api_conf($_POST);
	$result .= ',"transmission":' . transmission_api_conf($_POST);
	$result .= ',"smtp":' . email_api_conf($_POST).'}';

	if (!isset($TSW))
		$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
	$TSW->auth();

	if (file_exists(CONF_FILE))
	{
		$conf = $TSW->setConf($result);
		if ($conf['rtn']=='200')
			$msg = 'Configuration file saved';
		else
			$msg = 'Error during configuration save: ' . $conf['error'];
	} else
	{
		$conf = $TSW->createConf($result);
		if ($conf['rtn']=='200')
			$msg = 'Configuration file created';
		else
			$msg = 'Error during configuration creation: ' . $conf['error'];
	}

case 'conf':
	$page = 'config';
	if (file_exists(CONF_FILE))
	{
		if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
		$conf = $TSW->auth();
		$conf = $TSW->getConf();
		if ($conf['rtn']!='200')
			$msg = 'Error during configuration reading: ' . $conf['error'];
		else
			$confVal = $conf['result'];
		
	} else 
	{
		$confVal = Array(
				'tracker' => Array('id'=>'','user'=>''),
				'transmission' => Array('server'=>'','port'=>'','user'=>'','slotNumber' => 6,'folder'=>''),
				'smtp' => Array('server','port','ssltls' => 'False','user','password','emailSender')
					);
	}

	$slot_list = array();
	for ($i=1;$i<13;$i++)
		$slot_list[] = array('value'=> $i,'text'=>$i);

	$content = array();
	$content[] = array(
				'type' => 'h1',
				'title' => 'Configuration parameters'
			);

	$form = array();
	$form = array(
			/* Tracker */
			array(
				'type' => 'h2',
				'title' => 'Tracker'
			),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'tracker_id', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Tracker provider:'),
				'col2'		=> array(
							'type' => 'select', 
							'name' => 'tracker_id', 
							'value' => $confVal['tracker']['id'], 
							'choices' => array(
									array('value' => 't411', 'text' => 'T411')
									)
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'tracker_username', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Tracker username:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'tracker_username', 
							'value' => $confVal['tracker']['user']
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'tracker_password', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Tracker password:'),
				'col2'		=> array(
							'type' => 'input_password', 
							'name' => 'tracker_password', 
							'value' => 'initial'
							)
				),
			/* Transmission */
			array(
				'type' => 'h2',
				'title' => 'Transmission'
			),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_server',
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Transmission server:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'trans_server', 
							'value' => $confVal['transmission']['server']
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_port', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Transmission port:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'trans_port', 
							'value' => $confVal['transmission']['port']
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_username', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Transmission Username:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'trans_username', 
							'value' => $confVal['transmission']['user']
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_password', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Transmission Password:'),
				'col2'		=> array(
							'type' => 'input_password', 
							'name' => 'trans_password', 
							'value' => 'initial'
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_slotNumber', 
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Transmission maximum slots:'),
				'col2'		=> array(
							'type' => 'select', 
							'name' => 'trans_slotNumber', 
							'value' => $confVal['transmission']['slotNumber'], 
							'choices' => $slot_list
							)
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'trans_folder', 
				'col1'		=> array(
							'type' => 'text', 
							'mandatory'	=> false, 
							'label' => 'Local Transfer directory:', 
							'sublabel' => '(keep empty for disable)',
							'subclass' => 'sublabel'
							),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'trans_folder', 
							'value' => $confVal['transmission']['folder']
							)
				),
			/* Email */
			array(
				'type' => 'h2',
				'title' => 'Email notification'
				),
			array(
				'type'		=> 'line',
				'visible'	=> true,
				'id' 		=> 'smtp_enable',  
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Enable:'),
				'col2'		=> array(
							'type' => 'select', 
							'name' => 'smtp_enable', 
							'value' => ($confVal['smtp']['server']=='') ? 0 : 1, 
							'choices' => array(
									array('value' => '0', 'text' => 'No'),
									array('value' => '1', 'text' => 'Yes'),
									),
							'onchange'	=> "(this.value==0)?mode = 'fieldHidden':mode = 'fieldDisplay';visiField(['smtp_server','smtp_port','smtp_ssltls','smtp_emailSender','smtp_username','smtp_password'],mode);"
							)
				
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_server',  
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'SMTP server:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'smtp_server', 
							'value' => $confVal['smtp']['server']
							)
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_port', 
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'SMTP port:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'smtp_port', 
							'value' => $confVal['smtp']['port']
							)
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_ssltls', 
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'SSL/TLS encryption:'),
				'col2'		=> array(
							'type' => 'select', 
							'name' => 'smtp_ssltls', 
							'value' => ($confVal['smtp']['ssltls']=='True') ? 1 : 0,
							'choices' => array(
								array('value' => '0', 'text' => 'No'),
								array('value' => '1', 'text' => 'Yes'),
									)
							)
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_username', 
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Authentification Username:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'smtp_username', 
							'value' => $confVal['smtp']['user']
							)
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_password', 
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Authentification Password:'),
				'col2'		=> array(
							'type' => 'input_password', 
							'name' => 'smtp_password', 
							'value' => 'initial'
							)
				),
			array(
				'type'		=> 'line',
				'id' 		=> 'smtp_emailSender', 
				'visible'	=> ($confVal['smtp']['server']!=''),
				'col1'		=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Sender Email:'),
				'col2'		=> array(
							'type' => 'input_text', 
							'name' => 'smtp_emailSender', 
							'value' => $confVal['smtp']['emailSender']
							)
				)
			);

	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=save_conf'.$debug,
				'class' => 'myForm',
				'submit' => 'Submit',
				'content' => $form
						);

	$content[] = array(
				'type' => 'form',
				'action' => 'index.php?page=import_conf'.$debug,
				'class' => 'myForm',
				'content' => array(
						array(
							'type'	=> 'h1',
							'title' => 'Import configuration file'
							),
						array(
							'type'	=> 'line',
							'visible' => true,
							'col1'	=> array('type' => 'text', 'mandatory'	=> true, 'label' => 'Import file (*.xml):'),
							'col2'	=> array('type' => 'input_file', 'name' => 'configFile'),
							'col3'	=> array('type' => 'input_submit', 'name' => 'submit', 'value' => 'Import')
							)
						)
			);
	
	$tpl = new raintpl(); //include Rain TPL
	//$tpl->assign( "form", array($form,$import));
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'config');
	$tpl->assign( "msg", $msg);
	//$tpl->draw( "general_conf" ); // draw the template
	$tpl->draw( "home" ); // draw the template
	break;
default:
	$page = 'home';
        if (file_exists(CONF_FILE))
        {
                if (!isset($TSW))
                        $TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
                $conf = $TSW->auth();
                $conf = $TSW->getConf();
                if ($conf['rtn']!='200')
		{
                        $conf = '<span class="mandatory">Fail</span>';
			$run = 'Not configured';
                }
		else
		{
			$run = $TSW->testRunning();
                        $conf = '<span class="OK">OK</span>';
			if ($_GET['action'] == 'run')
				$TSW->run();
		}

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
				'col2' => array('type' => 'text','label' => $conf)
			);
	$content[] = array(
				'type' => 'line',
				'visible' => true,
				'col1' => array('type' => 'text','label' => 'Run status:'),
				'col2' => array('type' => 'text','label' => $run)
			);
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
	
}

?>
