(function() {
  var jqt = $.jQTouch({
    updatehash: false,
    hashquery: true,
    clearInitHash: false
  });

  // Items handler listens to CRUD events from model
  var binder = {
    added: function(event) {
      var $newitem, $container;

      $newitem = $("#eventitem-template").tmpl(event.item);
      $container = $("#main ul#tab-browse");
      $container.append($newitem);
    },
    removed: function(event) {
    },
    updated: function(event) {
    }
  };

  $(document).ready(function() {
    var $container = $("#main");
    $container.find("input[type='radio'][name='categories']").bind("click", function(event) {
      var $target = $(this);
      var val = $target.val();
      if (val === "Create") {
        if (!$container.find("#tab-create").hasClass("on")) {
          $container.find(".tab").removeClass("on");
          $container.find("#tab-create").addClass("on");
        }
      } else if (val === "Browse") {
        if (!$container.find("#tab-browse").hasClass("on")) {
          $container.find(".tab").removeClass("on");
          $container.find("#tab-browse").addClass("on");
        }
      } else {
        console.error("Unexpected radio button value: " + val);
      }
    });
  });

  /* the init might kill the rest of the script. runs it last */
  FB.init({
    appId:'111989465554857', cookie:true,
    status:true, xfbml:true
  });
})();
