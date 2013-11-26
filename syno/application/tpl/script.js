<!-- 
function visiField(fields,value)
{
	for (var i=0;i<fields.length;i++)
	{
		document.getElementById(fields[i]).className=value;
	}
}
function validateForm(form)
{
	for(var i=0;i<form.childNodes.length;i++)
	{
		if (form.childNodes[i].className=='fieldDisplay')
		{
			if (form.childNodes[i].getElementsByTagName('input').length>0)
			{
				if (form.childNodes[i].getElementsByClassName("label")[0].getElementsByClassName("mandatory").length>0)
					if (form.childNodes[i].getElementsByTagName('input')[0].value=='')
					{
						alert("Populate all mandatory fields");
						return false;
					}
			}
		}
	}
}

function set_last(eleSeason,eleEpisode,valSeason,valEpisode)
{
	eleSeason.value=valSeason;
	eleEpisode.value=valEpisode;
	return false;
}
// -->
