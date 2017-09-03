var pieces = new Array();

function handleClick(sq) {
    var found = false;
    for (var i in pieces) {
        if (sq.id == pieces[i].position) {
            mapNextMoves(pieces[i]);
            found = true;
            break;
        }
    }
    if (!found) {
        mapNextMoves(null);
    }
}

function mapNextMoves(piece) {
    var squares = document.getElementsByClassName("square");
    var positions = getMoves(piece);
    for (var i = 0; i < squares.length; i++) {
        if (squares[i].style.backgroundColor == "rgb(0, 255, 0)") {
            var row = Math.floor((i / 8) % 2);
            if (row % 2 == 0) {
                if (i % 2 == 0) {
                    squares[i].style.backgroundColor = "#ffffff";
                } else {
                    squares[i].style.backgroundColor = "#888888";
                }
            } else {
                if (i % 2 == 0) {
                    squares[i].style.backgroundColor = "#888888";
                } else {
                    squares[i].style.backgroundColor = "#ffffff";
                }
            }
        }
    }
    for (var i in positions) {
        var x = positions[i][0];
        var y = positions[i][1];
        if (x <= 7 && x >= 0 && y <= 7 && y >= 0) {
            squares[x * 8 + y].style.backgroundColor = "#00ff00";
        }
    }
}

// Creates board
function initBoard() {
    var square;
    var board = document.getElementsByClassName("chessboard");
    var black = false;
    for (var i = 0; i < 8; i++) {
        for (var j = 0; j < 8; j++) {
            square = document.createElement("div");
            square.className = "square";
            if (black) {
                square.style.backgroundColor = "#888888";
            } else {
                square.style.backgroundColor = "#ffffff";
            }
            square.onclick = function () {handleClick(this);};
            square.id = (8 * i + j)
            black = !black;
            board[0].appendChild(square);
        }
        black = !black;
    }
    populateBoard();
}


function populateBoard() {
    var squares = document.getElementsByClassName("square");
    pieces.push(new ChessPiece(false, 3, 0, "King"));
    pieces.push(new ChessPiece(false, 2, 1, "King"));
    //initialize pawns
    for (var i = 0; i < 8; i++) {
        pieces.push(new ChessPiece(true, 1, i, "Pawn"));
        pieces.push(new ChessPiece(false, 6, i, "Pawn"));
    }
    //initialize Rooks
    pieces.push(new ChessPiece(true, 0, 0, "Rook"));
    pieces.push(new ChessPiece(true, 0, 7, "Rook"));
    pieces.push(new ChessPiece(false, 7, 0, "Rook"));
    pieces.push(new ChessPiece(false, 7, 7, "Rook"));
    //Initialize Bishops
    pieces.push(new ChessPiece(true, 0, 2, "Bishop"));
    pieces.push(new ChessPiece(true, 0, 5, "Bishop"));
    pieces.push(new ChessPiece(false, 7, 2, "Bishop"));
    pieces.push(new ChessPiece(false, 7, 5, "Bishop"));
    //Initialize Knights
    pieces.push(new ChessPiece(true, 0, 1, "Knight"));
    pieces.push(new ChessPiece(true, 0, 6, "Knight"));
    pieces.push(new ChessPiece(false, 7, 1, "Knight"));
    pieces.push(new ChessPiece(false, 7, 6, "Knight"));
    //Queen and King
    pieces.push(new ChessPiece(true, 0, 3, "King"));
    pieces.push(new ChessPiece(true, 0, 4, "Queen"));
    pieces.push(new ChessPiece(false, 7, 3, "King"));
    pieces.push(new ChessPiece(false, 7, 4, "Queen"));
    for (var i in pieces) {
        squares[pieces[i].position].innerHTML = pieces[i].encoding;
    }
}
