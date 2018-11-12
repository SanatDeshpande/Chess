function init() {
    initBoard();
}

/*
    Possible statuses:
    1. My turn, idle
        -highlight possible moves
    2. Their turn
        -do nothing
    3. My turn, highlighted
        -move, do nothing, or revert highlightedness
*/



function requestAction(e) {
    console.log(e);
}

function highlight(moves) {
    console.log(moves);
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
