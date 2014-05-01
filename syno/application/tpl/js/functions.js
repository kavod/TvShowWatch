function serieStatus(status_id)
{
	switch(parseInt(status_id))
	{
		case 10:
			return 'Waiting for broadcast';
		case 20:
			return 'Waiting for torrent availability';
		case 30:
			return 'Download in progress';
		default:
			return 'Unknown status';
	}
}
	var apply_jcss = function() 
	{
		// Serie List content
		get_serielist();

		// Serie detail content
		load_serieData();

		// Tab management
		$( "#tabs" ).tabs( "refresh" );

		// General design
		$( "button" ).button();
		$( 'input[type="submit"]' ).button();
	}

	var conf_ok = function() {
	  $( "#tabs" ).tabs("enable", 2 );
	  $("#tab_keywords").attr("title", "");
	  $( "#tabs" ).tabs("enable", 3 );
	  $("#tab_series").attr("title", "");
	}

	var conf_ko = function() {
	  $( "#tabs" ).tabs( "disable", 2 );
	  $("#tab_keywords").attr("title", "Configuration must be completed before");
	  $( "#tabs" ).tabs( "disable", 3 );
	  $("#tab_series").attr("title", "Configuration must be completed before");
		$("span.ui-icon-close").click();
	}
// actual addTab function: adds new tab using the input from the form above
    function addTab(tabTitle,id) 
	{
		var tabs = $('#tabs');
		var found = false;
		var label = tabTitle || "Tab " + tabCounter,
        li = $( tabTemplate.replace( /#\{href\}/g, "#s" + id ).replace( /#\{label\}/g, label ) );
        //var tabContentHtml = tabContent || "Tab " + tabCounter + " content.";

		for (i in opened_tabs)
		{
			if (opened_tabs[i] == id)
			{
				found = true;
				break;
			}
		}
		if (!found)
		{
			opened_tabs.push(id);
			tabs.find( ".ui-tabs-nav" ).append( li );
			tabs.append( "<section id='s" + id + "'></section>");

			$('#s' + id).load('serie.html', function() 
			{
				$('#s' + id).html($('#s' + id).html().replace("###",id));
				$.post( "email_list2.php", {"id":id})
				.done(function( data ) 
				{
					$('#s' + id +' .emails').html(data);
				});
				apply_jcss();
				$( "#tabs" ).tabs("option", "active", tabCounter);
				tabCounter++;
			});
		}
    }

	function run() 
	{
		var jqxhr = $.get( "api/TvShowWatch.php?action=run", function() {
		  show_info("Successfully run");
			//alert( "success" );
		});
	}
	function closeTab(element) 
	{
		var tabs = $('#tabs');
		var panelId = element.remove().attr( "aria-controls" );
		panelId = panelId.substring(1);
		$( "#" + panelId).remove();
		tabs.tabs( "refresh" );
		tabCounter--;
		for (i in opened_tabs)
		{
			if (opened_tabs[i] == panelId)
			{
				delete opened_tabs[i];
				break;
			}
		}
	}
function email_activation() {
          if ($("#smtp_enable").val() != '1')
              $(".smtp_required div input,.smtp_required div select").attr("disabled", "disabled");
          else
              $(".smtp_required div input,.smtp_required div select").removeAttr("disabled");
      }
	function start_loading() {
		$('#blocker').fadeIn(10);
		$('#loading').fadeIn(10);
	}

	function stop_loading() {
		$('#blocker').fadeOut(300);
		$('#loading').fadeOut(300);
	}

	function save_conf(event) 
	{
		start_loading();
		// Stop form from submitting normally
		event.preventDefault();
		var data = $('#param').serialize();
		$.post( "api/TvShowWatch.php?action=save_conf", data)
		.done(function( data ) 
		{
			show_info(data);
			//alert(data);
			stop_loading();
		});
		return false;
	}

	function import_conf(event) {
		start_loading();
		event.preventDefault();
		formdata = new FormData();
		formdata.append('configFile', $('#configFile')[0].files[0]);
		$.ajax({  
			type: "POST", 
			url: "api/TvShowWatch.php?action=import_conf",  
			data: formdata,
			contentType: false,
			processData: false 
		})
		.done(function( data )  
		{  
			show_info(data)
			//alert( data );  
			get_conf();
			stop_loading();
		});
		return false;
	}

	function get_conf(event)
	{
		$.ajax({  
			type: "GET", 
			url: "api/TvShowWatch.php?action=get_conf"
		})
		.done(function( data )  
		{
			result = JSON.parse(data);
			if (result.rtn != 200)
			{
				show_error(result.error);
			} else
			{
				result = result.result;
				formdata = {};
				formdata.tracker_id = 't411';
				formdata.tracker_username = result.tracker.user;
				formdata.tracker_password = (result.tracker.password == "****") ? 'initial' : '';
				formdata.trans_server = result.transmission.server;
				formdata.trans_port = result.transmission.port;
				formdata.trans_username = result.transmission.user;
				formdata.trans_password = (result.transmission.password == "****") ? 'initial' : '';
				formdata.trans_slotNumber = result.transmission.slotNumber;
				formdata.trans_folder = result.transmission.folder;
				formdata.smtp_enable = (result.smtp.server=='') ? 0 : 1;
				formdata.smtp_server = result.smtp.server;
				formdata.smtp_port = result.smtp.port;
				formdata.smtp_ssltls = (result.smtp.ssltls!=true) ? 0 : 1;
				formdata.smtp_username = result.smtp.user;
				formdata.smtp_password = (result.smtp.password == "****") ? 'initial' : '';
				formdata.smtp_emailSender = result.smtp.emailSender;
				populate('#param',formdata);
				email_activation();
			}
		});
	}

	function populate(frm, data) {   
		$.each(data, function(key, value){  
		var $ctrl = $('[name='+key+']', frm);
		switch($ctrl.attr("type"))  
		{  
		    case "text" :   
		    case "hidden":  
		    case "textarea":
		    case "password":
			case "number":
			case "email":
		    $ctrl.val(value);   
		    break;   
		    case "radio" : 
			case "checkbox":   
		    $ctrl.each(function(){
		       if($(this).attr('value') == value) {  $(this).attr("checked",value); } });   
		    break;    
		}
		if ($ctrl.is('select'))
		{
		    $ctrl.children('option').each(function(){
		    if($(this).attr('value') == value) {  $(this).attr("selected", "selected")	; } });   
		}  
		});  
	}

	function show_info(msg)
	{
		$( "#info_box" ).show( 'fold', 500 );
		$( "#info_content" ).text(msg);
		setTimeout(function(){
			
			$( "#info_box" ).hide( 'fold', 500 );
		},10000);
	}

	function show_error(msg)
	{
		$( "#error_box" ).show( 'fold', 500 );
		$( "#error_content" ).text(msg);
		setTimeout(function(){
			$( "#error_box" ).hide( 'fold', 500 );
		},8000);
	}

	function save_keywords()
	{
		//start_loading();
		var keywords = [];
		$( "#keywords_list" ).children('li:not(.ui-state-disabled)').each(function()
		{
			keywords.push($(this).html());
		});
		data = {"keywords":keywords};
		$.post( "api/TvShowWatch.php?action=save_keywords", data)
		.done(function( result ) 
		{
			data = JSON.parse(result);
			if (data.rtn != '200')
				show_error(data.error);
			else
				show_info('Keywords updated');
			//stop_loading();
		});
	}

	function add_keyword(e)
	{
		e.preventDefault();
		var text = $("input[name='keywords_new']").val();
		var $li = $("<li class='ui-state-default'/>").text(text);
		$li.attr('title',text);
		$("input[name='keywords_new']").val('');
		$("#keywords_list>.ui-state-disabled:first").before($li);
		$("#keywords_list").sortable('refresh');
		save_keywords();
	}

	function load_serieData()
	{
		$.ajax({  
			type: "GET", 
			url: "api/TvShowWatch.php?action=getSeries"
		})
		.done(function( data )  
		{
			result = JSON.parse(data);
			if (result.rtn != 200)
			{
				show_error(result.error);
			} else
			{
				result = result.result;
				for (sid in opened_tabs)
				{
					for (serie in result)
					{
						if (parseInt(opened_tabs[sid]) == parseInt(result[serie].id))
						{
							$('#s' + opened_tabs[sid] + '>h1').text(result[serie].name);
							$('#s' + opened_tabs[sid] + '>.banner>img').attr('src',result[serie].tvdb.banner.replace("banners/graphical","banners/_cache/graphical"));
							$('#s' + opened_tabs[sid] + '>.description').text(result[serie].tvdb.overview);
							$('#s' + opened_tabs[sid] + '>.serie_status').text(serieStatus(result[serie].status));
							season_selector = '#s' + opened_tabs[sid] + '>.episode_form>input[name="season"]';
							episode_selector = '#s' + opened_tabs[sid] + '>.episode_form>input[name="episode"]';
							$(season_selector).val(result[serie].season);
							$(episode_selector).val(result[serie].episode);
							format_2digits(season_selector);
							format_2digits(episode_selector);
							var proxy = $.proxy(check_episode,null,opened_tabs[sid]);
							$(season_selector).change(proxy);
							$(episode_selector).change(proxy);
							$('#s' + opened_tabs[sid] + '>.episode_form').submit($.proxy(set_episode,null,opened_tabs[sid]));
							$('#s' + opened_tabs[sid] + '>.episode_form>.retrieve').click($.proxy(retrieve_episode,null,opened_tabs[sid],result[serie].nextEpisode.seasonnumber,result[serie].nextEpisode.episodenumber));
							$('#s' + opened_tabs[sid] + '>.unschedule').click($.proxy(unschedule,null,opened_tabs[sid]));
						}
					}
				}
			}
		});	
	}

	function check_episode(sid)
	{
		event.preventDefault();
		var data = $('#s' + sid + '>.episode_form').serialize();
		$.post( "api/TvShowWatch.php?action=getEpisode", data)
		.done(function( data )  
		{
			season_selector = '#s' + sid + '>.episode_form>input[name="season"]';
			episode_selector = '#s' + sid + '>.episode_form>input[name="episode"]';
			format_2digits(season_selector);
			format_2digits(episode_selector);
			result = JSON.parse(data);
			if (result.rtn != 200)
			{
				show_error(result.error);
				$(season_selector).css('background-color','#fea339');
				$(episode_selector).css('background-color','#fea339');
			} else
			{
				$( "#error_box" ).hide( 'fold', 500 );
				$(season_selector).css('background-color','#ffffff');
				$(episode_selector).css('background-color','#ffffff');
			}
		});
	}

	function format_2digits(field_selector)
	{
		field = $(field_selector);
		if (parseInt(field.val()) < 10)
			field.val('0'+parseInt(field.val()))	
	}

	function set_episode(sid)
	{
		event.preventDefault();
		var data = $('#s' + sid + '>.episode_form').serialize();
		
		$.post( "api/TvShowWatch.php?action=setSerie", data)
		.done(function( data )  
		{
			result = JSON.parse(data);
			show_info(result.error);
		});
	}


	function retrieve_episode(sid,seasonnumber,episodenumber)
	{
		season_selector = '#s' + sid + '>.episode_form>input[name="season"]';
		episode_selector = '#s' + sid + '>.episode_form>input[name="episode"]';
		$(season_selector).val(seasonnumber);
		$(episode_selector).val(episodenumber);
		format_2digits(season_selector);
		format_2digits(episode_selector);
	}

	function addSerie()
	{
		event.preventDefault();
		var data = $('#addSerie').serialize();
		var serie_id = $('#addSerie input[name="serie_id"]').val();
		$.post( "api/TvShowWatch.php?action=addSerie", data)
		.done(function( data )  
		{
			result = JSON.parse(data);
			if (result.rtn != 200)
			{
				show_error(result.error);
			}
			else
			{
				serie_id = $('#addSerie input[name="serie_id"]').val();
				$('#addSerie input[name="serie_id"]').val('');
				data = {
						"page":"serie_line",
						"data":JSON.stringify({'series':[{
								'series_id': serie_id,
								}]})
						};
				get_serielist(serie_id);
				//addTab(tabTitle,id);
				show_info(result.error);
			}
		});
	}

	function get_serielist(sid)
	{
		$("#serielist").load('series_list2.php', sid, function(){
			$("a[id^='serie_']").click(function() {
				tabTitle = $(this).text();
				id = $(this).attr('id').substring(6);
				addTab(tabTitle,id);
				return false;
			});
			if (typeof sid !== 'undefined')
			{
				$("#serie_"+sid).click();
			}
		});
	}

	function unschedule(sid)
	{
		event.preventDefault();
		var data = {"serie_id": sid};
		
		$.post( "api/TvShowWatch.php?action=delSerie", data)
		.done(function( data )  
		{
			get_serielist();			
			element = $( "#tabs>nav" ).find( ".ui-tabs-active" );
			closeTab(element);
			result = JSON.parse(data);
			show_info(result.error);
		});
	}
