$(window).load(function(){
	
	
  $('#friends').masonry({
		singleMode: true,
		animate: true,
	  itemSelector: '.friend',
	});
	
	$('.player-container').resize(function() {
	  console.log($(this).height);
		$('#shubz_player').attr('height', $(this).height());
	});
	
});

