<?php
$xmlDoc=new DOMDocument();
$xmlDoc->load("http://thetvdb.com/api/GetSeries.php?seriesname=".$_GET['q']);

$x=$xmlDoc->getElementsByTagName('Data')->item(0)->getElementsByTagName('Series');

//get the q parameter from URL
$q=$_GET["q"];

//lookup all links from the xml file if length of q>0
if (strlen($q)>0)
{
$hint="";
for($i=0; $i<($x->length); $i++)
  {
  $y=$x->item($i)->getElementsByTagName('SeriesName')->item(0)->nodeValue;
  $annee = $x->item($i)->getElementsByTagName('FirstAired')->item(0)->nodeValue;
  $label = $y . ' ('.substr($annee,0,4) . ')';
  $z="http://thetvdb.com/banners/" . $x->item($i)->getElementsByTagName('banner')->item(0)->nodeValue;

      if ($hint=="")
        {
        $hint="<a href='" . 
        $z . 
        "' target='_blank'>" . 
        $label . "</a>";
        }
      else
        {
        $hint=$hint . "<br /><a href='" . 
        $z . 
        "' target='_blank'>" . 
        $label . "</a>";
        }
  }
}

// Set output to "no suggestion" if no hint were found
// or to the correct values
if ($hint=="")
  {
  $response="no suggestion";
  }
else
  {
  $response=$hint;
  }

//output the response
echo $response;
?>
