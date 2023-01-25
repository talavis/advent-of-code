package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func getCoord(sCoord string) (int, int) {
	parts := strings.Split(sCoord, ",")
	coordX, _ := strconv.Atoi(parts[0])
	coordY, _ := strconv.Atoi(parts[1])
	return coordX, coordY
}

func main() {
	file, _ := os.Open("6.txt")
	scanner := bufio.NewScanner(file)

	var lamps [1_000_000]bool
	var lampsB [1_000_000]int

	for scanner.Scan() {
		parts := strings.Split(scanner.Text(), " ")
		var startX, startY, endX, endY int
		var op string
		if parts[0] == "toggle" {
			startX, startY = getCoord(parts[1])
			endX, endY = getCoord(parts[3])
			op = "t"
		} else {
			startX, startY = getCoord(parts[2])
			endX, endY = getCoord(parts[4])
			if parts[1] == "on" {
				op = "n"
			} else {
				op = "f"
			}
		}
		for y := startY * 1000; y <= (endY * 1000); y = y + 1000 {
			aoi := lamps[y+startX : y+endX+1]
			aoiB := lampsB[y+startX : y+endX+1]
			for i := 0; i < len(aoi); i++ {
				if op == "n" {
					aoi[i] = true
					aoiB[i]++
				} else if op == "f" {
					aoi[i] = false
					aoiB[i]--
					if aoiB[i] < 0 {
						aoiB[i] = 0
					}
				} else {
					aoi[i] = !aoi[i]
					aoiB[i] = aoiB[i] + 2
				}
			}
		}
	}

	total := 0
	for i := 0; i < len(lamps); i++ {
		if lamps[i] {
			total++
		}
	}

	fmt.Printf("Part 1: %d\n", total)

	brightness := 0
	for i := 0; i < len(lampsB); i++ {
		brightness = brightness + lampsB[i]
	}

	fmt.Printf("Part 2: %d\n", brightness)
}
