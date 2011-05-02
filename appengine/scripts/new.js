$(window).load(function(){
	
	
  $('#subscribers').masonry({
		animate: true,
	  itemSelector: '.friend',
	  columnWidth: 224
	});
	
	//$('.player-container').resize(function() {
	//  console.log($(this).height);
	//	$('#shubz_player').attr('height', $(this).height());
	//});
	
	// youtube scaling magic
  /*
		var $origVideo = $(".youtube, .youtube embed");
		var aspectRatio = $origVideo.attr("height") / $origVideo.attr("width");
					
		$(window).resize(function() {
			var wrapWidth = $("#page-wrap").width();
			$origVideo
				.width(wrapWidth)
				.height(wrapWidth * aspectRatio);
		}).trigger("resize");
	*/
});

