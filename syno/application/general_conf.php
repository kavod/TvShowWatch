<?
include "inc/rain.tpl.class.php"; //include Rain TPL
include "functions.php";

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
		'action'	=> 'general_conf.php?page=save_serieFile',
		'part' 		=> array($serieFile)
		);

	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form));

	break;

case 'save_conf':
	define('VERSION','1.7');

	$format = "<conf><version>%s</version>%s%s%s</conf>";
	$traker_conf = tracker_conf($_POST['tracker_id'],$_POST['tracker_username'],$_POST['tracker_password'],$_POST['tracker_keywords']);
	$transmission_conf = transmission_conf($_POST['trans_server'],$_POST['trans_port'],$_POST['trans_username'],$_POST['trans_password'],$_POST['trans_slotNumber'],$_POST['trans_folder']);
	$email_conf = email_conf($_POST['smtp_server'],$_POST['smtp_port'],$_POST['smtp_ssltls'],$_POST['smtp_username'],$_POST['smtp_password'],$_POST['smtp_emailSender']);
	$config_out = sprintf($format, VERSION,$traker_conf, $transmission_conf, $email_conf);

	$fp = fopen('/var/packages/TvShowWatch/etc/config.xml', 'w');
	fwrite($fp, $config_out);
	fclose($fp);
	echo "OK";
	break;

case 'general_conf':
default:
	$doc = new DOMDocument();
	$doc->load($dossier = '/var/packages/TvShowWatch/etc/series.xml');
	$trackerVal = $doc->getElementsByTagName('tracker')->item(0);
	$tracker = array(
			'title' => 'Tracker',
			'champs' => array(
					array(
						'field_id'	=> 'tracker_id',
						'type'		=> 'list',
						'label'		=> 'Tracker provider',
						'choices'	=> array(
										array('id' => 't411', 'label' => 'T411')
									)
						),
					array(
						'field_id'	=> 'tracker_username',
						'type'		=> 'text',
						'label'		=> 'Tracker username',
						'value'		=> $trackerVal->getElementsByTagName('username')->item(0)->value
						),
					array(
						'field_id'	=> 'tracker_password',
						'type'		=> 'password',
						'label'		=> 'Tracker password'
						),
					array(
						'field_id'	=> 'tracker_keywords',
						'type'		=> 'text',
						'label'		=> 'Default search keywords'
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
						'label'		=> 'Transmission server'
						),
					array(
						'field_id'	=> 'trans_port',
						'type'		=> 'text',
						'label'		=> 'Transmission port'
						),
					array(
						'field_id'	=> 'trans_username',
						'type'		=> 'text',
						'label'		=> 'Transmission Username'
						),
					array(
						'field_id'	=> 'trans_password',
						'type'		=> 'password',
						'label'		=> 'Transmission Password'
						),
					array(
						'field_id'	=> 'trans_slotNumber',
						'type'		=> 'list',
						'label'		=> 'Transmission maximum slots',
						'choices'	=> $slot_list
						),
					array(
						'field_id'	=> 'trans_folder',
						'type'		=> 'text',
						'label'		=> 'Local Transfer directory (keep empty for disable)'
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
									)
						),
					array(
						'field_id'	=> 'smtp_server',
						'type'		=> 'text',
						'label'		=> 'SMTP server'
						),
					array(
						'field_id'	=> 'smtp_port',
						'type'		=> 'text',
						'label'		=> 'SMTP server'
						),
					array(
						'field_id'	=> 'smtp_ssltls',
						'type'		=> 'list',
						'label'		=> 'SSL/TLS encryption',
						'choices'	=> array(
										array('id' => '0', 'label' => 'No'),
										array('id' => '1', 'label' => 'Yes'),
									)
						),
					array(
						'field_id'	=> 'smtp_username',
						'type'		=> 'text',
						'label'		=> 'Authentification Username'
						),
					array(
						'field_id'	=> 'smtp_password',
						'type'		=> 'password',
						'label'		=> 'Authentification Password'
						),
					array(
						'field_id'	=> 'smtp_emailSender',
						'type'		=> 'text',
						'label'		=> 'Sender Email'
						)
					)
			);
	$form = array(
		'title' 	=> 'Configuration parameters',
		'action'	=> 'general_conf.php?page=save_conf',
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
		'action'	=> 'general_conf.php?page=import_conf',
		'part' 		=> array($configFile)
		);
	
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "form", array($form,$import));

	
}
$tpl->draw( "general_conf" ); // draw the template
?>
