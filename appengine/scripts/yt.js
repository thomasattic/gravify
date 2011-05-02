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

function onytplayerStateChange(newState) {
	if (newState == 0) {
		video_control.next_video();
	}
	console.log("player new state: " + newState);
}

var video_control = new function() {
  var ytplayer;
  var current_video = 0;
  var items;

  var playerReady = Threads.latchbinder();

  function init(playerId) {
    ytplayer = document.getElementById("myytplayer");
    ytplayer.addEventListener("onStateChange", "onytplayerStateChange");

    playerReady.latch();
  }

  function next_video() {
	switch_video(current_video + 1);
  }

  function switch_video(video_number) {
    playerReady.exec(function() {
      video_number = parseInt(video_number);

      console.warn("switching to: " + video_number);

	  if (!video_number) {
        video_number = 0;
      }
	  current_video = video_number;
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
        $("#videolist").append('<li><div class="videoitem" videonumber="'+i+'" place="0">' + item.title + '</div><div class="videodelete" style="float: right; margin-left: 10px; z-index: 1;">X</div></li>');
      });
      $(".videoitem").bind('click', function() {
        var video_number = $(this).attr('videonumber');
        switch_video(video_number);
        change_cursor(video_number);
      });
      $(".videodelete").bind('click', function() {
        var video_number = $(this).prev().attr('videonumber');
        delete_item(video_number);
      });
    });
  }
  
  var regexFull = /http\:\/\/www\.youtube\.com\/watch\?v=(\w{11})/;
  var regexBit = /http\:\/\/.youtu\.be\/(\w{11})/;
  var regexWord = /\w/;
  $(document).ready(function() {
    $("#add-url-form").submit(function(event) {
      console.warn("submit ....");
      event.preventDefault();
      var val = $("#youtube-url").val();
      var video_id = window.location.search.split('v=')[1];

      if (val.toLowerCase().indexOf("youtube.com") >= 0) {
        video_id = val.match(regexFull)[1];
      } else if (val.toLowerCase().indexOf("youtu.be") >= 0) {
        video_id = val.match(regexBit)[1];
      } 
      if (video_id) {
        add_item(video_id);
        $("#youtube-url").val("");
      }
    });
  });

  return {
    switch_video: switch_video,
    update_list: update_list,
	next_video: next_video,
    init: init
  };
};
