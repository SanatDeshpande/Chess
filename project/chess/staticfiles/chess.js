function init() {
    initBoard();
    fetch("http://localhost:8000/test", {method: "GET"})
    .then(function(response) {
        return response.json()
    })
    .then(function(data) {
        console.log(data["response_data"]);
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

function requestAction(element) {
    alert("action");
}
