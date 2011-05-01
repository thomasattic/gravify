$(window).load(function(){
	
	
  $('#friends').masonry({
		singleMode: true,
		animate: true,
	  itemSelector: '.friend',
	  columnWidth: 240,
	});
	
	//$('.player-container').resize(function() {
	//  console.log($(this).height);
	//	$('#shubz_player').attr('height', $(this).height());
	//});
	
});

