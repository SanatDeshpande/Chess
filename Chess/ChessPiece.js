function ChessPiece(isBlack, xPos, yPos, type) {
    this.isBlack = isBlack;
    this.xPos = xPos;
    this.yPos = yPos;
    this.position = flatten(xPos, yPos);
    this.type = type;
    this.inPlay = true;
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
    this.movementRange = [
        this.forward,
        this.back,
        this.left,
        this.right
    ];
    this.forward = function() {
        this.x += this.shift;
        this.x = this.boundVal(this.x);
    }
    this.back = function() {
        this.x -= this.shift;
        this.x = this.boundVal(this.x);
    }
    this.left = function() {
        this.y -= this.shift;
        this.y = this.boundVal(this.y);
    }
    this.right = function() {
        this.y += this.shift;
        this.y = this.boundVal(this.y);
    }
    this.revert = function() {
        this.x = this.ogX;
        this.y = this.ogY;
    }
    this.getPositionArray = function() {
        return [this.x, this.y];
    }
    this.boundVal =  function(val) {
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
    if (piece === null) {
        return;
    }
    if (piece.type == "Pawn") {
        return getPawnMoves(piece);
    } else if (piece.type == "King") {
        return getKingMoves(piece);
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
