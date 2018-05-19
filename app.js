// var express = require('express')
// var app = express();
var app = require('express')();
var express = require('express');
var server = require('http').Server(app);
var io = require('socket.io')(server);

app.use(express.static(__dirname + "/static")); //lets us push js and css to client

app.get('/', function(req, res) {
    res.sendFile(__dirname + "/chess.html");
});

server.listen(8000, function() {
    console.log("listening");
});

io.on('connection', function(socket) {
    socket.on("test", function(data) {
        console.log(socket.id);
    })
})
