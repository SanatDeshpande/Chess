package main

import (
    "math/rand"
    "fmt"
    "time"
)

type Agent struct {
    matrix [][]int
    inputs int
    outputs int
}

func Initialize(inputs, outputs int) *Agent {
    max := 30

    agent := new(Agent)
    agent.matrix = make([][]int, max)
    for i := range agent.matrix {
        agent.matrix[i] = make([]int, max)
    }

    agent.inputs = inputs
    agent.outputs = outputs

    //seed random

    for i := 0; i < outputs; i++ {
        from := randint(inputs)
        agent.matrix[from][max - i - 1] = 1
    }

    return agent
}

func main() {
    agent := Initialize(10, 3)
    for i := range agent.matrix {
        fmt.Println(agent.matrix[i])
    }
    addNode(agent)
}
