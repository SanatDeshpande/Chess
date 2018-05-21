class Piece {

    constructor(type, color, pos) {
        this.type = type;
        this.color = color;
        this.pos = pos;
        this.active = true; //all pieces active at start

        //generates appopriate symbol
        var num = 12;
        var pieces = ["K", "Q", "R", "B", "Kn", "P"];
        for (var i = 0; i < pieces.length; i++) {
            if (pieces[i] == type) {
                if (!color) {
                    num += 6; //for black pieces
                }
                this.symbol = "&#98" + num.toString();
                break;
            }
            num++;
        }
    }
}

function occupied(pos) {
    if (pos[0] < 0 || pos[0] > 7 || pos[1] < 0 || pos[1] > 7) {
        return null;
    }
    for (var i = 0; i < pieces.length; i++) {
        if (pieces[i].pos[0] == pos[0] && pieces[i].pos[1] == pos[1]) {
            return pieces[i].color;
        }
    }
    return null;
}

function pawnMoves(p) {
    var candidates = [];
    var shift = 1;
    if (p.color) {
        shift = -1;
    }

    var candidates = [];
    if (occupied([p.pos[0]+shift, p.pos[1]]) == null) {
        candidates.push([p.pos[0]+shift, p.pos[1]]);
        if (occupied([p.pos[0]+2*shift, p.pos[1]]) == null) {
            candidates.push([p.pos[0]+2*shift, p.pos[1]]);
        }
    }
    if (occupied([p.pos[0]+shift, p.pos[1]+1]) == (!p.color)) {
        candidates.push([p.pos[0]+shift, p.pos[1]+1]);
    }
    if (occupied([p.pos[0]+shift, p.pos[1]-1]) == (!p.color)) {
        candidates.push([p.pos[0]+shift, p.pos[1]-1]);
    }
    return candidates;
}

function bishopMoves(p) {
    
}



var pieces = [];

//returns a new piece
module.exports.piece = function(type, color, pos) {
    var p = new Piece(type, color, pos);
    pieces.push(p); //adds to collection of pieces
    return p;
}

module.exports.getMoves = function(pos) {
    var piece = null;

    for (var i = 0; i < pieces.length; i++) {
        if (pieces[i].pos[0] == pos[0] && pieces[i].pos[1] == pos[1]) {
            piece = pieces[i];
            break;
        }
    }
    if (piece == null) {
        return [];
    }
    if (piece.type == "P") {
        return pawnMoves(piece);
    }
    return [];
}


module.exports.pieceList = pieces;
