function init() {
    initBoard();
    if (!window.location.href.includes("game")) {
        fetch("http://localhost:5000/init", {method: "GET"})
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            window.location.replace("http://localhost:5000/game/" + data["user"]["user_id"]);
        });
    } else {
        fetch("http://localhost:5000/game_state/" + getUserIdFromURL(), {method: "GET"})
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            setInterval(refresh, 2000);
            return data;
        }).then(function(data) {
            console.log(data);
            if (!data['full']) {
                document.getElementsByClassName("sharetext")[0].innerHTML = "<h1>Share Link for 2-Player:</h1>";
                var code = data["game_id"];
                var link = "http://localhost:5000/join/" + code + "/";
                var text = "<h3>" + link + " </h3>";
                document.getElementsByClassName("code")[0].innerHTML = text;
            }
        });
    }
}

function getUserIdFromURL() {
    return window.location.href.split("game/")[1];
}

function getGameIdFromUrl() {
    return window.location.href.split("join/")[1];
}

function initBoard() {
    var row = document.getElementsByClassName("row");
    var black = true;

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

function refresh() {
    fetch("http://localhost:5000/game_state/" + getUserIdFromURL(), {method: "GET"})
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data['user']['white'] && data['white_checkmate'] == true) {
            alert('YOU WON');
        } else if (!data['user']['white'] && data['white_checkmate'] == false) {
            alert('YOU WON');
        } else if (data['user']['white'] && data['white_checkmate'] == false) {
            alert('YOU LOST');
        } else if (!data['user']['white'] && data['white_checkmate'] == true) {
            alert('YOU LOST');
        }

        board = data["board"];
        var row = document.getElementsByClassName("row");

        for (var i = 0; i < row.length; i++) {
            var squares = row[i].getElementsByClassName("square");
            for (var j = 0; j < squares.length; j++) {
                squares[j].innerHTML = numToUnicode(board[i][j]);
            }
        }
    });
}

function highlight(board) {
    var row = document.getElementsByClassName("row");
    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            if (board[i][j] == 1) {
                squares[j].style.backgroundColor = "#22ff22";
            } else if (board[i][j] == 2) {
                squares[j].style.backgroundColor = "#ff2222";
            }
        }
    }
}

function numToUnicode(num) {
    if (num == 0) {
        return "";
    }
    if (num < 0) {
        num *= -1;
        num += 6;
    }
    num += 11;
    return "&#98" + num.toString();
}

function unicodeToNum(code) {
    if (code == "") {
        return 0;
    }

    var num = code.substring(code.length-2, code.length);

    if (num <= 17) {
        num -= 11;
    } else {
        num -= 17;
        num *= -1;
    }
    return num;
}


function requestAction(e) {
    //really, it's to request highlight
    selected = {
        "selected": [parseInt(e.parentElement.id), parseInt(e.id)],
    };
    fetch("http://localhost:5000/action/" + getUserIdFromURL() + "/",
    {
        method: "POST",
        body: JSON.stringify(selected),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        initBoard();
        highlight(data["highlight"]);
        console.log(data);
    });

    //registers checkmate status
    fetch("http://localhost:5000/checkmate/" + getUserIdFromURL() + "/", {method: "GET"});
}
