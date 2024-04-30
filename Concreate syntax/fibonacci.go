package main

import "fmt"

func main() {
	n := 10
	if n <= 0 {
		fmt.Println(0)
	} else {
		previous := 0
		current := 1
		if n == 1 {
			fmt.Println(1)
		} else {
			for i := 2; i <= n; i++ {
				next := previous + current
				previous = current
				current = next
			}
			fmt.Println(current)
		}
	}
}
