var sr = -1;
var sf = -1;

var game = null;

var team = "W";

var end = false;

var moves = [];

document.addEventListener("keydown", function(event) {
  if (end) return;
  if (event.keyCode == 32) {
    fetch("/api", {
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify({
        state: game,
        move: 0,
        team: team
      })
    }).then(response => response.json()).then(process);
    sr = -1;
    sf = -1;
  }
})

function clicked(r, f) {
  if (end) return;
  var old = document.getElementById("block" + sr + sf);
  if (old !== null) old.classList.remove("select-cell");
  if (sr == r && sf == f) {
    sr = -1;
    sf = -1;
  } else {
    if (sr == -1 && sf == -1) {
      var element = document.getElementById("block" + r + f);
      if (element !== null) element.classList.add("select-cell");
      sr = r;
      sf = f;
    } else {
      var move = [sr, sf, r, f];
      if (game[0][sr][sf][0] == "K" && sr == r && (r == 0 || r == 7) && sf == 4) {
        if (f == 6) {
          move.push(5);
        } else if (f == 2) {
          move.push(4);
        }
      }
      if (game[0][sr][sf][0] == "P" && (r == 0 || r == 7)) {
        while (true) {
          var promo = parseInt(prompt("Promotion! (0 = knight, 1 = bishop, 2 = rook, 3 = queen)"));
          if (0 <= promo && promo < 4) {
            move.push(promo);
            break;
          }
        }
      }
      fetch("/api", {
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify({
          state: game,
          move: move,
          team: team
        })
      }).then(response => response.json()).then(process);
      sr = -1;
      sf = -1;
    }
  }
}

function process(state) {
  if (load_state(state.result)) {
    toggle();
  }

  console.log(state.move);
  moves.push(state.move);

  if (state.win == 1) {
    alert("Checkmate!");
    end = true;
  } else if (state.win == -1) {
    alert("Stalemate!");
    end = true;
  }
}

var icon_map = {
  "": "",
  "KB": "&#x265A;",
  "QB": "&#x265B;",
  "RB": "&#x265C;",
  "BB": "&#x265D;",
  "NB": "&#x265E;",
  "PB": "&#x265F;",
  "KW": "&#x2654;",
  "QW": "&#x2655;",
  "RW": "&#x2656;",
  "BW": "&#x2657;",
  "NW": "&#x2658;",
  "PW": "&#x2659;"
}

function load_state(state) {
  if (state === false) return false;
  game = state;
  for (var r = 0; r < 8; r++) {
    for (var f = 0; f < 8; f++) {
      document.getElementById("cell" + r + f).innerHTML = icon_map[state[0][r][f]];
    }
  }
  return true;
}

function toggle() {
  if (team == "W") team = "B";
  else team = "W";
}

window.onload = function() {
  fetch("/get-state").then(response => response.json()).then(state => {
    load_state(state);
  });
};