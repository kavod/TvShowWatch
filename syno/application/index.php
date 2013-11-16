<?
include "inc/rain.tpl.class.php"; //include Rain TPL
include "functions.php";

define("CONF_VERSION", '1.8');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');

raintpl::$tpl_dir = "tpl/"; // template directory
raintpl::$cache_dir = "tmp/"; // cache directory

switch($_GET['page'])
{
case 'series_list':
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
	$form = array(
		'title' 	=> 'Importation',
		'action'	=> 'index.php?page=save_serieFile',
		'part' 		=> array($serieFile)
		);

	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form));
	$tpl->assign( "page", 'series');

	break;

case 'save_keywords':
	$cmd = 'PATH=/var/packages/python/target/bin:$PATH ; python /volume1/homes/boris/series/tvShowWatch.py -c"' . CONF_FILE . '"';
	if (file_exists(CONF_FILE))
	{
		$doc = new DOMDocument();
		$doc->load(CONF_FILE);
		$confVal = getArray($doc);
	} else die('configuration file unfounable');

	$keywords = array();	
	for ($i=0;$_POST['keywords_'.$i]!='';$i++)
		$keywords[] = $_POST['keywords_'.$i];
	if ($_POST['keywords_new'] != '')
		$keywords[] = $_POST['keywords_new'];
	$arg = implode(",",$keywords);
	$cmd =  $cmd . ' --action config --arg ' . escapeshellarg('4,' . $arg . ',') . ' >> /tmp/log_tsw 2>&1';
	exec("echo ".  escapeshellarg($cmd) . ">/tmp/log_tsw 2>&1");                                                             
        exec($cmd);
	$msg = 'The keywords have been saved';

case 'keywords':

	if (file_exists(CONF_FILE))
	{
		$doc = new DOMDocument();
		$doc->load(CONF_FILE);
		$confVal = $doc->getElementsByTagName('keywords');
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
	
	$keywords = array();
	foreach ($confVal->item(0)->getElementsByTagName('keyword') as $childNode) 
	{
		if ($childNode->nodeType != XML_TEXT_NODE) 
		{ 
		    $keywords[] = $childNode->firstChild->nodeValue; 
		}
	} 

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
		'action'	=> 'index.php?page=save_keywords',
		'part' 		=> array()
		);
	array_push($form['part'],$keywords_form);
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form));
	$tpl->assign( "page", 'keywords');
	$tpl->assign( "msg", $msg);
	break;

case 'save_conf':
	if (file_exists(CONF_FILE))
	{
		$doc = new DOMDocument();
		$doc->load(CONF_FILE);
		$confVal = getArray($doc);
		$tracker_password = ($_POST['tracker_password']=='initial') ? $confVal['conf']['tracker']['password'] : $_POST['tracker_password'];
		$transmission_password = ($_POST['trans_password']=='initial') ? $confVal['conf']['transmission']['password'] : $_POST['trans_password'];
		$smtp_password = ($_POST['smtp_password']=='initial') ? $confVal['conf']['smtp']['password'] : $_POST['smtp_password'];
		$keywordsNode = $doc->getElementsByTagName('keywords');
		$keywords = array();		
		foreach ($keywordsNode->item(0)->getElementsByTagName('keyword') as $childNode) 
		{
			if ($childNode->nodeType != XML_TEXT_NODE) 
			{ 
			    $keywords[] = $childNode->firstChild->nodeValue; 
			}
		} 
		$keywords_conf = keywords_conf($keywords);
	} else
	{
		$tracker_password =  $_POST['tracker_password'];
		$transmission_password = $_POST['transmission_password'];
		$smtp_password = $_POST['smtp_password'];
		$keywords_conf = keywords_conf(array());
	}

	$smtp_ssltls = ($_POST['smtp_ssltls'] == '1') ? '1' : '0';
	$format = "<conf><version>%s</version>%s%s%s%s</conf>";
	$traker_conf = tracker_conf($_POST['tracker_id'],$_POST['tracker_username'],$tracker_password);
	$transmission_conf = transmission_conf($_POST['trans_server'],$_POST['trans_port'],$_POST['trans_username'],$transmission_password,$_POST['trans_slotNumber'],$_POST['trans_folder']);
	$email_conf = email_conf($_POST['smtp_server'],$_POST['smtp_port'],$smtp_ssltls,$_POST['smtp_username'],$smtp_password,$_POST['smtp_emailSender']);
	$config_out = sprintf($format, CONF_VERSION,$traker_conf, $transmission_conf, $email_conf,$keywords_conf);

	$fp = fopen(CONF_FILE, 'w');
	fwrite($fp, $config_out);
	fclose($fp);
	$msg = 'Configuration file saved';

