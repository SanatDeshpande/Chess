var state = null;

function init() {
    initBoard();
    fetch("http://localhost:8000/init", {method: "GET"})
    .then(function(response) {
        return response.json()
    })
    .then(function(data) {
        state = data;
        refresh(state["board"]);
    });
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
    var row = document.getElementsByClassName("row");

    for (var i = 0; i < row.length; i++) {
        var squares = row[i].getElementsByClassName("square");
        for (var j = 0; j < squares.length; j++) {
            squares[j].style.backgroundColor = "22ff22";
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
    request = {
        "state": state,
        "selected": [parseInt(e.parentElement.id), parseInt(e.id)],
    };

    fetch("http://localhost:8000/action/",
    {
        method: "POST",
        body: JSON.stringify(request)
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        //TODO
    });
}
