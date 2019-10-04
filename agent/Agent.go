package main

import (
    "math/rand"
    "fmt"
    "time"
)

type Agent struct {
    matrix [][]int
    activations map[int]func(float64)float64
    inputs int
    outputs int
}

func Initialize(inputs, outputs int) *Agent {
    max := 1000

    agent := new(Agent)
    agent.matrix = make([][]int, max)
    for i := range agent.matrix {
        agent.matrix[i] = make([]int, max)
    }

    agent.inputs = inputs
    agent.outputs = outputs

    //seed random
    rand.Seed(time.Now().UTC().UnixNano())

    for i := 0; i < outputs; i++ {
        from := rand.Intn(inputs)
        agent.matrix[from][max - i - 1] = 1
    }

    return agent
}

func add_node(agent *Agent) *Agent {
    //Get Source Node
    
    //Point to somewhere random w/ constraints
    //Make random source point to previously pointed
    //Make initial source point to random node
}

func main() {
    agent := Initialize(10, 3)
    for i := range agent.matrix {
        fmt.Println(agent.matrix[i])
    }
}
