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

switch($_GET['page'])
{
case 'serie_edit':
	try
	{
		$tvdb = new Client(TVDB_URL, TVDB_API_KEY);

		$serverTime = $tvdb->getServerTime();
		// Search for a show
		$data = $tvdb->getSerie($_GET['id']);

		$tpl = new raintpl(); //include Rain TPL
	
		$tpl->assign( "banner", TVDB_URL . '/banners/_cache/' . $data->banner);
		$tpl->assign( "seriename", $data->name);
		$tpl->assign( "description", $data->overview);
		$tpl->assign( "page", 'series');
		$tpl->assign( "msg", $msg);
		$tpl->draw( "serie" ); // draw the template
		break;
	}
	catch (Exception $e) {
		$tpl = new raintpl(); //include Rain TPL
		$msg = 'TV Show unfounable';
		$tpl->assign( "msg", $msg);
		$tpl->assign( "page", 'series');
		break;
	}

case 'save_serie':
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

	if (file_exists(CONF_FILE))
	{
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
	} else 
	{
		$tpl = new raintpl(); //include Rain TPL
		$msg = 'Initial configuration must be done before';
		$tpl->assign( "msg", $msg);
		$tpl->assign( "page", 'keywords');
		break;
	}

	$form = array(
		'title' 	=> 'TV Shows list',
		'action'	=> 'index.php?page=save_series'.$debug,
		'part' 		=> array()
		);

	$serielist = array();
	foreach ($series as $serie)
	{
		array_push($serielist,array(
						'id'		=> $serie['id'],
						'seriename'	=> $serie['name']
					));
		$serie = array(
			'title' => $serie['name'],
			'champs' => array(
					array(
						'field_id'	=> 'serie_id'.$i,
						'type'		=> 'text',
						'label'		=> 'ID',
						'value'		=> $serie['id'],
						'mandatory'	=> true,
						'visible'	=> false,
					),
					array(
						'field_id'	=> 'season'.$i,
						'type'		=> 'text',
						'label'		=> 'Season',
						'value'		=> $serie['season'],
						'mandatory'	=> true
					),
					array(
						'field_id'	=> 'episode'.$i,
						'type'		=> 'text',
						'label'		=> 'Episode',
						'value'		=> $serie['episode'],
						'mandatory'	=> true
					),
					array(
						'field_id'	=> 'expected'.$i,
						'type'		=> 'text',
						'label'		=> 'Expected on ',
						'value'		=> $serie['expected'],
						'mandatory'	=> true
					),
				)
			);
		array_push($form['part'],$serie);
	}

	$serieFile = array(
		'title' => 'Import Series file',
		'champs' => array(
				array(
					'field_id'	=> 'serieFile',
					'type'		=> 'file',
					'label'		=> 'Import file (*.xml)'
					)
				)
		);
	$form_import = array(
		'title' 	=> 'Importation',
		'action'	=> 'index.php?page=save_serie'.$debug,
		'part' 		=> array($serieFile)
		);

	$tpl = new raintpl(); //include Rain TPL

	$tpl->assign( "serieList", array('title'=>'TV Shows list','list'=>$serielist));
	$tpl->assign( "form", array($form,$form_import));
	$tpl->assign( "page", 'series');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "general_conf" ); // draw the template
	break;

case 'save_keywords':
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

	if (file_exists(CONF_FILE))
	{
		$conf = $TSW->setConf($result);
		if ($conf['rtn']=='200')
			$msg = 'Keywords saved';
		else
			$msg = 'Error during keywords save: ' . $conf['error'];
	} else
	{
		$tpl = new raintpl(); //include Rain TPL
		$msg = 'Initial configuration must be done before';
		$tpl->assign( "msg", $msg);
		$tpl->assign( "page", 'keywords');
		break;
	}

case 'keywords':

	if (file_exists(CONF_FILE))
	{
		if (!isset($TSW))
			$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$_GET['debug']);
		$conf = $TSW->auth();
		$conf = $TSW->getConf();
		if ($conf['rtn']!='200')
			$msg = 'Error during configuration reading: ' . $conf['error'];
		else
		{
			if (isset($conf['result']) && isset($conf['result']['keywords']))
				$keywords = $conf['result']['keywords'];
			else
				$keywords = array();
		}
	} else 
	{
		$tpl = new raintpl(); //include Rain TPL
		$msg = 'Initial configuration must be done before';
		$tpl->assign( "msg", $msg);
		$tpl->assign( "page", 'keywords');
		break;
	}
	$keywords_form = array(
			'title' => 'Keywords',
			'champs' => array());

	for ($i=0;$i<count($keywords);$i++)
	{
		array_push($keywords_form['champs'],array(
				'field_id'	=> 'keywords_'.$i,
				'type'		=> 'text',
				'label'		=> 'Keywords '.($i+1),
				'value'		=> $keywords[$i]
				));
	}

	$new_keywords = array(
				'field_id'	=> 'keywords_new',
				'type'		=> 'text',
				'label'		=> 'New keywords',
				'value'		=> ''
				);
	array_push($keywords_form['champs'],$new_keywords);
	$form = array(
		'title' 	=> 'Keywords configuration',
		'action'	=> 'index.php?page=save_keywords'.$debug,
		'part' 		=> array()
		);
	array_push($form['part'],$keywords_form);
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form));
	$tpl->assign( "page", 'keywords');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "general_conf" ); // draw the template
	break;

