package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
)

func main() {
	triVovel := regexp.MustCompile(`[aeiou].*[aeiou].*[aeiou]`)
	hasUnwantedWord := regexp.MustCompile(`ab|cd|pq|xy`)

	file, _ := os.Open("5.txt")
	scanner := bufio.NewScanner(file)

	nice := 0

	for scanner.Scan() {
		word := []byte(scanner.Text())
		if !triVovel.Match(word) || hasUnwantedWord.Match(word) {
			continue
		}
		last := byte(0)
		for _, b := range word {
			if b == last {
				nice += 1
				break
			}
			last = b
		}
	}

	fmt.Printf("Part 1: %d\n", nice)

	file, _ = os.Open("5.txt")
	scanner = bufio.NewScanner(file)

	nice = 0
	for scanner.Scan() {
		word := scanner.Text()
		reps := make(map[string]int)
		rep2 := false
		for i := 1; i < len(word); i++ {
			identifier := string(word[i-1 : i+1])
			if reps[identifier] > 0 {
				if reps[identifier] < i-1 {
					rep2 = true
					break
				}
			} else {
				reps[identifier] = i
			}
		}
		gap_rep := false
		for i := 1; i < len(word)-1; i++ {
			if word[i-1] == word[i+1] {
				gap_rep = true
				break
			}
		}
		if rep2 && gap_rep {
			nice++
		}
	}

	fmt.Printf("Part 2: %d\n", nice)
}
