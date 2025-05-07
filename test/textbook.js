function uuid() {
  var id = "", i, random;
  for (i = 0; i < 32; i++) {
    random = Math.random() * 16 | 0;
    if (i === 8 || i === 12 || i === 16 || i === 20) {
      id += "-";
    }
    id += (i === 12 ? 4 : (i === 16 ? (random & 3 | 8) : random)).toString(16);
  }
  return id;
}

//~ https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

/*
function setSocket() {
  var id = uuid();
  var socket = (function() {
    var socket = new WebSocket("ws://"+ document.domain +":8765/");
    socket.onerror = function(event) {
      console.error("WebSocket error:", event);
      document.querySelector("body").innerHTML = "SOCKET ERROR";
    };
    return socket;
  })();
*/

function setSocket() {
  var id = uuid();
  var socket = new WebSocket("ws://"+ document.domain +":8765/");

  socket.onopen = function(event) {
    var msg = JSON.stringify({"id": id, "msg": "register", "to": "host", "path": window.location.pathname});
    socket.send(msg);
    var key = getParameterByName("key", location.href);
    socket.send(JSON.stringify({"msg": "checkLock", "id": id, "lvl": 1, "data": key, "to": "host"}));
  };

  socket.onmessage = function (event) {
    var data = JSON.parse(event.data);
    for (var key in OPS) {
      if (OPS.hasOwnProperty(key) && key == data['msg']) {
        OPS[key](data);
      }
    }
  }

  var OPS = {
    "accessDenied": function(data) {
      //window.location = "/login/1";
      var from = window.location.href.split('?')[0];
      window.location = "/login/1?from=" + from;
    }
  }

  return socket;
};

document.addEventListener("DOMContentLoaded", function(){
  var bLazy = new Blazy();
  var socket = setSocket();

  var scrubber = new ScrubberView();
  document.getElementById("scrubber").appendChild(scrubber.elt);
  scrubber.min(0).max(1000).step(1).value(1000).orientation('vertical').elt.style.height = "90vh";
  currentMedia.ontimeupdate = function() {
      scrubber.value(round(1000 - ((currentMedia.currentTime * 1000)/ currentMedia.duration),1));
  };

  scrubber.onScrubEnd = function (value) {
    currentMedia.currentTime = round(((1000 - scrubber.value())/ 1000)* currentMedia.duration,1);
    return false;
  };

  document.querySelector("#speed").addEventListener("input", function (evt) {
    var trackSpeed = this.value;
    var autoPlay = '0';
    currentMedia.playbackRate = trackSpeed/10;
  });

  var thumb = document.querySelector('#sidebar .scrubber-vert .thumb');
  thumb.addEventListener("click", mouseClick);

  function mouseClick() {
    if (currentMedia.paused) {
      currentMedia.play();
    } else {
      currentMedia.pause();
      resetAudioButtons();
    }
  }

  var draggables = document.querySelectorAll('.draggable li');
  if (draggables.length > 0) {
    window._lload("../../app/js/dragula.min.js", function (err) {
      var drake = dragula().on("drop", function (el, container) {
        el.classList.toggle("dropped");
      });
      forEach(draggables, function (i, val) {
        drake.containers.push(draggables[i]);
      });
    })
  }

  document.querySelector("#main").addEventListener("click", function(e) {
    var classes = e.target.classList;
    if (classes.contains("key")) {
      classes.toggle("unsolved");
    } else if (classes.contains("skey")) {
      classes.toggle("unsolved");
    } else if (classes.contains("audio")) {
      clicked(e);
    } else if (e.target.parentNode.classList.contains("frag")) {
      playClip(e.target.parentNode);
    } else if (classes.contains("pop-out")) {
      popOut(e);
    }
  });
});

function resetAudioButtons() {
  var otherAudios = document.getElementsByClassName("audio");
  forEach(otherAudios, function (i, val) {
      otherAudios[i].innerHTML = 'Play <i class="fa fa-play"></i>';
  });
}

