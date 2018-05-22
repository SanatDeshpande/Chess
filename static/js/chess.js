function init() {
    initBoard();
    var socket = io();
    socket.emit("init", "ready");

    socket.on("update", function(data) {
        refresh(data);
    });
}

function getMoves(e) {
    var socket = io();
    var pos = [parseInt(e.parentElement.id), parseInt(e.id)];
    socket.emit("getMoves", pos);
    socket.on("update", function(moves) {
        highlight(moves);
    });
}

function highlight(moves) {
    var row = document.getElementsByClassName("row");
    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            for (var k = 0; k < moves.length; k++) {
                if (moves[k][0] == i && moves[k][1] == j) {
                    squares[j].style.backgroundColor = "#229922";
                }
            }
        }
    }
}


function refresh(pieces) {
    var row = document.getElementsByClassName("row");
    for (var i = 0; i < pieces.length; i++) {
        if (!pieces[i].active) {
            continue; //ignores captured pieces
        }
        var pos = pieces[i].pos;
        var square = row[pos[0]].getElementsByClassName("square")[pos[1]];
        square.innerHTML = pieces[i].symbol;
    }
}

function initBoard() {
    var row = document.getElementsByClassName("row");
    var black = false;

    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            if (black) {
                squares[j].style.backgroundColor = "#888888";
            } else {
                squares[j].style.backgroundColor = "#ffffff";
            }
            black = !black;
        }
        black = !black;
    }
}
