<?
error_reporting(E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

define("TVDB_PY_FILE", '/var/packages/TvShowWatch/target/myTvDB.py');
define("PYTHON_EXEC", 'PATH=/var/packages/python/target/bin:$PATH ; python');
define("LOGFILE", '/var/log/TSW.log');

class TvDB
{
	var $py_file;
	var $cmd;

	function TvDB($debug = false)
	{
		$this->debug = ($debug != false);
		if (!file_exists(TVDB_PY_FILE))
		{
			trigger_error("Python file " . TVDB_PY_FILE . " does not exist");
			return false;
		}
		$this->py_file = TVDB_PY_FILE;
		$this->cmd = $this->py_file;
	}


	function getSerie($serie_id)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action getSerie -n "' . ((int)$serie_id) . '"';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}

	function getEpisodes($serie_id)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action getEpisodes -n "' . ((int)$serie_id) . '"';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return array('episodes' => json_decode($result[0],true));
	}
	function getEpisode($id, $season, $episode, $lang)
	{
		$cmd = PYTHON_EXEC . " " . $this->cmd .' --action getEpisode -n "' . ((int)$id) . ',' . ((int)$season) . ',' . ((int)$episode) . '"';
		exec($cmd,$result);
		if ($this->debug)
		{
			echo $cmd.'<br />';
			print_r($result);
		}
		return json_decode($result[0],true);
	}
}

//$t = new TvDB(TVDB_PY_FILE,true);
//print_r($t->getSerie(75760));
//print_r($t->getEpisodes(75760));
//print_r($t->getEpisode(75760,1,1,'en'));
?>
