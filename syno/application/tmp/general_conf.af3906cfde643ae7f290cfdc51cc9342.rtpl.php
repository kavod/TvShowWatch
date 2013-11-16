<?php if(!class_exists('raintpl')){exit;}?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
<title><?php echo $title;?></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link href="tpl/styles.css" rel="stylesheet" type="text/css" />
<SCRIPT LANGUAGE=Javascript SRC="tpl/script.js"></SCRIPT>
</head>
<body>
<div id="header1">
	<p id="title"><?php echo $title;?></p>
</div>
<div id="header2">
	<ul class="rubs">
		<li><a href="general_conf.php?page=home">Home</a></li>
		<li><a href="general_conf.php?page=general_conf">General Conf</a></li>
		<li><a href="general_conf.php?page=series_list">Series List</a></li>
	</ul>
</div>
<div class="contenu">

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

<input type="password" name="<?php echo $value3["field_id"];?>" />
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
