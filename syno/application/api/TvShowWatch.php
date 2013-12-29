<?

error_reporting(E_ALL | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

if (!isset($path))
	$path = '../';

require_once($path."inc/constants.php");
require_once($path."functions.php");

class TvShowWatch
{
	var $conffile;
	var $py_file;
	var $auth;
	var $cmd;

	function TvShowWatch($py_file = API_FILE, $conffile = CONF_FILE, $serielist = SERIES_FILE, $debug = False, $run_file = RUN_FILE)
	{
		$this->debug = ($debug != False);
		$this->auth = false;
		if (!file_exists($conffile))
		{
			throw new Exception("Configuration file $conffile does not exist",401);
			//trigger_error("Configuration file $conffile does not exist");
			return false;
		}
		$this->conffile = $conffile;
		$this->serielist = $serielist;
		if (!file_exists($py_file))
		{
			throw new Exception("Python executable $py_file does not exist",401);
			//trigger_error("Python file $py_file does not exist");
			return false;
		}
		$this->py_file = $py_file;
		if (!file_exists($run_file))
		{
			throw new Exception("Python run file $run_file does not exist",401);
			//trigger_error("Python run file $run_file does not exist",E_ERROR);
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

	function getEpisode($serie_id,$season,$episode)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action getEpisode --arg '{\"id\":$serie_id, \"season\":$season,\"episode\":$episode}'";
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

if (isset($_GET['action']))
{
	$debug = (isset($_GET['debug'])) ? $_GET['debug'] : false;
	switch ($_GET['action'])
	{
		case 'save_conf':
			$result = '{"tracker":' . tracker_api_conf($_POST);
			$result .= ',"transmission":' . transmission_api_conf($_POST);
			$result .= ',"smtp":' . email_api_conf($_POST).'}';
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
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
			die($msg);
			break;
		case 'get_conf':
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			echo json_encode($TSW->getConf());
			break;
		case 'save_keywords':
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			if (isset($_POST['keywords']))
			{
				$res = $TSW->setConf(json_encode(array('keywords' => $_POST['keywords'])));
				if ($res['rtn']!='200')
					die(json_encode(array('rtn' => $res['rtn'], 'error' => $res['error']	)));
				die(json_encode(array('rtn' => 200, 'error' => 'Keywords updated')));
			}
			else
			{
				die(json_encode(array('rtn' => 415, 'error' => 'Unable to parse arguments'	)));
			}			
			break;
		case 'import_conf':
			if(isset($_FILES['configFile']))
			{ 
				 if(move_uploaded_file($_FILES['configFile']['tmp_name'], CONF_FILE))
				 {
				  $msg =  'Upload of configuration file completed!';
				 }
				 else //Sinon (la fonction renvoie FALSE).
				 {
				  $msg =  'Failed to upload configuration file!';
				 }
			} 
			else
				$msg =  'Failed to upload configuration file due to missing file';
			die($msg);
			break;
		case "getSeries":
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->getSeries()));
			break;
		case "getEpisode":
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->getEpisode((int)$_POST['serie_id'],(int)$_POST['season'],(int)$_POST['episode'])));
			break;
		case "setSerie":
				if (isset($_POST['season']) and isset($_POST['episode']) and isset($_POST['serie_id']))
				{
					$serie_id = (int)$_POST['serie_id'];
					$season = (int)$_POST['season'];
					$episode = (int)$_POST['episode'];
					if ($season * $episode != 0)
					{
						if (!isset($TSW))
							$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
						$TSW->auth();
						try
						{
							$val_episode = $TSW->getEpisode($serie_id, $season, $episode, 'en');
						}
						catch (Exception $e)
						{
							die(json_encode(array('rtn' => 419, 'error' => 'Episode S' . sprintf("%02s", $season) . 'E'. sprintf("%02s", $episode) . ' does not exist')));
						}
						$update = $TSW->setSerie($serie_id,array('season'=>$season,'episode'=>$episode,'expected'=>$val_episode['result']['firstaired']));
						if ($update['rtn'] != '200')
							die(json_encode(array('rtn' => $update['rtn'], 'error' => 'Error during TV Show update<br />'.$update['error'])));
						else
						{
							die(json_encode(array('rtn' => 200, 'error' => 'TV Show updated')));
						}
					} else
					{
						die(json_encode(array('rtn' => 499, 'error' => 'You must indicate both of Season and Episode numbers')));
					}
				} else
				{
					die(json_encode(array('rtn' => 499, 'error' => 'You must indicate both of Season and Episode numbers')));
				}
			break;
		default:
	}
}

?>