//define the listener
function clicked(event) {
  var button = event.target;
  var trackHolder = document.getElementById(button.dataset.target);
  var trackURL = trackHolder.dataset.track;
  if (button.innerHTML == 'Pause <i class="fa fa-stop"></i>') {
    button.innerHTML = 'Play <i class="fa fa-play"></i>';
    currentMedia.pause();
  } else {
    confirmAudioTrack(trackURL);
    resetAudioButtons();
    button.innerHTML = 'Pause <i class="fa fa-stop"></i>';
    currentMedia.play();
  }
  currentMedia.addEventListener("ended", function() {
    button.innerHTML = 'Again <i class="fa fa-repeat"></i>';
    document.querySelector("#sidebar").classList.remove("playing");
    currentMedia.currentTime = 0;
  });
}

// Utility function: play mp3 fragment
function playClip(el) {
  var ref = el.getAttribute("href");
  var parent = getAncestor(el, "article");
  var trackURL = parent.dataset.track;
  confirmAudioTrack(trackURL);
  var trackSpeed = document.querySelector("#speed").value;
  var rootsrc = currentMedia.getAttribute("src").replace(/(\#.*)$/g, "");
  currentMedia.setAttribute("src", rootsrc + ref);
  currentMedia.playbackRate = trackSpeed/10;
  currentMedia.play();
  return false;
}

function confirmAudioTrack(trackURL) {
  if (audioName != trackURL) {
    audioName = trackURL;
    currentMedia.currentTime = 0;
    currentMedia.setAttribute("src", trackURL);
  }
}

function getAncestor(el, parentSelector) {
  // If no parentSelector defined will bubble up all the way to *document*
  if (parentSelector === undefined) {
    parentSelector = document;
  }
  var p = el.parentNode;
  while (p !== document) {
    var o = p;
    p = o.parentNode;
    if (p.tagName == parentSelector.toUpperCase()) {
      return p;
    }
  }
}

function fold(uuid,el) {
  var transcript = document.getElementById(uuid);
  var text = transcript.querySelectorAll("p");
  if (transcript.classList.contains("folded")) {
    el.innerHTML = 'Fold <i class="fa fa-minus-square"></i>';
  } else {
    el.innerHTML = 'Unfold <i class="fa fa-plus-square"></i>';
  }
  transcript.classList.toggle('folded');
}

function popOut(event) {
  event.preventDefault();
  var root = document.location.pathname.split("/").slice(0,-1).join("/") + "/";
  var url = event.target.href.replace("static","viewer/static").replace("?caps=", "?caps=" + root);
  var win = window.open(url, '_blank');
  win.focus();
  return false;
}

var audioName = "Earthbound";
var currentMedia = new Audio("../../app/assets/sounds/Title.mp3");
var currentTime = currentMedia.currentTime;

// ### Keyboard shortcuts

document.addEventListener("keydown", function(e) {
  var code = (e.keyCode ? e.keyCode : e.which);
  if (document.activeElement.tagName.toLowerCase() == "object") {
    return true;
  } else {
    switch (code) {
      case 37: // Left
        slideUp();
        break;
      case 32: // Space
      case 34: // Page down
      case 39: // Right
        slideDown();
        break;
      case 84: // t
        openToolBox(myurl);
        break;
      case 66: // b
        blackscreen();
        break;
      case 65: // a
        revealFirstKey();
        break;
    }
  }
});

// ### Modal Windows
//
function popImage(img){
  var image = img.src;
  var style = "";
  if (window.innerWidth >= 768){
    if (img.width >= img.height) {
      style = style + "min-width: 90vw; height: auto; max-height: 98vh !important";
    } else {
      style = style + "min-height: 90vh; width: auto; max-width: 98vw !important";
    }
    uglipop({class:"popImage", //styling class for Modal
      source:"html",
      content:'<div><img style="'+ style +'" src="'+ image +'"></div>'});
  }
}

function videoprojector(video,captions){
  if (captions) {
    vtt = "<track label='English' kind='subtitles' srclang='en' src='" + captions + "'>";
  } else {
    vtt = "";
  }
  uglipop({class:"video", //styling class for Modal
    source:"html",
    content:'<video style="width:90vw; height: auto;" controls><source src="' + video + '" type="video/mp4"/>' + vtt +'</video>'});
}

function iframe(document){
  uglipop({class:"iframe", //styling class for Modal
    source:"html",
    content:'<div class="intrinsic-container intrinsic-container-4x3"><iframe src="'+ document +'"></iframe></div>'});
}

function blackscreen(){
  var wrapper = document.querySelector("#uglipop_overlay_wrapper");
  if (wrapper.getAttribute("style").search("display: none") == -1) {
    remove();
  } else {
    uglipop({
      class:"blackscreen", //styling class for Modal
      source:"html",
      content:'<div></div>'
    });
  }
}

function remove() {
  document.getElementById('uglipop_overlay_wrapper').style.display = "none";
  document.getElementById('uglipop_overlay').style.display = "none";
  document.getElementById('uglipop_content_fixed').style.display = "none";
}

// ### Utility Functions
//

// http://www.jacklmoore.com/notes/rounding-in-javascript/
function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

function errorMSG() {
  uglipop({
    class:'error',
    source:'html',
    content:'<i class="fa fa-exclamation-triangle"></i>'
  });
}

// from: https://toddmotto.com/ditch-the-array-foreach-call-nodelist-hack/
var forEach = function (array, callback, scope) {
  for (var i = 0; i < array.length; i++) {
    callback.call(scope, i, array[i]); // passes back stuff we need
  }
};

function cloak(uuid,el) {
  var transcript = document.getElementById(uuid);
                // document.querySelector("#" + uuid); // doesn't work because it seems that the initial number of uuid has to be escaped …
  var lines = transcript.querySelectorAll(".text");
  var re = /([a-zA-Z0-9'’]*)/g;
  if (transcript.classList.contains("uncloaked")) {
    for (var i = 0; i < lines.length; i++) {
      var words = lines[i].textContent;
      lines[i].innerHTML = words.replace(re, '<span class="key unsolved">$1</span>');
    }
    el.innerHTML = 'Show <i class="fa fa-eye"></i>';
  } else {
    forEach(lines, function (i, val) {
      var words = lines[i].textContent;
      lines[i].innerHTML = words;
    });
    el.innerHTML = 'Hide <i class="fa fa-eye"></i>';
  }
  transcript.classList.toggle("uncloaked");
}

function revealFirstKey() {
  var unsolved = document.querySelectorAll('.unsolved');
  for (var i = 0; i < unsolved.length; i++) {
    var el = unsolved[i];
    if (isElementInViewport(el)) {
      el.classList.toggle("unsolved");
      return;
    }
  }
}

function slideDown() {
  var stops = document.querySelectorAll('h2, h3, h4');
  var scrolled = window.pageYOffset;
  for (var i = 0; i < stops.length; i++) {
    var el = stops[i];
    if (isElementInViewport(el) === false && el.offsetTop > scrolled) {
      window.scrollTo(0, el.offsetTop);
      return;
    }
  }
}

function slideUp() {
  var candidates = [];
  var stops = document.querySelectorAll('h2, h3, h4');
  var scrolled = window.pageYOffset;
  for (var i = 0; i < stops.length; i++) {
    var el = stops[i];
    if (isElementInViewport(el) === false && el.offsetTop < scrolled) {
      candidates.push(el.offsetTop);
    }
  }
  window.scrollTo(0, Array.max(candidates));
  return;
}

Array.max = function(array){
  return Math.max.apply( Math, array );
};

//~ https://stackoverflow.com/questions/123999/how-to-tell-if-a-dom-element-is-visible-in-the-current-viewport/7557433#7557433
function isElementInViewport (el) {
  var rect = el.getBoundingClientRect();
  return (
    rect.top >= 0 &&
    rect.left >= 0 &&
    rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) && /*or $(window).height() */
    rect.right <= (window.innerWidth || document.documentElement.clientWidth) /*or $(window).width() */
  );
}

function buildMDContent(link) {
  window._lload("../../app/js/marked.lazy.js", function (err) {
    window._lload("../../app/js/marked-renderer.js", function (err) {
      var request = new XMLHttpRequest();
      request.open("GET", link, true);
      request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
          var response = request.responseText;
          data = marked(response, {renderer: renderer}).replace(/{/g, "<a class='key unsolved'>").replace(/}/g, "</a>");
          uglipop({class:"markdownWrapper",
            source:"html",
            content:'<section id="s1">' + data + '</section>'});
        } else {
          errorMSG();
        }
      };
      request.onerror = function() {
        errorMSG();
      };
      request.send();
    });
  });
}