case 'conf':
default:
	if (file_exists(CONF_FILE))
	{
		$doc = new DOMDocument();
		$doc->load(CONF_FILE);
		$confVal = getArray($doc);
	} else 
	{
		$confVal = Array ('conf' => Array(
						'tracker' => Array('id'=>'','user'=>''),
						'transmission' => Array('server'=>'','port'=>'','user'=>'','slotNumber' => 6,'folder'=>''),
						'smtp' => Array('server','port','ssltls' => 'False','user','password','emailSender')
							));
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
						'value'		=> $confVal['conf']['tracker']['id'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'tracker_username',
						'type'		=> 'text',
						'label'		=> 'Tracker username',
						'value'		=> $confVal['conf']['tracker']['user'],
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
						'value'		=> $confVal['conf']['transmission']['server'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_port',
						'type'		=> 'text',
						'label'		=> 'Transmission port',
						'value'		=> $confVal['conf']['transmission']['port'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_username',
						'type'		=> 'text',
						'label'		=> 'Transmission Username',
						'value'		=> $confVal['conf']['transmission']['user'],
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
						'value'		=> $confVal['conf']['transmission']['slotNumber'],
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'trans_folder',
						'type'		=> 'text',
						'label'		=> 'Local Transfer directory (keep empty for disable)',
						'value'		=> $confVal['conf']['transmission']['folder']
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
						'value'		=> ($confVal['conf']['smtp']['server']=='') ? 0 : 1,
						'mandatory'	=> true,
						'onChange'	=> "(this.value==0)?mode = 'fieldHidden':mode = 'fieldDisplay';visiField(['smtp_server','smtp_port','smtp_ssltls','smtp_emailSender','smtp_username','smtp_password'],mode);(mode=='fieldDisplay')?document.getElementsByName('smtp_ssltls')[0].onchange():true;"
						),
					array(
						'field_id'	=> 'smtp_server',
						'type'		=> 'text',
						'label'		=> 'SMTP server',
						'value'		=> $confVal['conf']['smtp']['server'],
						'visible'	=> ($confVal['conf']['smtp']['server']!=''),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_port',
						'type'		=> 'text',
						'label'		=> 'SMTP port',
						'value'		=> $confVal['conf']['smtp']['port'],
						'visible'	=> ($confVal['conf']['smtp']['server']!=''),
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
						'value'		=> ($confVal['conf']['smtp']['ssltls']=='True') ? 1 : 0,
						'onChange'	=> "(this.value==0)?mode = 'fieldHidden':mode = 'fieldDisplay';visiField(['smtp_username','smtp_password'],mode)",
						'visible'	=> ($confVal['conf']['smtp']['server']!=''),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_username',
						'type'		=> 'text',
						'label'		=> 'Authentification Username',
						'value'		=> $confVal['conf']['smtp']['user'],
						'visible'	=> ($confVal['conf']['smtp']['ssltls']!='False'),
						'mandatory'	=> true
						),
					array(
						'field_id'	=> 'smtp_password',
						'type'		=> 'password',
						'label'		=> 'Authentification Password',
						'visible'	=> ($confVal['conf']['smtp']['ssltls']!='False'),
						'mandatory'	=> true,
						'value'		=> 'initial'
						),
					array(
						'field_id'	=> 'smtp_emailSender',
						'type'		=> 'text',
						'label'		=> 'Sender Email',
						'value'		=> $confVal['conf']['smtp']['emailSender'],
						'visible'	=> ($confVal['conf']['smtp']['server']!=''),
						'mandatory'	=> true
						)
					)
			);
	$form = array(
		'title' 	=> 'Configuration parameters',
		'action'	=> 'index.php?page=save_conf',
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
		'action'	=> 'index.php?page=import_conf',
		'part' 		=> array($configFile)
		);
	
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form,$import));
	$tpl->assign( "page", 'config');
	$tpl->assign( "msg", $msg);

	
}
$tpl->draw( "general_conf" ); // draw the template
?>
