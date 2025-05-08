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

function setSocket() {
  var id = uuid();
  console.log(id);
  var socket = new WebSocket("ws://"+ document.domain +":8000/websocket");

  socket.addEventListener("message", (event) => {
    console.log("msg:", event.data);
    try {
      var data  = JSON.parse(event.data);
      var tbody = ""
      for (const [key, value] of Object.entries(data)) {
        console.log(key, value);
        if (key == 'text') {
          var v = decodeURIComponent(JSON.parse(value))
          tbody = tbody + "<tr><td>"+ key +"</td><td>"+ v +"</td></td>";
        } else {
          tbody = tbody + "<tr><td>"+ key +"</td><td>"+ value +"</td></td>";
        }
        document.querySelector("#res").innerHTML = tbody;
      }
    } catch (error) {
      var m = {};
    }
    if (data['rands']) {
      rands = data['rands'].map((pair) => pair.join('_ON_D')
                                              .replace(/(\d{1,})(\d{1,})_ON_D100/, "$1_ON_D10, $2_ON_D10")
                                              .replace(/(\d{1,})_ON_D100/, "0_ON_D10, $1_ON_D10"))
                           .join(', ');
      console.log(rands);

      document.querySelector("#response").innerHTML = rands;

    }
  });

  // socket.onopen = function(event) {
    // var msg = JSON.stringify({"id": id, "msg": "register", "to": "host", "path": window.location.pathname});
    // socket.send(msg);
    // var key = getParameterByName("key", location.href);
    // socket.send(JSON.stringify({"msg": "checkLock", "id": id, "lvl": 1, "data": key, "to": "host"}));
  // };
  return socket;
};

document.addEventListener("DOMContentLoaded", function() {
  var socket = setSocket();

  body = document.querySelectorAll("body")[0];
  body.addEventListener("click", function(e) {
    target = e.target;
    if (target.className == "button") {
      val = document.querySelector("input").value
      socket.send(val);
    }
  });
})
