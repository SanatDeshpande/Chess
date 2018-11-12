// var express = require('express')
// var app = express();
var app = require('express')();
var express = require('express');
var server = require('http').Server(app);
var io = require('socket.io')(server);


var PORT = process.env.PORT || 8000;

app.use(express.static(__dirname + "/static")); //lets us push js and css to client

app.get('/', function(req, res) {
    res.sendFile(__dirname + "/chess.html");
});

server.listen(PORT, function() {
    console.log("listening");
    console.log(PORT);
});
//-----------------//-----------------//-----------------//-----------------//-

// White >0 and Black <0
// Pawn = 1, Rook = 2, Bishop = 3, Knight = 4, Queen = 5, King = 6
// Empty = 0
var board = [[-2, -3, -4, -5, -6, -4, -3, -2],
             [-1, -1, -1, -1, -1, -1, -1, -1],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1],
             [2, 3, 4, 5, 6, 4, 3, 2]];
