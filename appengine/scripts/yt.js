
function onYouTubePlayerReady(playerId) {
  video_control.init(playerId);
}

var video_control = new function() {
  var current_video = 0;
  var ytplayer;
  var items;

  function init(playerId) {
    ytplayer = document.getElementById("myytplayer");
    ytplayer.addEventListener("onStateChange", "onytplayerStateChange");

    ytplayer.loadVideoById(data.id);
    ytplayer.playVideo();
  }

  function onytplayerStateChange(newState) {
     //alert("Player's new state: " + newState);
  }

  function switch_video(video_number) {
    if (ytplayer) {
      if (!video_number) {
        video_number = 0;
      }
      var data = items[video_number];
      var video_id=data.id;
      var video_title=data.title;
  
      ytplayer.loadVideoById(data.id);
    }
  }

  function update_list(new_items) {
    if (ytplayer) {
      items = new_items;
      $("#videolist").html('');
      $.each(items, function(i, item) {
        $("#videolist").append('<li><div class="videoitem" videonumber="'+i+'" place="0">' + item.title + '</div></li>');
      });
      $(".videoitem").bind('click', function() {
        var video_number = $(this).attr('videonumber');
        switch_video(video_number);
        change_cursor(video_number);
      });
    }
  }

  return {
    switch_video: switch_video,
    update_list: update_list,
    init: init
  };
};
