// Load functions
function load_logs()
{
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=logs"
	})
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
		{
			logs = [];
			result.result.forEach(function(log_entry)
			{
				logs.push({
						datetime:	log_entry.datetime,
						name:		log_entry.seriesname,
						rtn:		log_entry.rtn,
						msg:		log_entry.msg,
						season:		log_entry.season,
						episode: 	log_entry.episode
						});
			});

			$("#list4").jqGrid({
				datatype: "local",
				height: 345,
				width: 700,
				rowNum:15,
			   	colNames:['Date', 'TVShow', 'Season','Episode','ResCd','Message'],
			   	colModel:[
			   		{name:'datetime',index:'datetime', width:110, sorttype:"date", formatter:"date", formatoptions:{srcformat:'ISO8601Long', newformat:"Y-m-d H:i:s"}},
			   		{name:'name',index:'name', width:150},
			   		{name:'season',index:'season', width:50, align:"center",sorttype:"number"},
			   		{name:'episode',index:'episode', width:50, align:"center",sorttype:"number"},		
			   		{name:'rtn',index:'rtn', width:55,align:"center",sorttype:"number"},		
			   		{name:'msg',index:'msg', sortable:false}		
			   	],
				sortname: 'datetime',
				sortorder: 'desc',
			   	caption: "TvShowWatch logs entries",
				hidegrid: false,
				viewrecords: true,
				recordtext: "View {0} - {1} of {2}",
				loadtext: "Loading...",
				pager: "#pager5",
				data: logs
			});
			jQuery("#list4").jqGrid('filterToolbar',{searchOperators : false});
		}
	});
}

function load_keywords(keywords)
{
	for (key in keywords)
	{
		new_li = '<li class="keyword ui-state-default" title="'+keywords[key]+'" id="keyword-' + key + '">'+keywords[key]+'</li>';
		$(new_li).insertBefore( "#add_new_keyword" );
	}
}


function get_conf(event)
{
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=get_conf"
	})
	.done(function( data )  
	{
		get_arch();
		result = compute_data(data);
		if (result.ok)
		{
			conf_ok();
			result = result.result;
			formdata = {};
			formdata.tracker_id = result.tracker.id;
			formdata.tracker_username = result.tracker.user;
			formdata.tracker_password = (result.tracker.password == "****") ? 'initial' : '';
			formdata.trans_server = result.transmission.server;
			formdata.trans_port = result.transmission.port;
			formdata.trans_username = result.transmission.user;
			formdata.trans_password = (result.transmission.password == "****") ? 'initial' : '';
			formdata.trans_slotNumber = result.transmission.slotNumber;
			formdata.trans_folder = result.transmission.folder;
			formdata.smtp_enable = (typeof result.smtp.server === 'undefined' || result.smtp.server=='') ? 0 : 1;
			formdata.smtp_server = result.smtp.server;
			formdata.smtp_port = result.smtp.port;
			formdata.smtp_ssltls = (result.smtp.ssltls!=true) ? 0 : 1;
			formdata.smtp_username = result.smtp.user;
			formdata.smtp_password = (result.smtp.password == "****") ? 'initial' : '';
			formdata.smtp_emailSender = result.smtp.emailSender;
			populate('#param',formdata);
			load_tracker_conf(event,$('#tracker_id option[value='+result.tracker.id+']').attr('login'));
			load_keywords(result.keywords);
			email_activation();
		} else
		{
			conf_ko();
		}
	});
}

function get_arch()
{
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=get_arch"
	})
	.done(function( data )  
	{
		$('#arch').text(data);
	});
}

function testRunning()
{
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=testRunning"
	})
	.done(function( data )  
	{
		$('#testRunning').text(data);
	});
}

