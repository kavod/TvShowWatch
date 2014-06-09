<?
error_reporting(E_ALL | E_STRICT);  
ini_set('display_startup_errors',1);  
ini_set('display_errors',1);

if (!isset($path))
	$path = '../';

include $path . "inc/rain.tpl.class.php"; //include Rain TPL

raintpl::$tpl_dir = $path."tpl/"; // template directory
raintpl::$cache_dir = $path."tmp/"; // cache directory

$tpl = new raintpl(); //include Rain TPL
echo $_POST['data'];
$data = json_decode($_POST['data']);
foreach($data as $key => $val)
	$tpl->assign( $key, $val);
$tpl->draw( $_POST['page'] ); // draw the template
print_r($data);
?>
