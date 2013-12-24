<?
define("PY_FILE", '/var/packages/TvShowWatch/target/TSW_api.py');
define("RUN_FILE", '/var/packages/TvShowWatch/target/tvShowWatch.py');
define("CONF_FILE", '/var/packages/TvShowWatch/etc/config.xml');
define("LIST_FILE", '/var/packages/TvShowWatch/etc/series.xml');
define("PYTHON_EXEC", 'PATH=/var/packages/python/target/bin:$PATH ; python');
define("LOGFILE", '/var/log/TSW.log');

class TvShowWatch
{
	var $conffile;
	var $py_file;
	var $auth;
	var $cmd;

	function TvShowWatch($py_file = PY_FILE, $conffile = CONF_FILE, $serielist = LIST_FILE, $debug = False, $run_file = RUN_FILE)
	{
		$this->debug = ($debug != False);
		$this->auth = false;
		if (!file_exists($conffile))
		{
			trigger_error("Configuration file $conffile does not exist");
			return false;
		}
		$this->conffile = $conffile;
		if (!file_exists($serielist))
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
		if (!file_exists($run_file))
		{
			trigger_error("Python run file $run_file does not exist");
			return false;
		}
		$this->run_file = $run_file;
		$this->cmd = $this->py_file . ' -c "'.str_replace('"','\"',$this->conffile) . '" -s "'.str_replace('"','\"',$this->serielist).'" ';
		$this->run_cmd = $this->run_file . ' -c "'.str_replace('"','\"',$this->conffile) . '" -s "'.str_replace('"','\"',$this->serielist).'" ';
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
			if ($key == 'emails' && count($value)>0)
				$cmd .= '"emails":["' . implode('","',$value) . '"],';
			elseif ($key == 'emails' && count($value)<1)
				$cmd .= '"emails":[],';
			else
				$cmd.='"' . $key . '":"' . $value . '",';
		}
		$cmd .= '"status":10';
		/*if (count($param)>0)
			$cmd = substr($cmd,0,-1);*/
		$cmd .= "}}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

        function delSerie($id)
        {
                $cmd = PYTHON_EXEC . " " . $this->cmd ." --action del --arg '{\"id\":" . $id . "}'";
                exec($cmd,$result);
                if ($this->debug)
                {
                        echo $cmd.'<br />';
                        print_r($result);
                }
                return json_decode($result[0],true);
        }

        function addSerie($id)
        {
                $cmd = PYTHON_EXEC . " " . $this->cmd ." --action add --arg '{\"id\":" . $id . "}'";
                exec($cmd,$result);
                if ($this->debug)
                {
                        echo $cmd.'<br />';
                        print_r($result);
                }
                return json_decode($result[0],true);
        }
	
	function testRunning()
	{
		$cmd = '/var/packages/TvShowWatch/scripts/start-stop-status status';
		exec($cmd,$result);
		if ($this->debug)
                {
                        echo $cmd.'<br />';
                        print_r($result);
                }
		return str_replace('tvShowWatch is ','',$result[0]);
	}

	function run()
	{
		$cmd = "date >> " . LOGFILE . ";".PYTHON_EXEC . " " . $this->run_cmd." --action run >>".LOGFILE." 2>&1 &";
		exec($cmd,$result);
		if ($this->debug)
                {
                        echo $cmd.'<br />';
                }
		return true;
	}
}

?>
