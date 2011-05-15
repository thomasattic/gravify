
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
  var ytplayer;
  var current_video = 0;
  var items;

  var playerReady = Threads.latchbinder();

  function init(playerId) {
    ytplayer = document.getElementById("myytplayer");
    ytplayer.addEventListener("onStateChange", onytplayerStateChange);

    playerReady.latch();
  }

  function onytplayerStateChange(newState) {
    if (newState == 0) {
      video_control.next_video();
    }
    console.log("player new state: " + newState);
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
      if (items.length > 0) {
        var data = items[video_number];
        if (!data) {
          console.error("data not found: " + video_number);
        }
        var video_id=data.id;
        var video_title=data.title;

        ytplayer.loadVideoById(data.id);
      }
    });
  }

  function update_list(new_items) {
    playerReady.exec(function() {
      console.warn("setting list: " + new_items.length);
      items = new_items;
      $("#videolist").html('');
      $.each(items, function(i, item) {
        $("#videolist").append('<li><div class="videoitem" style="display: inline-block; width: 80%;" videonumber="'+i+'" place="0">' + item.title + '</div><div class="videodelete" style="display: inline-block; width: 20%;">X</div></li>');
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

  function get_youtube(video_id, fn, err) {
    var url = "http://gdata.youtube.com/feeds/api/videos/" + video_id + "?v=2&alt=json";
    $.ajax({
      type: 'GET',
      url: url,
      dataType: 'json',
      beforeSend: function(xhr) {},
      success: function(data) {
        fn(data);
      },
      error: function(request, textStatus, errorThrown) {
        // err
        var exception = {datasetname: 'madswvideo', status: request.status, message: request.statusText, url: url, method: "read", kind: textStatus};
        err(exception);
      }
    });
  }

  var regexFull = /http\:\/\/www\.youtube\.com\/watch\?v=(\w{11})/;
  var regexBit = /http\:\/\/.youtu\.be\/(\w{11})/;
  var regexWord = /\w/;
  var shortPrefix = "youtu.be/";
  $(document).ready(function() {
    $("#add-url-form").submit(function(event) {
      event.preventDefault();
      var val = $("#youtube-url").val().trim();
      var video_id = window.location.search.split('v=')[1];

      console.warn("submit: " + val + " :" + video_id);
      if (val.toLowerCase().indexOf("youtube.com") >= 0) {
        var vid = val.split('v=')[1];
        var ampersandPosition = vid.indexOf('&');
        if(ampersandPosition != -1) {
          video_id = vid.substring(0, ampersandPosition);
        } else {
          video_id = vid;
        }
      } else if (val.toLowerCase().indexOf("youtu.be/") >= 0) {
        video_id = val.substring(val.toLowerCase().indexOf(shortPrefix) + shortPrefix.length);
      } else if (val.indexOf("#") == 0) {
      	video_id = val.substr(1);
      }
      if (video_id) {
        get_youtube(video_id, function(data) {
          //console.warn("got it: " + video_id + " title: " + JSON.stringify(data.entry.title.$t));
          add_item({id: video_id, title: data.entry.title.$t});
          $("#youtube-url").val("");
        }, function(exception) {
          alert("Cannot find the specified movie");
        });
      }
    });
  });

  return {
    switch_video: switch_video,
    update_list: update_list,
    next_video: next_video,
    mute_video: mute_video,
    init: init
  };
};