case 'save_conf':
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
default:
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
	$tracker = array(
			'title' => 'Tracker',
			'champs' => array(
					array(
						'field_id'	=> 'tracker_id',
						'type'		=> 'list',
						'label'		=> 'Tracker provider',
						'choices'	=> array(
										array('id' => 't411', 'label' => 'T411')
									),
						'value'		=> $confVal['tracker']['id'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'tracker_username',
						'type'		=> 'text',
						'label'		=> 'Tracker username',
						'value'		=> $confVal['tracker']['user'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'tracker_password',
						'type'		=> 'password',
						'label'		=> 'Tracker password',
						'mandatory'	=> true,
						'value'		=> 'initial'
						)
					)
			);

	$slot_list = array();
	for ($i=1;$i<13;$i++)
		array_push($slot_list,array('id'=> $i,'label'=>$i));

	$transmission = array(
			'title' => 'Transmission',
			'champs' => array(
					array(
						'field_id'	=> 'trans_server',
						'type'		=> 'text',
						'label'		=> 'Transmission server',
						'value'		=> $confVal['transmission']['server'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_port',
						'type'		=> 'text',
						'label'		=> 'Transmission port',
						'value'		=> $confVal['transmission']['port'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_username',
						'type'		=> 'text',
						'label'		=> 'Transmission Username',
						'value'		=> $confVal['transmission']['user'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_password',
						'type'		=> 'password',
						'label'		=> 'Transmission Password',
						'mandatory'	=> true,
						'value'		=> 'initial'
						),
					array(
						'field_id'	=> 'trans_slotNumber',
						'type'		=> 'list',
						'label'		=> 'Transmission maximum slots',
						'choices'	=> $slot_list,
						'value'		=> $confVal['transmission']['slotNumber'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_folder',
						'type'		=> 'text',
						'label'		=> 'Local Transfer directory (keep empty for disable)',
						'value'		=> $confVal['transmission']['folder']
						)
					)
			);

	$email = array(
			'title' => 'Email notification',
			'champs' => array(
					array(
						'field_id'	=> 'smtp_enable',
						'type'		=> 'list',
						'label'		=> 'Enable',
						'choices'	=> array(
										array('id' => '0', 'label' => 'No'),
										array('id' => '1', 'label' => 'Yes'),
									),
						'value'		=> ($confVal['smtp']['server']=='') ? 0 : 1,
						'mandatory'	=> true,
						'onChange'	=> "(this.value==0)?mode = 'fieldHidden':mode = 'fieldDisplay';visiField(['smtp_server','smtp_port','smtp_ssltls','smtp_emailSender','smtp_username','smtp_password'],mode);(mode=='fieldDisplay')?document.getElementsByName('smtp_ssltls')[0].onchange():true;"
						),
					array(
						'field_id'	=> 'smtp_server',
						'type'		=> 'text',
						'label'		=> 'SMTP server',
						'value'		=> $confVal['smtp']['server'],
						'visible'	=> ($confVal['smtp']['server']!=''),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_port',
						'type'		=> 'text',
						'label'		=> 'SMTP port',
						'value'		=> $confVal['smtp']['port'],
						'visible'	=> ($confVal['smtp']['server']!=''),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_ssltls',
						'type'		=> 'list',
						'label'		=> 'SSL/TLS encryption',
						'choices'	=> array(
										array('id' => '0', 'label' => 'No'),
										array('id' => '1', 'label' => 'Yes'),
									),
						'value'		=> ($confVal['smtp']['ssltls']=='True') ? 1 : 0,
						'onChange'	=> "(this.value==0)?mode = 'fieldHidden':mode = 'fieldDisplay';visiField(['smtp_username','smtp_password'],mode)",
						'visible'	=> ($confVal['smtp']['server']!=''),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_username',
						'type'		=> 'text',
						'label'		=> 'Authentification Username',
						'value'		=> $confVal['smtp']['user'],
						'visible'	=> ($confVal['smtp']['ssltls']!='False'),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_password',
						'type'		=> 'password',
						'label'		=> 'Authentification Password',
						'visible'	=> ($confVal['smtp']['ssltls']!='False'),
						'mandatory'	=> true,
						'value'		=> 'initial'
						),
					array(
						'field_id'	=> 'smtp_emailSender',
						'type'		=> 'text',
						'label'		=> 'Sender Email',
						'value'		=> $confVal['smtp']['emailSender'],
						'visible'	=> ($confVal['smtp']['server']!=''),
						'mandatory'	=> true
						)
					)
			);
	$form = array(
		'title' 	=> 'Configuration parameters',
		'action'	=> 'index.php?page=save_conf'.$debug,
		'part' 		=> array()
		);
	array_push($form['part'],$tracker);
	array_push($form['part'],$transmission);
	array_push($form['part'],$email);

	$configFile = array(
		'title' => 'Import configuration file',
		'champs' => array(
				array(
					'field_id'	=> 'configFile',
					'type'		=> 'file',
					'label'		=> 'Import file (*.xml)'
					)
				)
		);

	$import = array(
		'title' 	=> 'Configuration importation',
		'action'	=> 'index.php?page=import_conf'.$debug,
		'part' 		=> array($configFile)
		);
	
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form,$import));
	$tpl->assign( "page", 'config');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "general_conf" ); // draw the template
	
}

?>