function get_serielist()
{
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=getSeries&load_tvdb=0"
	})
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
		{
			series_data = result.result;
			header = $("#serielist tr:first-child");
			$("#serielist").html('');
			$("#serielist").append(header);
			for (serie_id in series_data)
			{
				serie = series_data[serie_id];
				
				series_episode = "S" 
					+ ((serie.season < 10) ? "0"+serie.season : serie.season)
					+ "E"
					+ ((serie.episode < 10) ? "0"+serie.episode : serie.episode);

				var d = new Date(Date.parse(serie.expected));

				if($("#serie_line_" + serie.id).length == 0) 
				{
					tr = $('<tr></tr>');
					tr.attr('id','serie_line_' + serie.id);
					tr.attr('class',"serie_line");
					$("#serielist").append(tr);
				} else
				{
					$("#serie_line_" + serie.id).html('');
				}

				link = $('<a></a>')
					.attr('id',"serie_" + serie.id)
					.attr('href','#')
					.html(serie["name"])
					.click(function() {
							tabTitle = $(this).text();
							id = $(this).attr('id').substring(6);
							addTab(tabTitle,id);
							return false;
						});
				td = $('<td></td>')
					.addClass('td_tvshow');
				td.append(link);
				$("#serie_line_" + serie.id).append(td);

				td = $('<td></td>')
					.addClass('td_episode')
					.html(series_episode);
				$("#serie_line_" + serie.id).append(td);

				td = $('<td></td>')
					.addClass('td_status')
					.html(serieStatus(serie.status));
				$("#serie_line_" + serie.id).append(td);

				td = $('<td></td>')
					.addClass('td_expected')
					.html(d.toLocaleDateString());
				$("#serie_line_" + serie.id).append(td);
			}
		}
		loading_in_progress = true;
		$.ajax({  
			type: "GET", 
			url: "api/TvShowWatch.php?action=getSeries&load_tvdb=1"
		})
		.done(function( data )  
		{		
			result = compute_data(data);
			if (result.ok)
			{
				series_data = result.result; 
				load_serieData();
				loading_in_progress = false;
			}
		});
	});
}

function check_update(event)
{
	if (serie_time == "0")
	{
		initial_update = true;
		start_loading();
	}
	if (serie_time != event.data)
	{
		serie_time = event.data;
		get_serielist();
		if (initial_update)
			stop_loading();
	}
}

function load_email(id)
{
	$.post( "email_list2.php", {"id":id})
	.done(function( data ) 
	{
		$('#s' + id +' .emails').html(data);
		$('#s' + id +' .emails>li>div>.ui-icon-circle-close').click($.proxy(del_email,null,id,this));
	});
}

function load_serie_keywords(id)
{
	$.post( "keyword_list2.php", {"id":id})
	.done(function( data ) 
	{
		$('#keywords_list' + id).html(data);
		$( "#keywords_list" + id ).sortable({
			placeholder: "ui-state-highlight",
			distance: 15,
			items: "li:not(.ui-state-disabled)",
			axis: "y",
			stop: save_serie_keywords
		});
		$( "#keywords_list" +id ).disableSelection();
		$("#trash" +id ).droppable({
			accept: "#keywords_list" + id + " li",
			hoverClass: "ui-state-hover",
			drop: function(ev, ui) {
				ui.draggable.remove();
			}
		});
		$( "#keyword_add"+id ).submit(event, add_serie_keyword);
		$( "#keywords"+id +">.resetKeywords").click(reset_serie_keywords);
	});
}

