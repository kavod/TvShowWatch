<?php if(!class_exists('raintpl')){exit;}?><?php $tpl = new RainTPL;if( $cache = $tpl->cache( $template = basename("header") ) )	echo $cache;else{	$tpl_dir_temp = self::$tpl_dir;	$tpl->assign( $this->var );	$tpl->draw( dirname("header") . ( substr("header",-1,1) != "/" ? "/" : "" ) . basename("header") );} ?>

<div class="contenu">
<?php if( isset($msg) ){ ?>

<div class="message"><?php echo $msg;?></div>
<?php } ?>

<?php if( isset($serieList) ){ ?>

<h1><?php echo $serieList["title"];?></h1>
<ul class="serielist">
<?php $counter1=-1; if( isset($serieList["list"]) && is_array($serieList["list"]) && sizeof($serieList["list"]) ) foreach( $serieList["list"] as $key1 => $value1 ){ $counter1++; ?>

<li><a href="index.php?page=serie_edit&id=<?php echo $value1["id"];?>"><?php echo $value1["seriename"];?></a></li>
<?php } ?>

</ul>
<?php } ?>

<?php $counter1=-1; if( isset($form) && is_array($form) && sizeof($form) ) foreach( $form as $key1 => $value1 ){ $counter1++; ?>

	<form method="POST" action="<?php echo $value1["action"];?>" enctype="multipart/form-data" class="myForm" onSubmit="return validateForm(this)">
		<h1><?php echo $value1["title"];?></h1>
<?php $counter2=-1; if( isset($value1["part"]) && is_array($value1["part"]) && sizeof($value1["part"]) ) foreach( $value1["part"] as $key2 => $value2 ){ $counter2++; ?>

		<h2><?php echo $value2["title"];?></h2>
<?php $counter3=-1; if( isset($value2["champs"]) && is_array($value2["champs"]) && sizeof($value2["champs"]) ) foreach( $value2["champs"] as $key3 => $value3 ){ $counter3++; ?>

		<div class="<?php if( $value3["visible"] === false ){ ?>fieldHidden<?php }else{ ?>fieldDisplay<?php } ?>" id="<?php echo $value3["field_id"];?>">
			<div class="label"><?php echo $value3["label"];?>: <?php if( $value3["mandatory"] == true ){ ?><span class="mandatory"> *</span><?php } ?></div><div class="champs">
<?php if( $value3["type"] == 'text' ){ ?>

<input type="text" name="<?php echo $value3["field_id"];?>" value="<?php echo $value3["value"];?>" />
<?php }elseif( $value3["type"] == 'password' ){ ?>

<input type="password" name="<?php echo $value3["field_id"];?>" value="<?php echo $value3["value"];?>" />
<?php }elseif( $value3["type"] == 'file' ){ ?>

<input type="file" name="<?php echo $value3["field_id"];?>" />
<?php }elseif( $value3["type"] == 'list' ){ ?>

<select name="<?php echo $value3["field_id"];?>"<?php if( $value3["onChange"] != '' ){ ?> onChange="<?php echo $value3["onChange"];?>"<?php } ?>>
<?php echo $selected = $value3["value"];?>

<?php $counter4=-1; if( isset($value3["choices"]) && is_array($value3["choices"]) && sizeof($value3["choices"]) ) foreach( $value3["choices"] as $key4 => $value4 ){ $counter4++; ?>

<option value="<?php echo $value4["id"];?>"<?php if( $value4["id"] == $selected ){ ?> selected<?php } ?>><?php echo $value4["label"];?></option>
<?php } ?>

</select>
<?php } ?>

</div><br /></div>
<?php } ?>

<br />
<?php } ?>


		<input type="submit" name="envoyer" value="Submit">
	</form>
<?php } ?>

</div>
</body>
</html>
