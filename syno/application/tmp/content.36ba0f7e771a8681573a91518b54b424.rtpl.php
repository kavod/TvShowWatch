<?php if(!class_exists('raintpl')){exit;}?><?php $counter1=-1; if( isset($content) && is_array($content) && sizeof($content) ) foreach( $content as $key1 => $value1 ){ $counter1++; ?>

<?php if( $value1["type"]=='h1' or $value1["type"]=='h2' ){ ?>

<?php $h1=$this->var['h1']=$value1;?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("h1") . ( substr("h1",-1,1) != "/" ? "/" : "" ) . basename("h1") );?>

<?php }elseif( $value1["type"]=='longtext' ){ ?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("longtext") . ( substr("longtext",-1,1) != "/" ? "/" : "" ) . basename("longtext") );?>

<?php }elseif( $value1["type"]=='banner' ){ ?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("banner") . ( substr("banner",-1,1) != "/" ? "/" : "" ) . basename("banner") );?>

<?php }elseif( $value1["type"]=='line' ){ ?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("line") . ( substr("line",-1,1) != "/" ? "/" : "" ) . basename("line") );?>

<?php }elseif( $value1["type"]=='iframe' ){ ?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("iframe") . ( substr("iframe",-1,1) != "/" ? "/" : "" ) . basename("iframe") );?>

<?php }elseif( $value1["type"]=='form' ){ ?>

<?php $form=$this->var['form']=$value1;?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->assign( "key", $key1 ); $tpl->assign( "value", $value1 );$tpl->draw( dirname("form") . ( substr("form",-1,1) != "/" ? "/" : "" ) . basename("form") );?>

<?php } ?>

<?php } ?>