function load_serieData()
{
	/*start_loading()
	$.ajax({  
		type: "GET", 
		url: "api/TvShowWatch.php?action=getSeries&load_tvdb=1"
	})
	.done(function( data )  
	{		
		result = compute_data(data);
		if (result.ok)
		{
			result = result.result;*/

			result = series_data;
			for (sid in opened_tabs)
			{
				var tabs = $( "#tabs_serie_" + opened_tabs[sid] ).tabs();
				serie_found = false;
				for (serie in result)
				{
					if (parseInt(opened_tabs[sid]) == parseInt(result[serie].id))
					{
						serie_found = true;
						$('#s' + opened_tabs[sid] + '>h1').text(result[serie].name);
						if (typeof(result[serie].tvdb.banner) != 'undefined')
							$('#s' + opened_tabs[sid] + '>.banner>img').attr('src',result[serie].tvdb.banner.replace("banners/graphical","banners/_cache/graphical"));
						$('#s' + opened_tabs[sid] + '>.description').text(result[serie].tvdb.overview);
						$('#data' + opened_tabs[sid] + '>.serie_status').text(serieStatus(result[serie].status));
						season_selector = '#data' + opened_tabs[sid] + '>.episode_form>input[name="season"]';
						episode_selector = '#data' + opened_tabs[sid] + '>.episode_form>input[name="episode"]';
						episode_label = '#current_episode' + opened_tabs[sid];
						pattern_field = '#data' + opened_tabs[sid] + '>.episode_form>input[name="pattern"]';
						emails_selector = '#emails_' + opened_tabs[sid];

						season = (result[serie].season > 9) ? result[serie].season : '0' + result[serie].season;
						episode = (result[serie].episode > 9) ? result[serie].episode : '0' + result[serie].episode;
						$(season_selector).val(season);
						$(episode_selector).val(episode);
						$(episode_label).text('S' + season + 'E' + episode);
						format_2digits(season_selector);
						format_2digits(episode_selector);
						$(pattern_field).val(result[serie].pattern);
						emails = result[serie].emails;

						switch(result[serie].status)
						{
							case 10:
							case 15:
							case 20:
							case 21:
								break;
							case 30:
							case 90:
							default:
								$("#tab_push" + opened_tabs[sid]).attr("title", serieStatus(result[serie].status));
								$( "#tabs_serie_" + opened_tabs[sid] ).tabs( "disable", 3 );
								break;
						}

						for (key in emails)
						{
							email = emails[key];
							li = $('<li></li>')
								.attr('id','email_' + opened_tabs[sid] + '_' + key);
							node = $('<label></label>').html('Emails '+(parseInt(key)+1));
							li.append(node);
							node = $('<span></span>').addClass('email').html(email);
							li.append(node);

							span = $('<span></span>')
								.addClass("ui-icon ui-icon-circle-close")
								.attr('title',"Remove email")
								.attr('email',email)
								.click($.proxy(del_email,null,opened_tabs[sid],this));
						
							node = $('<div></div>')
								.attr("style","display:inline-block");
							node.append(span);
							li.append(node);
							$(emails_selector).append(li);
						}

						var proxy = $.proxy(check_episode,null,opened_tabs[sid]);
						$(season_selector).change(proxy);
						$(episode_selector).change(proxy);
						$('#data' + opened_tabs[sid] + '>.episode_form').submit($.proxy(set_episode,null,opened_tabs[sid]));
						$('#push' + opened_tabs[sid] + '>form').submit($.proxy(push_torrent,$('#push' + opened_tabs[sid] + '>form'),opened_tabs[sid]));
						if (result[serie].nextEpisode === null)
						{
							$('#data' + opened_tabs[sid] + '>.episode_form>.retrieve').button("option","disabled",true);
							$('#data' + opened_tabs[sid] + '>.episode_form>.retrieve').button("option","label","last episode reached");
						} else
						{
							$('#data' + opened_tabs[sid] + '>.episode_form>.retrieve').click($.proxy(retrieve_episode,null,opened_tabs[sid],result[serie].nextEpisode.seasonnumber,result[serie].nextEpisode.episodenumber));
						}
						$('#data' + opened_tabs[sid] + '>.unschedule').click($.proxy(unschedule,null,opened_tabs[sid]));
						$('#emails' + opened_tabs[sid] + '>.email_add').submit($.proxy(add_email,null,opened_tabs[sid]));
						
					}
				}
				if (!serie_found)
				{
					closeTab($( "#tabs>nav" ).find( "li[aria-controls='s"+ opened_tabs[sid] +"']" ));
				}
			}/*
		}
		stop_loading()
	});*/	
}

/*function get_serielist(sid)
{
	return true;
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
}*/

function load_tracker_conf(event,login)
{
	login = typeof login !== 'undefined' ? login : -1;
	// Hide or show login fields if selected tracker requires
	if(login == 1 || (login == -1 && $('#tracker_id option:selected').attr('login') == 1))
	{
			$('#tracker_login').show('highlight');
			$('#tracker_login input').prop('required',true);
	} else
	{
			$('#tracker_login').hide('highlight');
			$('#tracker_login input').prop('required',false);
	}
}

function serieStatus(status_id)
{
	switch(parseInt(status_id))
	{
		case 10:
			return 'Waiting for broadcast';
		case 15:
			return 'Torrent search scheduled';
		case 20:
			return 'Waiting for torrent availability';
		case 21:
			return 'No tracker configured';
		case 30:
			return 'Download in progress';
		case 90:
			return 'Broadcast achieved';
		default:
			return 'Unknown status';
	}
}



function apply_jcss() 
{
	// Tab management
	$( "#tabs" ).tabs( "refresh" );

	// General design
	$( "button" ).button();
	$( 'input[type="submit"]' ).button();

	// Serie List content
	//get_serielist();

	// Serie detail content
	load_serieData();

	// Load logs
	load_logs();
}

