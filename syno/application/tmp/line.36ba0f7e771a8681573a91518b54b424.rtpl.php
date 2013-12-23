<?php if(!class_exists('raintpl')){exit;}?><div class="<?php if( $value["visible"] === false ){ ?>fieldHidden<?php }else{ ?>fieldDisplay<?php } ?>"<?php if( $value["id"] != '' ){ ?> id="<?php echo $value["id"];?>"<?php } ?>>
<?php if( isset($value["col1"]) ){ ?>

<div class="col col1">
<?php $col=$this->var['col']=$value["col1"];?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("col") . ( substr("col",-1,1) != "/" ? "/" : "" ) . basename("col") );?>

</div>
<?php } ?>

<?php if( isset($value["col2"]) ){ ?>

<?php $col=$this->var['col']=$value["col2"];?>

<div class="col col2">
<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("col") . ( substr("col",-1,1) != "/" ? "/" : "" ) . basename("col") );?>

</div>
<?php } ?>

<?php if( isset($value["col3"]) ){ ?>

<?php $col=$this->var['col']=$value["col3"];?>

<div class="col col3">
<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("col") . ( substr("col",-1,1) != "/" ? "/" : "" ) . basename("col") );?>

</div>
<?php } ?>

</div>
