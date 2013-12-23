<?php if(!class_exists('raintpl')){exit;}?><form method="POST" action="<?php echo $form["action"];?>"<?php if( $form["enctype"] == 'file' ){ ?> enctype="multipart/form-data"<?php } ?> class="<?php echo $form["class"];?>"<?php if( $form["onsubmit"] != '' ){ ?> onsubmit="<?php echo $form["onsubmit"];?>"<?php } ?>>
<?php $content=$this->var['content']=$form["content"];?>

<?php $tpl = new RainTPL;$tpl_dir_temp = self::$tpl_dir;$tpl->assign( $this->var );$tpl->draw( dirname("content") . ( substr("content",-1,1) != "/" ? "/" : "" ) . basename("content") );?>

<?php if( $form["submit"]!='' ){ ?>

<div class="fieldDisplay">
<div class="col col1"></div><div class="col col2"><input type="submit" name="envoyer" value="<?php echo $form["submit"];?>" /></div>
</div>
<?php } ?>

</form>