// Tabs management
function conf_ok() 
{
	$( "#tabs" ).tabs("enable", 2 );
	$("#tab_keywords").attr("title", "");
	$( "#tabs" ).tabs("enable", 3 );
	$("#tab_series").attr("title", "");
	$( "#tabs" ).tabs("enable", 4 );
	$("#tab_series").attr("title", "");

	$('#conf_status').text('OK')
		.addClass('OK')
		.removeClass('mandatory');
	testRunning();
}

function conf_ko() {
	$( "#tabs" ).tabs( "disable", 2 );
	$("#tab_keywords").attr("title", "Configuration must be completed before");
	$( "#tabs" ).tabs( "disable", 3 );
	$("#tab_series").attr("title", "Configuration must be completed before");
	$( "#tabs" ).tabs( "disable", 4 );
	$("#tab_series").attr("title", "Configuration must be completed before");
	$("span.ui-icon-close").click();

	$('#conf_status').text('Fail')
		.removeClass('OK')
		.addClass('mandatory');
	$('#testRunning').text('Not configured');
}

function check_loading_in_progress()
{
	if(loading_in_progress)
	{
		setTimeout(function() { check_loading_in_progress(); }, 1000);
	} else
		stop_loading();
}

function addTab(tabTitle,id) 
{
	var tabs = $('#tabs');
	var found = false;
	var label = tabTitle || "Tab " + tabCounter;
	var li = $( tabTemplate.replace( /#\{href\}/g, "#s" + id ).replace( /#\{label\}/g, label ) );

	if(loading_in_progress)
	{
		start_loading();
		setTimeout(function() { check_loading_in_progress(); }, 1000);
		
	}
	

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
		tabs.find( ">nav>.ui-tabs-nav" ).append( li );
		tabs.append( "<section id='s" + id + "'></section>");

		$('#s' + id).load('tpl/serie.html', function() 
		{
			$('#s' + id).html($('#s' + id).html().replace(/###/g,id));
			//load_email(id);
			load_serie_keywords(id)
			apply_jcss();
			$( "#tabs" ).tabs("option", "active", tabCounter);
			tabCounter++;
		});
	}
}

function closeTab(element) 
{
	var tabs = $('#tabs');
	var panelId = element.remove().attr( "aria-controls" );
	panelId = panelId.substring(1);
	$( "#s" + panelId).remove();
	tabs.tabs("option", "active", 4);
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

// Loader management
function start_loading() {
	$('#blocker').fadeIn(10);
	$('#loading').fadeIn(10);
}

function stop_loading() {
	$('#blocker').fadeOut(300);
	$('#loading').fadeOut(300);
}

function add_serie_keyword(event)
{
	event.preventDefault();
	id = event.target.serie_id.value;
	var text = $("#keywords_list"+id+" input[name='keywords_new']").val();
	if (text != '')
	{
		var $li = $("<li class='keyword ui-state-default'/>").text(text);
		$li.attr('title',text);
		$("input[name='keywords_new']").val('');
		$("#keywords_list"+id+">.ui-state-disabled:first").before($li);
		$("#keywords_list"+id).sortable('refresh');
		save_serie_keywords(event,$("#keywords_list"+id));
	}
}

function reset_serie_keywords(event,ui)
{
	id = event.target.parentNode.getAttribute('serie_id');
	data = {"serie_id":id}
	$.post( "api/TvShowWatch.php?action=reset_serie_keywords", data)
	.done(function( data ) 
	{
		result = compute_data(data);
		if (result.ok)
		{
			show_info('Keywords updated');
		}
		load_serie_keywords(id);
		//stop_loading();
	});
}

function resetAllKeywords()
{
	start_loading();
	$.post( "api/TvShowWatch.php?action=reset_all_keywords")
	.done(function( data ) 
	{
		result = compute_data(data);
		if (result.ok)
			show_info('Keywords updated for all TV shows');
		for (sid in opened_tabs)
		{
			load_serie_keywords(id);
		}
		stop_loading();
	});
}

function save_serie_keywords(event,ui)
{
	id = event.target.getAttribute('serie_id');
	var keywords = [];
	$( "#keywords_list" + id ).children('li:not(.ui-state-disabled)').each(function()
	{
		keywords.push($(this).html());
	});
	data = {"serie_id":id,"keywords":keywords};
	$.post( "api/TvShowWatch.php?action=save_keywords", data)
	.done(function( data ) 
	{
		result = compute_data(data);
		if (result.ok)
			show_info('Keywords updated');
	});
}

function del_email(id,node)
{
	event.preventDefault();
	data = "serie_id="+id+"&email="+event.target.getAttribute('email');
	$.post( "api/TvShowWatch.php?action=delemail", data)
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
		{
			show_info(result.error);
			load_email(id);
		}
	});
}

function run() 
{
	var jqxhr = $.get( "api/TvShowWatch.php?action=run", function() {
	  show_info("Successfully run");
	});
}

function email_activation() {
  if ($("#smtp_enable").val() != '1')
      $(".smtp_required div input,.smtp_required div select").attr("disabled", "disabled");
  else
      $(".smtp_required div input,.smtp_required div select").removeAttr("disabled");
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
		result = compute_data(data);
		if (result.ok)
		{
			show_info(result.error);
		}
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
		result = compute_data(data);
		if (result.ok)
		{
			show_info(result.error)
			get_conf();
			load_tracker_conf();
		}
		stop_loading();
	});
	return false;
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
	    if($(this).attr('value') == value) { $(this).attr("selected", "selected")	; } });   
	}  
	});  
}

