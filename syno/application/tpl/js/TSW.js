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
	
	$("#smtp_enable").blur(email_activation);
	$('input').attr("autocomplete", "off");
	$( "#run" ).click(run);
	$( "#param" ).submit(event,save_conf);
	$( "#import_conf" ).submit(event,import_conf);
	//$( "#addSerie" ).submit(event,addSerie);
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

	if (!conf_status)
		$(document).ready(conf_ko);

	$(document).ready(function(){
		get_conf();
		apply_jcss();
		stop_loading();
	});


	var tabTitle; // = $( "#tab_title" ),
      tabContent = $( "#tab_content" ),
      tabTemplate = "<li><a href='#{href}'>#{label}</a> <span class='ui-icon ui-icon-close' role='presentation'>Remove Tab</span></li>",
      tabCounter = 4;
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
