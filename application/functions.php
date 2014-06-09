<? 
function cmp($a, $b)
{
    return strcmp($a['col1']["label"], $b['col1']["label"]);
}

function cmp_serie_az($a, $b)
{
    return strcmp($a["series_name"], $b['series_name']);
}

date_default_timezone_set('America/New_York'); 
function cmp_serie($a, $b)
{
	$a['firstaired'] = (string)$a['firstaired'] !== '' ? new DateTime((string)$a['firstaired']) : null;
	$b['firstaired'] = (string)$b['firstaired'] !== '' ? new DateTime((string)$b['firstaired']) : null;
    return ($a['firstaired'] < $b['firstaired']) ? -1 : 1;
}

function filter_series($a)
{
	$a['firstaired'] = (string)$a['firstaired'] !== '' ? new DateTime((string)$a['firstaired']) : null;

	$today = getdate();
	if ($a['firstaired'] == null)
		return false;

	return ($a['firstaired']->getTimestamp() > mktime(12,0,0,$today['mon'],$today['mday']+1));
}

function serieStatus($status_id)
{
	switch($status_id)
	{
		case '10':
			return 'Waiting for broadcast';
		case '15':
			return 'Torrent search scheduled';
		case '20':
			return 'Waiting for torrent availability';
		case '21':
			return 'No tracker configured';
		case '30':
			return 'Download in progress';
		case '90':
			return 'Broadcast achieved';
		default:
			return 'Unknown status';
	}
}

/*function display_error($page='home',$msg='')
{
	$tpl = new raintpl(); //include Rain TPL
	$tpl->assign( "page", $page);
	$tpl->assign( "msg", $msg);
	$tpl->draw( "general_conf" );
	die();
}*/

function tracker_api_conf($post)
{
	$conf_out = '{"id":"' . $post['tracker_id'] . '","user":"'.$post['tracker_username'].'"';
	$conf_out .= ($post['tracker_password'] != 'initial') ? ',"password":"'.$post['tracker_password'] . '"' : '';
	$conf_out .= '}';
	return $conf_out;
}

function transmission_api_conf($post)
{
	$conf_out = '{"server":"' . $post['trans_server'] . '","port":'.$post['trans_port'];
	$conf_out .= ',"user":"' . $post['trans_username'] . '"';
	$conf_out .= ($post['trans_password'] != 'initial') ? ',"password":"'.$post['trans_password'] . '"' : '';
	$conf_out .= ',"slotNumber":' . $post['trans_slotNumber'];
	$conf_out .= ',"folder":"' . $post['trans_folder'] . '"';
	$conf_out .= '}';
	return $conf_out;
}

function email_api_conf($post)
{
	if ($post['smtp_enable'] == '0')
		return '{"enable":"False"}';
	else
		$values = $post;
	$conf_out = '{"server":"' . $values['smtp_server'] . '","port":'.$values['smtp_port'];
	$conf_out .= ($values['smtp_ssltls'] == '1') ? ',"ssltls":"True"' : ',"ssltls":"False"';
	$conf_out .= ',"user":"' . $values['smtp_username'] . '"';
	$conf_out .= ($values['smtp_password'] != 'initial') ? ',"password":"'.$values['smtp_password'] . '"' : '';
	$conf_out .= ',"emailSender":"' . $values['smtp_emailSender'] . '"';
	$conf_out .= '}';
	return $conf_out;
}

$tab_msg = array(
	'conf' => 	'Initial configuration must be done before',
	'series' =>	'No TV Show scheduled'
);
	
function check_file($file,$type='conf',$page='home')
{
	global $tab_msg;
	if (!file_exists($file))
	{
		$msg = $tab_msg[$type];
		display_error($page,$msg);
		die();
	}
	return true;
}

function check_conf($conffile,$page='home') { check_file($conffile,'conf',$page);}
function check_series($seriefile,$page='home') { check_file($seriefile,'series',$page);}
function check_result($result,$msg='General error',$page='home',$result_expected=true)
{
	if ($result['rtn']!='200')
		$msg .= '<br>\n' . $result['error'];
	else
	{
		if (!$result_expected || isset($result['result']))
			return true;
	}
	display_error($page,$msg);
	die();
}

function getArray($node) 
{ 
    $array = false; 

    if ($node->hasAttributes()) 
    { 
        foreach ($node->attributes as $attr) 
        { 
            $array[$attr->nodeName] = $attr->nodeValue; 
        } 
    } 

    if ($node->hasChildNodes()) 
    {
        if ($node->childNodes->length == 1) 
        {  
		if ($node->firstChild->nodeName=='#text') 
			$array = $node->firstChild->nodeValue;
		else
			$array[$node->firstChild->nodeName] = getArray($node->firstChild); 
        } 
        else 
        { 
            foreach ($node->childNodes as $childNode) 
            {
                if ($childNode->nodeType != XML_TEXT_NODE) 
                { 
                    $array[$childNode->nodeName] = getArray($childNode); 
                }
            } 
        } 
    } else
    { 
	$array = $node->nodeValue;
    }

    return $array; 
} 
?>
