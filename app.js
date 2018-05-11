var express = require('express')
var app = express();
app.use(express.static(__dirname + "/static"));

app.get('/', function(req, res) {
    res.sendFile(__dirname + "/chess.html");
});

app.listen(8000, function() {
    console.log("listening");
});
