<?php if(!class_exists('raintpl')){exit;}?><?php if( $col["type"]=='text' ){ ?>

<?php if( $col["class"]!='' ){ ?><span class="<?php echo $col["class"];?>"><?php } ?>

<?php if( $col["href"]!='' ){ ?><a href="<?php echo $col["href"];?>"><?php } ?>

<?php echo $col["label"];?>

<?php if( $col["href"]!='' ){ ?></a><?php } ?>

<?php if( $col["mandatory"]==true ){ ?><span class="mandatory"> *</span><?php } ?>

<?php if( $col["class"]!='' ){ ?></span><?php } ?>

<?php if( $col["sublabel"]!='' ){ ?><br />
<?php if( $col["subclass"]!='' ){ ?><span class="<?php echo $col["subclass"];?>"><?php } ?>

<?php if( $col["subhref"]!='' ){ ?><a href="<?php echo $col["subhref"];?>"<?php if( $col["subonclick"]!='' ){ ?> onclick="<?php echo $col["subonclick"];?>"<?php } ?>><?php } ?>

<?php echo $col["sublabel"];?>

<?php if( $col["subhref"]!='' ){ ?></a><?php } ?>

<?php if( $col["subclass"]!='' ){ ?></span><?php } ?>

<?php } ?>

<?php }elseif( $col["type"] == 'episodechoice' ){ ?>

S<input type="text" name="<?php echo $col["s_name"];?>" id="<?php echo $col["s_id"];?>" value="<?php echo $col["season"];?>" class="episode" />E<input type="text" name="<?php echo $col["e_name"];?>" id="<?php echo $col["e_id"];?>" value="<?php echo $col["episode"];?>" class="episode" />
<?php }elseif( $col["type"] == 'submit' ){ ?>

<input type="submit" name="envoyer" value="<?php echo $col["label"];?>" />
<?php }elseif( substr($col["type"],0,6)=='input_' ){ ?>

<input type="<?php echo ( substr( $col["type"], 6 ) );?>"<?php if( $col["value"]!='' ){ ?> value="<?php echo $col["value"];?>"<?php } ?> name="<?php echo $col["name"];?>"<?php if( $col["onclick"]!='' ){ ?> onclick="<?php echo $col["onclick"];?>"<?php } ?> />
<?php }elseif( $col["type"] == 'select' ){ ?>

<select name="<?php echo $col["name"];?>"<?php if( $col["onchange"] != '' ){ ?> onchange="<?php echo $col["onchange"];?>"<?php } ?>>
<?php echo $selected = $col["value"];?>

<?php $counter1=-1; if( isset($col["choices"]) && is_array($col["choices"]) && sizeof($col["choices"]) ) foreach( $col["choices"] as $key1 => $value1 ){ $counter1++; ?>

<option value="<?php echo $value1["value"];?>"<?php if( $value1["value"] == $selected ){ ?> selected<?php } ?>><?php echo $value1["text"];?></option>
<?php } ?>

</select>
<?php } ?>