// Message management
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

function compute_data(data)
{
	try
	{
		result = JSON.parse(data);
		if (result.rtn != 200 && result.rtn != 302 && result.rtn != 230)
		{
			show_error(result.error);
			result.ok = false;
			
		} else
		{
			result.ok = true;
		}
		return result;
	}
	catch(err)
	{
		alert("API returns: "+data+"\r\nError:"+err.message);
		return {"ok":false};
	}
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
	.done(function( data ) 
	{  
		result = compute_data(data);
		if (result.ok)
			show_info('Keywords updated');
		//stop_loading();
	});
}


function add_keyword(e)
{
	e.preventDefault();
	var text = $("input[name='keywords_new']").val();
	if (text != '')
	{
		var $li = $("<li class='keyword ui-state-default'/>").text(text);
		$li.attr('title',text);
		$("input[name='keywords_new']").val('');
		$("#keywords_list>.ui-state-disabled:first").before($li);
		$("#keywords_list").sortable('refresh');
		save_keywords();
	}
}

function push_torrent(sid)
{
	event.preventDefault();
	start_loading();
	var formObj = event.target;
	var formURL = "api/TvShowWatch.php?action=pushTorrent";
	var formData = new FormData(formObj);
	$.ajax({
		url: formURL,
		type: 'POST',
		data: formData,
		mimeType: "multipart/form-data",
		contentType: false,
		cache: false,
		processData: false,
		success: function( data, textStatus, jqXHR )  
			{  
				result = compute_data(data);
				if (result.ok)
				{
					apply_jcss();
					$( "#tabs_serie_" + sid ).tabs( "option", "active", 0 );
					stop_loading();
					show_info(result.error);
				}
			}
		});
}

function check_episode(sid)
{
	event.preventDefault();
	var data = $('#s' + sid + ' .episode_form').serialize();
	$.post( "api/TvShowWatch.php?action=getEpisode", data)
	.done(function( data )  
	{
		season_selector = '#s' + sid + '>.episode_form>input[name="season"]';
		episode_selector = '#s' + sid + '>.episode_form>input[name="episode"]';
		format_2digits(season_selector);
		format_2digits(episode_selector);
		result = compute_data(data);
		if (!result.ok)
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
	var data = $('#data' + sid + '>.episode_form').serialize();
	
	$.post( "api/TvShowWatch.php?action=setSerie", data)
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
			show_info(result.error);
	});
}

function add_email(sid)
{
	event.preventDefault();
	var data = $('#emails' + sid + '>.email_add').serialize();
	$.post( "api/TvShowWatch.php?action=addemail", data)
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
		{
			show_info(result.error);
			$('#emails' + sid + ' input[name=\'email\']').val('');
			load_email(sid);
		}
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

function addSerie(id)
{
	event.preventDefault();
	var data = {'serie_id': id}
	$.post( "api/TvShowWatch.php?action=addSerie", data)
	.done(function( data )  
	{
		result = compute_data(data);
		if (result.ok)
		{
			serie_id = $('#addSerie input[name="serie_id"]').val();
			$('#addSerie input[name="serie_id"]').val('');
			data = {
					"page":"serie_line",
					"data":JSON.stringify({'series':[{
							'series_id': serie_id,
							}]})
					};
			//get_serielist(serie_id);
			get_serielist();
			show_info(result.error);
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
