<?
if (!TSW)
	die('Not in TSW');

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
				'enctype' => 'file',
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
	
	$tpl = new raintpl();
	$tpl->assign( "content", $content);
	$tpl->assign( "page", 'config');
	$tpl->assign( "msg", $msg);
	$tpl->draw( "home" ); // draw the template
?>
