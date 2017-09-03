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
}
function flatten(x, y) {
    return x * 8 + y;
}

function getMoves(piece) {
    if (piece.type == "Pawn") {
        return getPawnMoves(piece);
    }
}
function getPawnMoves(piece) {
    var currentX = piece.xPos;
    var currentY = piece.yPos;
    var possiblePositions = []
    var shift;
    if (!piece.isBlack) {
        shift = -1;
    } else {
        shift = 1;
    }
    if (!isOccupied([currentX + shift, currentY])) {
        possiblePositions.push([currentX + shift, currentY]);
        if (piece.position == piece.originalPosition && !isOccupied([currentX + shift*2, currentY])) {
            possiblePositions.push([currentX + shift*2, currentY]);
        }
    }
    if (isOccupied([currentX + shift, currentY + 1])) {
        possiblePositions.push([currentX + shift, currentY + 1]);
    }
    if (isOccupied([currentX + shift, currentY - 1])) {
        possiblePositions.push([currentX + shift, currentY - 1]);
    }
    return possiblePositions;
}
function getKingMoves(piece) {
    var xPos = piece.xPos;
    var yPos = piece.yPos;
}
function isOccupied(position) {
    var squares = document.getElementsByClassName("square");
    position = flatten(position[0], position[1]);
    for (var i in squares) {
        if (squares[i].innerHTML != "" && i == position) {
            return true;
        }
    }
    return false;
}
