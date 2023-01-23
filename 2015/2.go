package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	file, _ := os.Open("2.txt")

	scanner := bufio.NewScanner(file)
	paper := 0
	ribbon := 0
	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), "x")

		vals := make([]int, len(parts))
		for i, s := range parts {
			vals[i], _ = strconv.Atoi(s)
		}
		sort.Ints(vals)
		sides := []int{vals[0] * vals[1], vals[0] * vals[2], vals[1] * vals[2]}
		smallest := sides[0]
		for _, side := range sides {
			if smallest > side {
				smallest = side
			}
			paper = paper + 2*side
		}

		ribbon = ribbon + 2*vals[0] + 2*vals[1] + vals[0]*vals[1]*vals[2]
		paper = paper + smallest
	}

	fmt.Printf("Part 1: %d\n", paper)
	fmt.Printf("Part 2: %d\n", ribbon)
}
