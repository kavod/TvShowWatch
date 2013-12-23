<?php if(!class_exists('raintpl')){exit;}?><?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("header") . ( substr("header",-1,1) != "/" ? "/" : "" ) . basename("header") );?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("content") . ( substr("content",-1,1) != "/" ? "/" : "" ) . basename("content") );?>

<?php $tpl = new RainTPL;if( $cache = $tpl->cache( $template = basename("footer") ) )	echo $cache;else{	$tpl_dir_temp = self::$tpl_dir;	$tpl->assign( $this->var );	$tpl->draw( dirname("footer") . ( substr("footer",-1,1) != "/" ? "/" : "" ) . basename("footer") );} ?>

