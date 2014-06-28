var serie_time = "0";
var series_data = new Array();
var loading_in_progress = false;
$(function() {
$.ajaxSetup({
    // Disable caching of AJAX responses
    cache: false
});
	var tabs = $( "#tabs" ).tabs();
	$( document ).tooltip({
		track: true
		});
	var tvshow_result = [];

	var trackers = [
		{'value':'t411', 'text':'T411','login':true},
		{'value':'tpb', 'text':'The Pirate Bay', 'login':false},
		{'value':'none', 'text':'No tracker, only manual push', 'login':false}
		];
	
	$("#smtp_enable").blur(email_activation);
	$('input').attr("autocomplete", "off");
	$( "#run" ).click(run);
	$( "#param" ).submit(event,save_conf);
	$( "#import_conf" ).submit(event,import_conf);
	$( "#addSerie" ).submit(function() { return false; });

	$( "#keywords_list" ).sortable({
		placeholder: "ui-state-highlight",
		distance: 15,
		items: "li:not(.ui-state-disabled)",
		axis: "y",
		stop: save_keywords
	});
	$( "#keywords_list" ).disableSelection();

	$("#trash").droppable({
		accept: "#keywords_list li",
		hoverClass: "ui-state-hover",
		drop: function(ev, ui) {
		    ui.draggable.remove();
		}
	});

	$( "#add_keyword" ).click(event, add_keyword);

// Hide or show login fields for tracker if required
	$('#tracker_id').change(load_tracker_conf); 

	$( "#resetAllKeywords" ).click(event,resetAllKeywords);

	$( "#tvshow_name" ).change(function() {
			if ($(this).val().length>2)
			{
				$.get("api/TvShowWatch.php?action=search&pattern="+$(this).val())
				.done(function(result) {
					data = JSON.parse(result);
					tvshow_result = data['result'];
					liste = '';
					for(serie in tvshow_result)
					{
						liste += '<li><div style="display:inline-block;width:200px"><a href="#" class="result_item" serie_id="' + tvshow_result[serie]['seriesid'] 
									+ '" >' + tvshow_result[serie]['seriesname'] + '</div></a>'
									+ '<div style="display:inline-block;width:150px">' + tvshow_result[serie]['network'] + '</div>'
									+ '<div style="display:inline-block;width:100px">' + tvshow_result[serie]['firstaired'] + '</div>'
									+ '</li>';
					}
					$( "#search_result" ).html(liste);
						$( ".result_item").click(function() {
								id = this.getAttribute('serie_id');
								addSerie(id);
						$( "#tvshow_name" ).val('');
						$( "#search_result" ).html('');
											});
				});
				return false;
			} else
			{
				$( "#search_result" ).html('');
			}

		});

	$(document).ready(function(){
		for (tracker in trackers)
		{
			myOption = new Option(trackers[tracker]["text"], trackers[tracker]["value"]);
			$("#tracker_id").append(myOption);
			$("#tracker_id option:last-child").attr('login',(trackers[tracker]["login"]) ? '1' : '0');
		}
		get_conf();
		apply_jcss();
		var source = new EventSource("api/TvShowWatch.php?action=streamGetSeries");
		source.onmessage = check_update;
		stop_loading();
	});


	var tabTitle; // = $( "#tab_title" ),
      tabContent = $( "#tab_content" ),
      tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span></li>",
      tabCounter = 5;
	opened_tabs = [];


    // close icon: removing the tab on click
    tabs.delegate( "span.ui-icon-close", "click", function() {
		element = $( this ).closest( "li" );
		closeTab(element);
	} );
 
    tabs.bind( "keyup", function( event ) {
      if ( event.altKey && event.keyCode === $.ui.keyCode.BACKSPACE ) {
	element = tabs.find( ".ui-tabs-active" );
	closeTab(element);
      }
    });

});
