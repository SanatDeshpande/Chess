function init() {
    initBoard();
    if (!window.location.href.includes("game")) {
        fetch("http://localhost:8000/init", {method: "GET"})
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            window.location.replace("http://localhost:8000/game/" + data["user"]["user_id"]);
        });
    } else {
        fetch("http://localhost:8000/game_state/" + getUserIdFromURL(), {method: "GET"})
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(data);
            refresh(data["board"]);
            return data;
        }).then(function(data) {
            document.getElementsByClassName("sharetext")[0].innerHTML = "<h1>Share Link for 2-Player:</h1>";
            var code = data["game_id"];
            var link = "http://localhost:8000/join/" + code + "/";
            var text = "<h3>" + link + " </h3>";
            document.getElementsByClassName("code")[0].innerHTML = text;
        });
    }
}

function getUserIdFromURL() {
    return window.location.href.split("game/")[1];
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

function refresh(board) {
    var row = document.getElementsByClassName("row");

    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            squares[j].innerHTML = numToUnicode(board[i][j]);
        }
    }
}

function highlight(board) {
    console.log("called");
    var row = document.getElementsByClassName("row");

    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            squares[j].style.backgroundColor = "22ff22";
        }
    }
    console.log("ended");
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
    selected = {
        "selected": [parseInt(e.parentElement.id), parseInt(e.id)],
    };
    fetch("http://localhost:8000/action/" + getUserIdFromURL() + "/",
    {
        method: "POST",
        body: JSON.stringify(selected)
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        highlight(data);
        console.log(data);
    });
}
