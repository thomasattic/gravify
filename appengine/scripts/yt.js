function onYouTubePlayerReady(playerId) {
  video_control.init(playerId);
}

var Threads = new function() {
  this.latchbinder = function() {
    var result = new function() {
      var instance = this;
      var caller, args;
      var queue = [];
      this.latch = function() {
        if (!caller) {
          caller = this;
          args = Array.prototype.slice.call(arguments);
          for (var i=0,len=queue.length; i<len; i++) {
            queue[i].apply(caller, args);
          }
          queue = null;
        }
      };
      this.exec = function(fn) {
        if (caller) {
          fn.apply(caller, args);
        } else {
          queue.push(fn);
        }
      };
    };
    return result;
  };
};

var video_control = new function() {
  var current_video = 0;
  var ytplayer;
  var items;

  var playerReady = Threads.latchbinder();

  function init(playerId) {
    ytplayer = document.getElementById("myytplayer");
    ytplayer.addEventListener("onStateChange", "onytplayerStateChange");

    playerReady.latch();
  }

  function onytplayerStateChange(newState) {
     //alert("Player's new state: " + newState);
  }

  function switch_video(video_number) {
    playerReady.exec(function() {
      console.warn("switching to: " + video_number);
      if (!video_number) {
        video_number = 0;
      }
      var data = items[video_number];
      var video_id=data.id;
      var video_title=data.title;

      ytplayer.loadVideoById(data.id);
    });
  }

  function update_list(new_items) {
    playerReady.exec(function() {
      console.warn("setting list: " + new_items.length);
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
    });
  }

  return {
    switch_video: switch_video,
    update_list: update_list,
    init: init
  };
};
