// var express = require('express')
// var app = express();
var app = require('express')();
var express = require('express');
var server = require('http').Server(app);
var io = require('socket.io')(server);

var chess = require('./Piece.js')
var turn = true; //initially white's turn

app.use(express.static(__dirname + "/static")); //lets us push js and css to client

app.get('/', function(req, res) {
    res.sendFile(__dirname + "/chess.html");
});

server.listen(8000, function() {
    console.log("listening");
});

io.on('connection', function(socket) {
    socket.on("init", function(data) {
        //init pawns
        for (var i = 0; i < 8; i++) {
            chess.piece("P", false, [1,i]);
            chess.piece("P", true, [6,i]);
        }
        //init king/queen
        chess.piece("K", false, [0,3]);
        chess.piece("K", true, [7,3]);
        chess.piece("Q", false, [0,4]);
        chess.piece("Q", true, [7,4]);
        //init bishop
        chess.piece("B", false, [0,2]);
        chess.piece("B", false, [0,5]);
        chess.piece("B", true, [7,2]);
        chess.piece("B", true, [7,5]);
        //init knight
        chess.piece("Kn", false, [0,1]);
        chess.piece("Kn", false, [0,6]);
        chess.piece("Kn", true, [7,1]);
        chess.piece("Kn", true, [7,6]);
        //init rook
        chess.piece("R", false, [0,0]);
        chess.piece("R", false, [0,7]);
        chess.piece("R", true, [7,0]);
        chess.piece("R", true, [7,7]);

        //debug
        chess.piece("Kn", false, [3, 3])
        //io.to(socket.id).emit("update", chess.pieceList);
        socket.emit("update", chess.pieceList);
    });

    socket.on("getMoves", function(pos) {
        var moves = chess.getMoves(pos); //gets coordinates of legit moves
        //io.to(socket.id).emit("update");
        socket.emit("update", moves);
    });
});
