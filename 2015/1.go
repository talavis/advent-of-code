package main

import "fmt"
import "io/ioutil"

func main() {
	dat, _ := ioutil.ReadFile("1.txt")
	first_neg := -1
	floor := 0
	for i, c := range dat {
		switch string(c) {
		case "(":
			floor++
		case ")":
			floor--
		}
		if first_neg < 0 && floor < 0 {
			first_neg = i + 1
		}
	}
	fmt.Printf("Part 1: %d\n", floor)
	fmt.Printf("Part 2: %d\n", first_neg)
}
