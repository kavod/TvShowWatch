<?php if(!class_exists('raintpl')){exit;}?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title><?php echo $title;?></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="tpl/./styles.css" rel="stylesheet" type="text/css" />
<SCRIPT LANGUAGE=Javascript SRC="tpl/script.js"></SCRIPT>
</head>
<body>
<div id="header1">
	<p id="title"><?php echo $title;?></p>
</div>
<div id="header2">
	<ul class="rubs">
		<li><a href="index.php?page=home">Home</a></li>
		<li<?php if( $page == 'config' ){ ?> class="actif"<?php } ?>><a href="index.php?page=general_conf">General Conf</a></li>
		<li<?php if( $page == 'keywords' ){ ?> class="actif"<?php } ?>><a href="index.php?page=keywords">Keywords</a></li>
		<li<?php if( $page == 'series' ){ ?> class="actif"<?php } ?>><a href="index.php?page=series_list">Series List</a></li>
	</ul>
</div>
