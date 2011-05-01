		var apiKey = 589411; // OpenTok sample API key. Replace with your own API key.
		var sessionId = '153975e9d3ecce1d11baddd2c9d8d3c9d147df18'; // Replace with your session ID.
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
         "items":[
            {"id":"tl_BUk5P8RA","title":"Sesame Street: Smell Like A Monster","description":"Grover talks about the word \"on.\" Visit Grover on Facebook: on.fb.me If you're watching videos with your preschooler and would like to do so in a safe, child-friendly environment, please join us at www.sesamestreet.org Sesame Street is a production of Sesame Workshop, a nonprofit educational organization which also produces Pinky Dinky Doo, The Electric Company, and other programs for children around the world."},
            {"id":"3tI4CbCniBI","title":"Old Spice | Flex :30","description":"Welcome to the wildly powerful world of Odor Blocker Body Wash. I hope you're into explosions. Directed by Tim and Eric from the Awesome Show."},
            {"id":"Af1OxkFOK18","title":"Old Spice Commercial ft Bruce Campbell","description":"Old Spice commercial starring Bruce Campbell"}
          ]
        }

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
			var subscriberDiv = document.createElement('div'); // Create a div for the subscriber to replace
			subscriberDiv.setAttribute('id', stream.streamId); // Give the replacement div the id of the stream as its id.
			subscriberDiv.setAttribute('class', 'friend'); // Give the replacement div the id of the stream as its id.
			document.getElementById("subscribers").appendChild(subscriberDiv);
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
    }
    function read() {
       items.read(sessionId, function(list) {
          // fn
          if (!list || list.current===undefined || list.current===null || list.items.length === 0) {
             list = DEFAULT_LIST;
             items.update(sessionId, JSON.stringify(list), function() {
                console.warn("updated");
             }, function(exception) {
                console.warn(JSON.stringify(exception));
             });
           }
           //console.warn("=== poll (pos): " + list.current + " (length): " + list.items.length + " ===");
           if (!Hashs.isEquals(playlist, list.items)) {
              //console.warn("=== playlist updated from the server ===");
              video_control.update_list(list.items);
              video_control.switch_video(list.current);
              playlist = list.items;
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
          playlist = new_list;
          console.warn("updated list: " + playlist.length);
          video_control.update_list(playlist);
        }, function(exception) {
          console.warn(JSON.stringify(exception));
        });
      }
    }
    function add_item(video_id) {
      var new_list = playlist.slice(0);
      //console.warn("before list: " + JSON.stringify(playlist));
      new_list.push({id: video_id, title: "newly added: " + video_id});
      //console.warn("after list: " + JSON.stringify(playlist));
      items.update(sessionId, JSON.stringify({items: new_list, current: onair}), function() {
        playlist = new_list;
        console.warn("updated list: " + playlist.length);
        video_control.update_list(playlist);
      }, function(exception) {
        console.warn(JSON.stringify(exception));
      });
    }
    function createSession(fn) {
      var url = '/newsession';
      $.ajax({
        type: 'POST',
        url: url,
        dataType: 'xml',
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
        console.warn("updated index: " + onair);
      }, function(exception) {
        console.warn(JSON.stringify(exception));
      });
    }
    $(document).ready(function() {
      var loc = window.location;
      var search = parseSearch(loc.hash.substring(1));
      if (search.session) {
        sessionId = search.session;
      }
      createSession(function(data) {
        var go = false;
        if (go) {
          console.error("token: " + data.session_id);
          if (data.session_id) {
            sessionId = data.session_id;
            window.location = window.location + '#' + getSearchString({session: data.session_id}); 
          }
        }
      });
      read();
      setInterval(function() {
         read();
      },
      1000);
    });
