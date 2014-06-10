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

	function getSeries($load_tvdb=false)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action list --arg '{\"load_tvdb\":" . (($load_tvdb) ? 'true' : 'false') . "}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function getSerie($id)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd ." --action list --arg '{\"ids\":[" . $id . "]}'";
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
			elseif ($key == 'keywords' && count($value)>0)
				$cmd .= '"keywords":["' . implode('","',$value) . '"],';
			elseif ($key == 'keywords' && count($value)<1)
				$cmd .= '"keywords":[],';
			else
				$cmd.='"' . $key . '":"' . $value . '",';
		}
		$cmd .= '"status":15';
		$cmd .= "}}'";
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function addemail($id,$email)
	{
		$serie = $this->getSerie($id);
		$emails = $serie['result']['emails'];
		$emails[] = $email;
		return $this->setSerie($id,array('emails'=>$emails));
	}

	function delemail($id,$email)
	{
		$serie = $this->getSerie($id);
		$emails = $serie['result']['emails'];
		for( $i=0;$i<count($emails);$i++)
		{
			if ($emails[$i] == $email)
				unset($emails[$i]);
		}
		return $this->setSerie($id,array('emails'=>$emails));
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

    function resetSerieKeywords($id)
    {
            $cmd = PYTHON_EXEC . " " . $this->cmd ." --action resetKeywords --arg '{\"id\":" . $id . "}'";
            exec($cmd,$result);
            if ($this->debug)
            {
                    echo $cmd.'<br />';
                    print_r($result);
            }
            return json_decode($result[0],true);
    }

    function resetAllKeywords()
    {
            $cmd = PYTHON_EXEC . " " . $this->cmd ." --action resetAllKeywords";
            exec($cmd,$result);
            if ($this->debug)
            {
                    echo $cmd.'<br />';
                    print_r($result);
            }
            return json_decode($result[0],true);
    }

	function search($pattern)
    {
            $cmd = PYTHON_EXEC . " " . $this->cmd ." --action search --arg '{\"pattern\":\"" . $pattern . "\"}'";
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
		$cmd = '/var/packages/TvShowWatch/scripts/start-stop-status status 2>&1';
		exec($cmd,$result);
		if ($this->debug)
		{
		        echo $cmd.'<br />';
		        print_r($result);
		}
		return str_replace('tvShowWatch is ','',$result[0]);
	}

	function push($serie_id,$destination)
	{
			$cmd = PYTHON_EXEC . " " . $this->cmd ." --action push --arg '{\"id\":" . $serie_id . ",\"filepath\":\"" . $destination . "\"}'";
            exec($cmd,$result);
            if ($this->debug)
            {
                    echo $cmd.'<br />';
                    print_r($result);
            }
            return json_decode($result[0],true);
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

	function logs()
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action logs';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}
}

if (isset($_GET['action']))
{
	$debug = (isset($_GET['debug'])) ? $_GET['debug'] : false;
	switch ($_GET['action'])
	{
		case "run":
			if (!isset($TSW))
				$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			$TSW->auth();
			$TSW-run();
			break;
		case 'save_conf':
			$result = '{"tracker":' . tracker_api_conf($_POST);
			$result .= ',"transmission":' . transmission_api_conf($_POST);
			$result .= ',"smtp":' . email_api_conf($_POST);
			$result .= '}';
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
				if ($conf['rtn']=='200' || $conf['rtn']=='302')
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
			die(json_encode(array('rtn' => $conf['rtn'], 'error' => $msg)));
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
				$keywords = $_POST['keywords'];
			else
				$keywords = array();
			if (isset($_POST['serie_id']) and (int)$_POST['serie_id']>0)
			{
				$res = $TSW->setSerie($_POST['serie_id'],array('keywords' => $keywords));
				if ($res['rtn']!='200')
					die(json_encode(array('rtn' => $res['rtn'], 'error' => $res['error']	)));
				die(json_encode(array('rtn' => 200, 'error' => 'Keywords updated')));
			} else
			{
				$res = $TSW->setConf(json_encode(array('keywords' => $keywords)));
				if ($res['rtn']!='200')
					die(json_encode(array('rtn' => $res['rtn'], 'error' => $res['error']	)));
				die(json_encode(array('rtn' => 200, 'error' => 'Keywords updated')));
			}			
			break;

		case 'import_conf':
			if(isset($_FILES['configFile']))
			{ 
				 if(move_uploaded_file($_FILES['configFile']['tmp_name'], CONF_FILE))
				 {
					$rtn = '200';
					$msg =  'Upload of configuration file completed!';
				 }
				 else
				 {
					$rtn = '418';
					$msg =  'Failed to upload configuration file!';
				 }
			} 
			else
				$msg =  'Failed to upload configuration file due to missing file';
			die(json_encode(array('rtn' => $rtn, 'error' => $msg	)));
			break;

		case "getSeries":
			$load_tvdb = (isset($_GET['load_tvdb']) && $_GET['load_tvdb']==1) ? true : false;
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->getSeries($load_tvdb)));
			break;

		case "getSerie":
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->getSerie((int)$_POST['id'])));
			break;

		case "delSerie":
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->delSerie((int)$_POST['serie_id'])));
			break;

		case "addSerie":
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			die(json_encode($TSW->addSerie((int)$_POST['serie_id'])));
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
					$pattern = htmlentities($_POST['pattern']);
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
					} else
					{
						die(json_encode(array('rtn' => 499, 'error' => 'You must indicate both of Season and Episode numbers')));
					}
				} else
				{
					die(json_encode(array('rtn' => 499, 'error' => 'You must indicate both of Season and Episode numbers')));
				}

				$update = $TSW->setSerie($serie_id,array('season'=>$season,'episode'=>$episode,'pattern'=>$pattern,'expected'=>$val_episode['result']['firstaired']));
				if ($update['rtn'] != '200')
					die(json_encode(array('rtn' => $update['rtn'], 'error' => 'Error during TV Show update<br />'.$update['error'])));
				else
				{
					die(json_encode(array('rtn' => 200, 'error' => 'TV Show updated')));
				}
			break;

		case "addemail":
				if (!isset($_POST['serie_id']) or (int)$_POST['serie_id']==0)
					die(json_encode(array('rtn' => 499, 'error' => 'TV Show unfound')));
				if (!isset($_POST['email']) or $_POST['email']=='')
					die(json_encode(array('rtn' => 499, 'error' => 'Email blank')));

				$id = (int)$_POST['serie_id'];
				$email = htmlentities($_POST['email']);

				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
				$TSW->auth();
				$update = $TSW->addemail($id,$email);
				if ($update['rtn'] != '200')
					die(json_encode($update));
				else
				{
					die(json_encode(array('rtn' => 200, 'error' => 'TV Show updated')));
				}
				break;

		case "delemail":
				if (!isset($_POST['serie_id']) or (int)$_POST['serie_id']==0)
					die(json_encode(array('rtn' => 499, 'error' => 'TV Show unfound')));
				if (!isset($_POST['email']) or $_POST['email']=='')
					die(json_encode(array('rtn' => 499, 'error' => 'Email blank')));

				$id = (int)$_POST['serie_id'];
				$email = htmlentities($_POST['email']);

				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
				$TSW->auth();
				$update = $TSW->delemail($id,$email);
				if ($update['rtn'] != '200')
					die(json_encode($update));
				else
				{
					die(json_encode(array('rtn' => 200, 'error' => 'TV Show updated')));
				}
		case "reset_serie_keywords":
				if (!isset($_POST['serie_id']) or (int)$_POST['serie_id']==0)
					die(json_encode(array('rtn' => 499, 'error' => 'TV Show unfound')));
				$id = (int)$_POST['serie_id'];
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
				$TSW->auth();
				$update = $TSW->resetSerieKeywords($id);
				if ($update['rtn'] != '200')
					die(json_encode($update));
				else
				{
					die(json_encode(array('rtn' => 200, 'error' => 'Keywords updated')));
				}
				break;

		case "reset_all_keywords":
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
				$TSW->auth();
				$update = $TSW->resetAllKeywords();
				if ($update['rtn'] != '200')
					die(json_encode($update));
				else
				{
					die(json_encode(array('rtn' => 200, 'error' => 'Keywords updated for all TV shows')));
				}
				break;

		case "search":
				if (isset($_GET['pattern']))
					$pattern = $_GET['pattern'];
				if (!isset($pattern) or $pattern=='')
					die(json_encode(array('rtn' => 499, 'error' => 'TV Show unfound')));
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
				$TSW->auth();
				$result = $TSW->search($pattern);
				if ($result['rtn'] != '200')
					die(json_encode($result));
				else
				{
					die(json_encode($result));
				}
				break;

		case "pushTorrent":
				if (isset($_POST['serie_id']))
					$serie_id = $_POST['serie_id'];
				else
					die(json_encode(array('rtn' => 499, 'error' => 'TV Show unfound')));
				if(isset($_FILES['torrent']))
				{ 
					$destination = getcwd() . '/../' . TMP_DIR . '/' . $_FILES['torrent']['name'];
					if(move_uploaded_file($_FILES['torrent']['tmp_name'], $destination))
					{
						if (!isset($TSW))
							$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
						$TSW->auth();
						die(json_encode($TSW->push($serie_id,$destination)));
						
					}
				}	 
				else
				{
					die(json_encode(array('rtn' => 499, 'error' => 'Enable to upload file')));
				}
				break;

		case 'logs':
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			echo json_encode($TSW->logs());
			break;

		case 'get_arch':
			echo ARCH;
			break;

		case 'testRunning':
			try {
				if (!isset($TSW))
					$TSW = new TvShowWatch(API_FILE,CONF_FILE,SERIES_FILE,$debug);
			} catch (Exception $e)
			{
				die(json_encode(array('rtn' => $e->getCode(), 'error' => $e->getMessage())));
			}
			$TSW->auth();
			echo $TSW->testRunning();
			break;
		default:
	}
}

?>
