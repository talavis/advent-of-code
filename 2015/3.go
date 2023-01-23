package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
)

func main() {
	dat, _ := ioutil.ReadFile("3.txt")
	visited := make(map[string]bool)
	x_pos := 0
	y_pos := 0
	s_pos := strconv.Itoa(x_pos) + "," + strconv.Itoa(y_pos)
	visited[s_pos] = true
	for _, c := range dat {
		switch string(c) {
		case "^":
			y_pos++
		case "v":
			y_pos--
		case ">":
			x_pos++
		case "<":
			x_pos--
		}
		s_pos := strconv.Itoa(x_pos) + "," + strconv.Itoa(y_pos)
		visited[s_pos] = true
	}

	fmt.Printf("Part 1: %d\n", len(visited))

	visited_2 := make(map[string]bool)
	x_pos_1 := 0
	y_pos_1 := 0
	x_pos_2 := 0
	y_pos_2 := 0

	s_pos_start := strconv.Itoa(x_pos_1) + "," + strconv.Itoa(y_pos_1)
	visited_2[s_pos_start] = true
	for i, c := range dat {
		switch string(c) {
		case "^":
			if i%2 == 0 {
				y_pos_1++
			} else {
				y_pos_2++
			}
		case "v":
			if i%2 == 0 {
				y_pos_1--
			} else {
				y_pos_2--
			}
		case ">":
			if i%2 == 0 {
				x_pos_1++
			} else {
				x_pos_2++
			}

		case "<":
			if i%2 == 0 {
				x_pos_1--
			} else {
				x_pos_2--
			}
		}
		s_pos_1 := strconv.Itoa(x_pos_1) + "," + strconv.Itoa(y_pos_1)
		s_pos_2 := strconv.Itoa(x_pos_2) + "," + strconv.Itoa(y_pos_2)
		visited_2[s_pos_1] = true
		visited_2[s_pos_2] = true
	}

	fmt.Printf("Part 2: %d\n", len(visited_2))
}
