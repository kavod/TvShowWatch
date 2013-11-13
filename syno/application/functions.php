<? 
function tracker_conf($tracker_id,$username,$password,$keywords)
{
	$config_out = "<tracker><id>";
	$config_out .= $tracker_id;
	$config_out .= "</id><user>";
	$config_out .= $username;
	$config_out .= "</user><password>";
	$config_out .= $password;
	$config_out .= "</password>";
	if ($keywords != "")
	{
		$config_out .= "<keywords>";
		$config_out .= $keywords;
		$config_out .= "</keywords>";
	}
	$config_out .= "</tracker>";
	return $config_out;
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
	$config_out .= ($ssltls==1) ? 'True' : 'False';
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
?>
