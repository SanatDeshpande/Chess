function ChessPiece(isBlack, xPos, yPos, type) {
    this.isBlack = isBlack;
    this.xPos = xPos;
    this.yPos = yPos;
    this.position = flatten(xPos, yPos);
    this.type = type;
    this.inPlay = true;
    this.selected = false;
    this.encoding = "&#";
    var encodingMap = {"King" : 9812,
                       "Queen": 9813,
                       "Rook": 9814,
                       "Bishop": 9815,
                       "Knight": 9816,
                       "Pawn": 9817};
    if (isBlack) {
        this.encoding += encodingMap[type] + 6;
    } else {
        this.encoding += encodingMap[type];
    }

    if (type == "Pawn") {
        this.originalPosition = this.position;
    }
    this.move = function(newPos) {
        this.position = newPos;
        this.xPos = newPos / 8;
        this.yPos = newPos % 8;
    }
    this.getPosObj = function() {
        return new posObj(this.xPos, this.yPos, this.isBlack);
    }
}
function posObj(x, y, isBlack) {
    this.x = x;
    this.y = y;
    this.ogX = this.x;
    this.ogY = this.y;
    this.isBlack = isBlack;
    this.shift = 1;
    if (!this.isBlack) {
        this.shift = -1;
    }
    this.names = ["forward", "back", "left", "right", "forwardRight",
                  "forwardLeft", "backRight", "backLeft"];
    this.callFunction = function(name) {
        if (name == "forward") {
            this.forward();
        } else if (name == "back") {
            this.back();
        } else if (name == "right") {
            this.right();
        } else if (name == "left") {
            this.left();
        } else if (name == "forwardRight") {
            this.forward();
            this.right();
        } else if (name == "forwardLeft") {
            this.forward();
            this.left();
        } else if (name == "backRight") {
            this.back();
            this.right();
        } else if (name == "backLeft") {
            this.back();
            this.left();
        }
    }
    this.forward = function() {
        this.x += this.shift;
        this.x = boundVal(this.x);
    }
    this.back = function() {
        this.x -= this.shift;
        this.x = boundVal(this.x);
    }
    this.left = function() {
        this.y -= this.shift;
        this.y = boundVal(this.y);
    }
    this.right = function() {
        this.y += this.shift;
        this.y = boundVal(this.y);
    }
    this.revert = function() {
        this.x = this.ogX;
        this.y = this.ogY;
    }
    this.getPositionArray = function() {
        return [this.x, this.y];
    }
    var boundVal =  function(val) {
        if (val > 7) {
            return 7;
        } else if (val < 0) {
            return 0;
        } else {
            return val;
        }
    }
}
function flatten(x, y) {
    return x * 8 + y;
}

function getMoves(piece) {
    if (piece === null || !piece.inPlay) {
        return;
    }
    if (piece.type == "Pawn") {
        return getPawnMoves(piece);
    } else if (piece.type == "King") {
        return getKingMoves(piece);
    } else if (piece.type == "Queen") {
        return getQueenMoves(piece);
    } else if (piece.type == "Bishop") {
        return getBishopMoves(piece);
    } else if (piece.type == "Rook") {
        return getRookMoves(piece);
    } else if (piece.type == "Knight") {
        return getKnightMoves(piece);
    }
}
function getPawnMoves(piece) {
    var possiblePositions = [];
    var pos = piece.getPosObj();
    pos.forward();
    if (getPieceColor(pos.x, pos.y) == !piece.isBlack) {
        possiblePositions.push(pos.getPositionArray());
    } else if (!isOccupied(pos.x, pos.y)) {
        possiblePositions.push(pos.getPositionArray());
        pos.forward();
        if (getPieceColor(pos.x, pos.y) == !piece.isBlack || !isOccupied(pos.x, pos.y)) {
            possiblePositions.push(pos.getPositionArray());
        }
    }
    pos.revert();
    pos.forward();
    var pos2 = new posObj(pos.x, pos.y, pos.isBlack);
    pos.left();
    if (getPieceColor(pos.x, pos.y) == !piece.isBlack) {
        possiblePositions.push(pos.getPositionArray());
    }
    pos2.right();
    if (getPieceColor(pos2.x, pos2.y) == !piece.isBlack) {
        possiblePositions.push(pos2.getPositionArray());
    }
    return possiblePositions;
}
function getKingMoves(piece) {
    var possiblePositions = [];
    var pos = piece.getPosObj();
    for (var i in pos.names) {
        pos.callFunction(pos.names[i]);
        if (getPieceColor(pos.x, pos.y) == !piece.isBlack || !isOccupied(pos.x, pos.y)) {
            possiblePositions.push(pos.getPositionArray());
        }
        pos.revert();
    }
    return possiblePositions;
}
function getQueenMoves(piece) {
    // debugger;
    return bishopRookQueenHelper(piece, true, true);
}
function getBishopMoves(piece) {
    // debugger;
    return bishopRookQueenHelper(piece, true, false);
}
function getRookMoves(piece) {
    return bishopRookQueenHelper(piece, false, true);
}
function bishopRookQueenHelper(piece, isDiagonal, isHorizontal) {
    var possiblePositions = []
    var pos = piece.getPosObj();
    for (var i = 0; i < pos.names.length; i++) {
        if (pos.names[i].toLowerCase() == pos.names[i] && !isHorizontal) {
            continue;
        }
        if (pos.names[i].toLowerCase() != pos.names[i] && !isDiagonal) {
            continue;
        }
        pos.callFunction(pos.names[i]);
        while (!isOccupied(pos.x, pos.y)) {
            possiblePositions.push(pos.getPositionArray());
            pos.callFunction(pos.names[i]);
            if (pos.x == 0 || pos.x == 7 || pos.y == 0 || pos.y == 7) {
                break;
            }
        }
        if (getPieceColor(pos.x, pos.y) == !piece.isBlack || !isOccupied(pos.x, pos.y)) {
            possiblePositions.push(pos.getPositionArray());
        }
        pos.revert();
    }
    return possiblePositions;
}
function getKnightMoves(piece) {
    var possiblePositions = [];
    var pos = piece.getPosObj();
    var shift = [
        [2,-1],
        [2,1],
        [-2,-1],
        [-2,1],
    ];
    for (var i = 0; i < shift.length; i++) {
        var x = pos.x + shift[i][0];
        var y = pos.y + shift[i][1];
        if (x < 0 || x > 7 || y < 0 || y > 7) {
            continue;
        }
        for (var j = 0; j < 2; j++) {
            if (getPieceColor(x, y) == !piece.isBlack || !isOccupied(x, y)) {
                possiblePositions.push([x, y]);
            }
            x = pos.x + shift[i][1];
            y = pos.y + shift[i][0];
        }
    }
    return possiblePositions;
}
function isOccupied(x, y) {
    var occupied = getPieceColor(x, y);
    return occupied != null;
}
function getPieceColor(x, y) {
    var position = flatten(x, y);
    for (var i in pieces) {
        if (pieces[i].position == position) {
            return pieces[i].isBlack;
        }
    }
    return null;
}
