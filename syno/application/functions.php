<? 
function tracker_conf($tracker_id,$username,$password)
{
	$config_out = "<tracker><id>";
	$config_out .= $tracker_id;
	$config_out .= "</id><user>";
	$config_out .= $username;
	$config_out .= "</user><password>";
	$config_out .= $password;
	$config_out .= "</password>";
	$config_out .= "</tracker>";
	return $config_out;
}

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
	$conf_out = '{"server":"' . $post['smtp_server'] . '","port":'.$post['smtp_port'];
	$conf_out .= ($post['smtp_ssltls'] == '1') ? ',"ssltls":"True"' : ',"ssltls":"False"';
	$conf_out .= ',"user":"' . $post['smtp_username'] . '"';
	$conf_out .= ($post['smtp_password'] != 'initial') ? ',"password":"'.$post['smtp_password'] . '"' : '';
	$conf_out .= ',"emailSender":"' . $post['smtp_emailSender'] . '"';
	$conf_out .= '}';
	return $conf_out;
}

function transmission_conf($server,$port,$username,$password,$slotNumber,$folder)
{
	$config_out = "<transmission><server>";
	$config_out .= $server;
	$config_out .= "</server><port>";
	$config_out .= $port;
	$config_out .= "</port><user>";
	$config_out .= $username;
	$config_out .= "</user><password>";
	$config_out .= $password;
	$config_out .= "</password><slotNumber>";
	$config_out .= $slotNumber;
	$config_out .= "</slotNumber>";
	if ($folder != "")
	{
		$config_out .= "<folder>";
		$config_out .= $folder;
		$config_out .= "</folder>";
	} else
	{
		$config_out .= "<folder />";
	}
	$config_out .= "</transmission>";
	return $config_out;
}

function email_conf($server,$port,$ssltls,$username,$password,$emailSender)
{
	$config_out = "<smtp><server>";
	$config_out .= $server;
	$config_out .= "</server><port>";
	$config_out .= $port;
	$config_out .= "</port><ssltls>";
	$config_out .= ($ssltls=='1') ? 'True' : 'False';
	$config_out .= "</ssltls>";
	if ($username != "")
	{
		$config_out .= "<user>";
		$config_out .= $username;
		$config_out .= "</user><password>";
		$config_out .= $password;
		$config_out .= "</password>";
	}
	$config_out .= "<emailSender>";
	$config_out .= $emailSender;
	$config_out .= "</emailSender>";
	$config_out .= "</smtp>";
	return $config_out;
}

function keywords_conf($keywords)
{
	$config_out = "<keywords>";
	foreach ($keywords as $keyword)
	{
		$config_out .= "<keyword>";
		$config_out .= $keyword;
		$config_out .= "</keyword>";
	}
	$config_out .= "</keywords>";
	return $config_out;
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
