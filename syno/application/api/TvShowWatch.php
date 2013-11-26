<?
define("PY_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("LIST_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("PYTHON_EXEC", '/var/packages/python/target/bin/python');

class TvShowWatch
{
	var $conffile;
	var $py_file;
	var $auth;
	var $cmd;

	function TvShowWatch($py_file = PY_FILE, $conffile = CONF_FILE, $serielist = LIST_FILE, $debug = False)
	{
		$this->debug = ($debug != False);
		$this->auth = false;
		if (!file_exists($conffile))
		{
			trigger_error("Configuration file $conffile does not exist");
			return false;
		}
		$this->conffile = $conffile;
		if (!file_exists($conffile))
		{
			trigger_error("Serie list file $serielist does not exist");
			return false;
		}
		$this->serielist = $serielist;
		if (!file_exists($py_file))
		{
			trigger_error("Python file $py_file does not exist");
			return false;
		}
		$this->py_file = $py_file;
		$this->cmd = $this->py_file . ' -c "'.str_replace('"','\"',$this->conffile) . '" -s "'.str_replace('"','\"',$this->serielist).'" ';
	}

	function auth($auth=true)
	{
		if ($this->auth != $auth)
		{
			$this->auth = $auth;
			if ($auth)
				$this->cmd .= '--admin ';
			else
				$this->cmd = str_replace('--admin ','',$this->cmd);
		}
	}

	function isAuth()
	{
		return $this->auth;
	}	

	function getConf()
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action getconf';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function setConf($conf)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action config --arg '{\"conf\":" . $conf . "}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function createConf($conf)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action init --arg '{\"conf\":" . $conf . "}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function getSeries()
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action list';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function setSerie($id,$param)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action update --arg '{\"id\":" . $id . ",\"param\":{";
		foreach($param as $key => $value)
		{
			$cmd.='"' . $key . '":"' . $value . '",';
		}
		if (count($param)>0)
			$cmd = substr($cmd,0,-1);
		$cmd .= "}}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}
}

?>
