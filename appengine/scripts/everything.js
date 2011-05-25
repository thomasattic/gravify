		var apiKey = 589411; // OpenTok sample API key. Replace with your own API key.
		var sessionId = '153975e9d3ecce1d11baddd2c9d8d3c9d147df18'; // Replace with your session ID.
		//var sessionId = '17d88c9b1a3a78aa09b1f3e1e72324a14f8f61be'; // Replace with your session ID.
		var token = 'devtoken'; // Should not be hard-coded.
								// Add to the page using the OpenTok server-side libraries.
		var session;
		var publisher;
		var subscribers = {};
        var DOC_URL = "/jdata";
        var playlist = [];
        var onair = 0;
        var DEFAULT_LIST = {
         "current": 0,
         items: []
        };

		// Un-comment either of the following to set automatic logging and exception handling.
		// See the exceptionHandler() method below.
		// TB.setLogLevel(TB.DEBUG);
		TB.addEventListener("exception", exceptionHandler);

		if (TB.checkSystemRequirements() != TB.HAS_REQUIREMENTS) {
			alert("You don't have the minimum requirements to run this application."
				  + "Please upgrade to the latest version of Flash.");
		}

		//--------------------------------------
		//  LINK CLICK HANDLERS
		//--------------------------------------

		/*
		If testing the app from the desktop, be sure to check the Flash Player Global Security setting
		to allow the page from communicating with SWF content loaded from the web. For more information,
		see http://www.tokbox.com/opentok/build/tutorials/helloworld.html#localTest
		*/
		function connect() {
			session = TB.initSession(sessionId);	// Initialize session

			// Add event listeners to the session
			session.addEventListener('sessionConnected', sessionConnectedHandler);
			session.addEventListener('sessionDisconnected', sessionDisconnectedHandler);
			session.addEventListener('connectionCreated', connectionCreatedHandler);
			session.addEventListener('connectionDestroyed', connectionDestroyedHandler);
			session.addEventListener('streamCreated', streamCreatedHandler);
			session.addEventListener('streamDestroyed', streamDestroyedHandler);

			session.connect(apiKey, token);
		}

		function disconnect() {
			session.disconnect();

			// Add event listeners to the session
			session.removeEventListener('sessionConnected', sessionConnectedHandler);
			session.removeEventListener('sessionDisconnected', sessionDisconnectedHandler);
			session.removeEventListener('connectionCreated', connectionCreatedHandler);
			session.removeEventListener('connectionDestroyed', connectionDestroyedHandler);
			session.removeEventListener('streamCreated', streamCreatedHandler);
			session.removeEventListener('streamDestroyed', streamDestroyedHandler);

			hide('disconnectLink');
			hide('publishLink');
			hide('unpublishLink');
		}

		// Called when user wants to start publishing to the session
		function startPublishing() {
			if (!publisher) {
				var parentDiv = document.getElementById("myCamera");
				var publisherDiv = document.createElement('div'); // Create a div for the publisher to replace
				publisherDiv.setAttribute('id', 'opentok_publisher');
				parentDiv.appendChild(publisherDiv);
				publisher = session.publish(publisherDiv.id); // Pass the replacement div id to the publish method
			}
		}

		function stopPublishing() {
			if (publisher) {
				session.unpublish(publisher);
			}
			publisher = null;

			show('publishLink');
			hide('unpublishLink');
		}

		//--------------------------------------
		//  OPENTOK EVENT HANDLERS
		//--------------------------------------

		function sessionConnectedHandler(event) {
			// Subscribe to all streams currently in the Session
			for (var i = 0; i < event.streams.length; i++) {
				addStream(event.streams[i]);
			}
			room_entered();
		}

		function streamCreatedHandler(event) {
			// Subscribe to the newly created streams
			for (var i = 0; i < event.streams.length; i++) {
				addStream(event.streams[i]);
			}
			room_camera_on();
		}

		function streamDestroyedHandler(event) {
			// This signals that a stream was destroyed. Any Subscribers will automatically be removed.
			// This default behaviour can be prevented using event.preventDefault()
			room_camera_off();
		}

		function sessionDisconnectedHandler(event) {
			// This signals that the user was disconnected from the Session. Any subscribers and publishers
			// will automatically be removed. This default behaviour can be prevented using event.preventDefault()
			publisher = null;
			room_left();
		}

		function connectionDestroyedHandler(event) {
			// This signals that connections were destroyed
		}

		function connectionCreatedHandler(event) {
			// This signals new connections have been created.
		}

		/*
		If you un-comment the call to TB.addEventListener("exception", exceptionHandler) above, OpenTok calls the
		exceptionHandler() method when exception events occur. You can modify this method to further process exception events.
		If you un-comment the call to TB.setLogLevel(), above, OpenTok automatically displays exception event messages.
		*/
		function exceptionHandler(event) {
			alert("Exception: " + event.code + "::" + event.message);
		}

		//--------------------------------------
		//  HELPER METHODS
		//--------------------------------------

		function addStream(stream) {
			// Check if this is the stream that I am publishing, and if so do not publish.
			if (stream.connection.connectionId == session.connection.connectionId) {
				return;
			}
			var containerDiv = document.createElement('div');
			containerDiv.setAttribute('class', 'friend');
			document.getElementById("subscribers").appendChild(containerDiv);
			
			var subscriberDiv = document.createElement('div'); // Create a div for the subscriber to replace
			subscriberDiv.setAttribute('id', stream.streamId); // Give the replacement div the id of the stream as its id.
			subscriberDiv.setAttribute('class', 'friend'); // Give the replacement div the id of the stream as its id.
			containerDiv.appendChild(subscriberDiv);
			subscribers[stream.streamId] = session.subscribe(stream, subscriberDiv.id);
		}

		function show(id) {
			document.getElementById(id).style.display = 'inline';
		}

		function hide(id) {
			document.getElementById(id).style.display = 'none';
		}
		
		function enable(id) {
			document.getElementById(id).disabled = false;
		}
		
		function disable(id) {
			document.getElementById(id).disabled = true;
		}
		
		function show_and_disable(id) {
			show(id);
			disable(id);
		}

		function show_and_enable(id) {
			show(id);
			enable(id);
		}

    var Hashs = new function() {
      // <isEquals>
      // http://www.pageforest.com/lib/beta/js/pf-client.js : namespace.lookup('org.startpad.base')
      function generalType(o) {
        var t = typeof(o);
        if (t != 'object') {
            return t;
        }
        if (o instanceof String) {
            return 'string';
        }
        if (o instanceof Number) {
            return 'number';
        }
        return t;
      }

      function keys(map) {
        var list = [];

        for (var prop in map) {
            if (map.hasOwnProperty(prop)) {
                list.push(prop);
            }
        }
        return list;
      }

      /* Sort elements and remove duplicates from array (modified in place) */
      function uniqueArray(a) {
        if (!(a instanceof Array)) {
            return;
        }
        a.sort();
        for (var i = 1; i < a.length; i++) {
          if (a[i - 1] == a[i]) {
              a.splice(i, 1);
          }
        }
      }

      //Perform a deep comparison to check if two objects are equal.
      //Inspired by Underscore.js 1.1.0 - some semantics modifed.
      //Undefined properties are treated the same as un-set properties
      //in both Arrays and Objects.
      //Note that two objects with the same OWN properties can be equal
      //if they have different prototype chains (and inherited values).
      this.isEquals = function isEqual(a, b) {
        if (a === b) {
            return true;
        }
        if (generalType(a) != generalType(b)) {
            return false;
        }
        if (a == b) {
            return true;
        }
        if (typeof a != 'object') {
            return false;
        }
        // null != {}
        if (a instanceof Object != b instanceof Object) {
            return false;
        }

        if (a instanceof Date || b instanceof Date) {
            if (a instanceof Date != b instanceof Date ||
                a.getTime() != b.getTime()) {
                return false;
            }
        }

        var allKeys = [].concat(keys(a), keys(b));
        uniqueArray(allKeys);

        for (var i = 0; i < allKeys.length; i++) {
            var prop = allKeys[i];
            if (!isEqual(a[prop], b[prop])) {
                return false;
            }
        }
        return true;
      }
      // </isEquals>

      return this;
    };
    function removeArray(array, from, to) {
      //Array Remove - By John Resig (MIT Licensed)
      var rest = array.slice((to || from) + 1 || array.length);
      array.length = from < 0 ? array.length + from : from;
      return array.push.apply(array, rest);
    };
    function parseSearch(q) {
      // Andy E and community @ http://stackoverflow.com/posts/2880929/revisions
      var results = {};
      var e,
          a = /\+/g,  // Regex for replacing addition symbol with a space
          r = /([^&=]+)=?([^&]*)/g,
          d = function (s) { return decodeURIComponent(s.replace(a, " ")); };

      while (e = r.exec(q)) {
         results[d(e[1])] = d(e[2]);
      }
      return results;
    };
    function getSearchString(search) {
      var result = '';
      for (var item in search) {
          if (result.length !== 0) {
              result += '&';
          }
          result += item + '=' + encodeURIComponent(search[item]);
      }
      return result;
    };
    function optPrefix(leading, string) {
      if (!string) {
        return string;
      }
      return leading + string;
    };
    function replaceHrefPart(loc, parts) {
      var href = {protocol: loc.protocol, host: loc.host, port: loc.port,
          pathname: loc.pathname, hash: loc.hash, search: loc.search};
      var h = $.extend(href, parts);
      var result = "";
      result += h.protocol;
      result += "//";
      result += h.host;
      result += h.pathname;
      result += h.search;
      result += h.hash;

      return result;
    };

    var items = {
      read: function(id, fn, err) {
        var url = DOC_URL + "/" + id;
        $.ajax({
          type: 'GET',
          url: url,
          dataType: 'json',
          beforeSend: function(xhr) {},
          success: function(data) {
            // console.log("read succeded: " + JSON.stringify(data));
            fn(data);
          },
          error: function(request, textStatus, errorThrown) {
            // err
            var exception = {datasetname: 'madswvideo', status: request.status, message: request.statusText, url: url, method: "read", kind: textStatus};
            err(exception);
          }
        });
      },
      update: function(id, json, fn, err) {
        var url = DOC_URL + "/" + id;
        $.ajax({
          type: 'POST',
          url: url,
          data: json,
          dataType: 'json',
          beforeSend: function(xhr) {},
          success: fn,
          error: function(request, textStatus, errorThrown) {
            // err
            var exception = {datasetname: 'madswvideo', status: request.status, message: request.statusText, url: url, method: "update", kind: textStatus};
            err(exception);
          }
        });
      }
    };
    function poke_video_control() {
      video_control.update_list([]);
      video_control.switch_video(0);
    }
    function read() {
       items.read(sessionId, function(list) {
          // fn
           //console.warn("=== poll (pos): " + list.current + " (playlist): " + playlist.length + " (length): " + list.items.length + " ===");
           if (!Hashs.isEquals(playlist, list.items)) {
              //console.warn("=== playlist updated from the server ===");
              video_control.update_list(list.items);
              video_control.switch_video(list.current);
              playlist = list.items? list.items: [];
           } else if (onair !== list.current) {
              //console.warn("=== current song is updated ===");
              video_control.switch_video(list.current);
              onair = list.current;
           } else {
             //console.warn("=== no change ===");
           }
       }, function(exception) {
          console.warn(JSON.stringify(exception));
       });
    }
    function delete_item(video_id) {
      var new_list = playlist.slice(0);
      var index = onair;
      if (video_id < playlist.length) {
        removeArray(new_list, video_id);
        if (index !== onair) {
          index = Math.min(video_id + 1, new_list.length - 1);
          if (index !== onair) {
            video_control.switch_video(index);
          }
        }

        items.update(sessionId, JSON.stringify({items: new_list, current: index}), function() {
          playlist = new_list? new_list: [];
          console.warn("updated list: " + playlist.length);
          video_control.update_list(playlist);
        }, function(exception) {
          console.warn(JSON.stringify(exception));
        });
      }
    }
    function add_item(item) {
      var new_list = playlist.slice(0);
      //console.warn("before list: " + JSON.stringify(playlist));
      new_list.push(item);
      //console.warn("after list: " + JSON.stringify(playlist));
      items.update(sessionId, JSON.stringify({items: new_list, current: onair}), function() {
        playlist = new_list? new_list: [];
        console.warn("updated list: " + playlist.length);
        video_control.update_list(playlist);
      }, function(exception) {
        console.warn(JSON.stringify(exception));
      });
    }
    function createSession(fn, err) {
      var url = '/newsession';
      $.ajax({
        type: 'GET',
        url: url,
        dataType: 'JSON',
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
    };
    function change_cursor(index) {
      items.update(sessionId, JSON.stringify({items: playlist, current: index}), function() {
        onair = index;
      }, function(exception) {
        console.warn(JSON.stringify(exception));
      });
    }
    function poll() {
      try{sgtracker.setSgAccount("geuaegzh");}catch(err){};
      $("#fbSendLink").attr("href", location);
      poke_video_control();
      setTimeout(function() {
        ping();
      }, 0);
    }
    function ping() {
      read();
      setTimeout(function() {
         ping();
      }, 1000);
    }
    $(document).ready(function() {
      var loc = window.location;
      var search = parseSearch(loc.hash.substring(1));
      if (search.session) {
        $(".playlist .inline .selected").removeClass("selected");
        $("#enterroom").addClass("selected");

        sessionId = search.session;
        poll();
      } else {
        poll();
      }
      $("#video-mute").bind("click", function() {
        console.warn("mute... clicked");
        var $target = $(this);
        if (!$target.hasClass("selected")) {
          $target.addClass("selected");
          $target.text("Unmute");
          video_control.mute_video();
        } else {
          $target.removeClass("selected");
          $target.text("Mute");
          video_control.unmute_video();
        }
      });
      $("#video-suspend").bind("click", function() {
        console.warn("take_break... clicked");
        var $target = $(this);
        if (!$target.hasClass("selected")) {
          $target.addClass("selected");
          $target.text("Resume");
          video_control.suspend_video();
        } else {
          $target.removeClass("selected");
          $target.text("Take a break");
          video_control.unsuspend_video();
        }
      });
      $("#publicroom").bind("click", function() {
        var $target = $(this);
        if (!$target.hasClass("selected")) {
          if (confirm("Are you sure?")) {
            $("body").addClass("block");
            $(".playlist .inline .selected").removeClass("selected");
            $target.addClass("selected");
            window.location.hash = "";
            window.location.reload();
          }
        }
      });
      $("#enterroom").bind("click", function() {
        var hash, loc;
        var room = prompt("Please enter your room number:", search.session);
        if (room && room !== search.session) {
          $("body").addClass("block");
          hash = optPrefix("#", getSearchString({session: room}));
          loc =  replaceHrefPart(window.location, {hash: hash});
          window.location = loc;
          window.location.reload();
        }
      });
      $("#createroom").bind("click", function() {
        var $target = $(this);
        if (!$target.hasClass("selected")) {
          $(".selected").removeClass("selected");
          $target.addClass("selected");
          $("body").addClass("block");
          createSession(function(data) {
            var hash, loc;
            if (data.session_id) {
              sessionId = data.session_id;
              hash = optPrefix("#", getSearchString({session: data.session_id}));
              loc =  replaceHrefPart(window.location, {hash: hash});
              window.location = loc;
              window.location.reload();
            }
          }, function(exception) {
            console.error(JSON.stringify(exception));
          });
        }
      });
      $("#fbinvite").bind("click",
        function() {
          var link = document.URL;
          console.warn("url: " + link);

          FB.ui({
            method: 'feed',
            name: 'Facebook Dialogs',
            link: link,
            picture: 'http://fbrell.com/f8.jpg',
            caption: 'Reference Documentation',
            description: 'Dialogs provide a simple, consistent interface for applications to interface with users.',
            message: 'Facebook Dialogs are easy!'
          },
          function(response) {
            if (response && response.post_id) {
              alert('Post was published.');
            } else {
              alert('Post was not published.');
            }
          });
        });
        //FB.ui({method: 'send', message: 'Come watch this awesome video with me:' + document.URL + "#session="+ sessionId});
          /* {
          method: 'send', message: 'Come watch this awesome video with me.' ,
          name: 'Invite friend',
          link: document.URL,
          caption: 'Gravify: Watch with friends',
          picture: 'http://www.gravify.com/images/logo_gravify.png'
        },
        function(response) {
          if (response && response.post_id) {
            alert('Post was published.');
          } else {
            alert('Post was not published.');
          }
        });
          */
      //});
    });
