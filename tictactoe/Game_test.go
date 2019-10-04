package tictactoe

import (
    "testing"
)

func TestInitialize(t *testing.T) {
    got := Initialize()
    for i := range got {
        for j := range got[i] {
            if got[i][j] != 0 {
                t.Errorf("Index %d, %d was %d", i, j, got[i][j])
            }
        }
    }
}

func TestWrongMark (t *testing.T) {
    init_board := Initialize()
    _, err := Mark(init_board, 2, 0, 1)
    if err == nil {
        t.Errorf("Incorrect mark check not working")
    }
}

func TestOutOfBounds (t *testing.T) {
    init_board := Initialize()
    _, err := Mark(init_board, -1, 3, 0)
    if err == nil {
        t.Errorf("out of bounds check not working")
    }
}

func TestSelection (t *testing.T) {
    init_board := Initialize()
    board, err := Mark(init_board, 1, 0, 1)
    board, err = Mark(board, -1, 0, 1)
    if err == nil {
        t.Errorf("double selection not working")
    }
}

func TestMark (t *testing.T) {
    init_board := Initialize()

    board, _ := Mark(init_board, 1, 0, 1)
    if board[0][1] != 1 {
        t.Errorf("mark not registering")
    }

    board, _ = Mark(board, -1, 2, 2)
    if board[2][2] != -1 {
        t.Errorf("mark not registering")
    }
}

func TestWon (t *testing.T) {
    board := Initialize()

    winner, err := Won(board)
    if err == nil {
        t.Errorf("Empty winning board")
    }

    board, err = Mark(board, 1, 0, 0)
    winner, err = Won(board)
    if err == nil {
        t.Errorf("No-win board is winning")
    }

    board, err = Mark(board, 1, 0, 1)
    board, err = Mark(board, -1, 1, 0)
    winner, err = Won(board)
    if err == nil {
        t.Errorf("No-win board is winning")
    }

    board, err = Mark(board, 1, 0, 2)
    winner, err = Won(board)
    if err == nil {
        if winner != 1 {
            t.Errorf("Wrong winner reported")
        }
    } else {
        t.Errorf("Didn't detect winning board")
    }
}
