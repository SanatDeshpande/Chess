package tictactoe

import (
    "errors"
)

func Initialize() [][]int {
    board := make([][]int, 3)
    for i := range board {
        board[i] = make([]int, 3)
    }
    return board
}

func Mark(board [][]int, mark int, i int8, j int8) ([][]int, error) {
    if mark != -1 && mark != 1 {
        return nil, errors.New("Invalid Mark")
    }
    if i > 2 || i < 0 || j > 2 || j < 0 {
        return nil, errors.New("Out of Bounds")
    }
    if board[i][j] != 0 {
        return nil, errors.New("Invalid Selection")
    }

    board[i][j] = mark
    return board, nil
}

func Won(board [][]int) (int, error) {
    //Horizontal
    horizontal := 0
    vertical := 0
    for i := range board {
        for j := range board[i] {
            horizontal += board[i][j]
            vertical += board[j][i]
        }
        if horizontal == 3 {
            return 1, nil
        } else if horizontal == -3 {
            return -1, nil
        } else if vertical == 3 {
            return 1, nil
        } else if vertical == -3 {
            return -1, nil
        } else {
            horizontal = 0
            vertical = 0
        }
    }
    return 0, errors.New("No Winner")
}
