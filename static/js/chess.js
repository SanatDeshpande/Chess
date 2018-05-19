function init() {
    initBoard();
    var socket = io();
    socket.emit("test", "client side data");
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
