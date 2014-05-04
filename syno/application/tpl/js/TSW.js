$(function() {
$.ajaxSetup({
    // Disable caching of AJAX responses
    cache: false
});
	var tabs = $( "#tabs" ).tabs();
	$( document ).tooltip({
		track: true
		});
	
	$('#apply_jcss').click(apply_jcss);
	$("#smtp_enable").blur(email_activation);
	$('input').attr("autocomplete", "off");
	$( "#run" ).click(run);

	$( "#conf_ok" ).click(conf_ok);
	$( "#conf_ko" ).click(conf_ko);
	$( "#param" ).submit(event,save_conf);
	$( "#import_conf" ).submit(event,import_conf);
	$( "#addSerie" ).submit(event,addSerie);

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

	$( "#resetAllKeywords" ).click(event,resetAllKeywords);

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
