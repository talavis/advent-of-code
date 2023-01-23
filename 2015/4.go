package main

import (
	"crypto/md5"
	"fmt"
	"io/ioutil"
	"strconv"
)

func main() {
	i := 0
	input_key, _ := ioutil.ReadFile("4.txt")
	for {
		data := []byte(string(input_key) + strconv.Itoa(i))
		hash := md5.Sum(data)
		if hash[0] == 0 && hash[1] == 0 && hash[2] <= 0xF {
			break
		}
		i++
	}
	fmt.Printf("Part 1: %d\n", i)
	for {
		data := []byte(string(input_key) + strconv.Itoa(i))
		hash := md5.Sum(data)
		if hash[0] == 0 && hash[1] == 0 && hash[2] == 0 {
			break
		}
		i++
	}
	fmt.Printf("Part 2: %d\n", i)
}
