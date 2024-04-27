package main

import "fmt"

func main() {
    x := 5  
    ans := 1

    for x > 1 {
        ans = ans * x
        x = x - 1
    }
    
    fmt.Println(ans)
}