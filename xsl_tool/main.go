package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	type ColorGroup struct {
		ID     int
		Name   string
		Colors []string
	}
	group := ColorGroup{
		ID:     1,
		Name:   "Reds",
		Colors: []string{"Crimson", "Red", "Ruby", "Maroon"},
	}
	b, err := json.Marshal(group)
	if err != nil {
		fmt.Println("error:", err)
	}
	fmt.Println(string(b))

	type Data struct {
		Guid string
	}

	{
		data := Data{
			Guid: "abc",
}
		b, err := json.Marshal(data)
		if err != nil {
			fmt.Println("error:", err)
		}
		fmt.Println(string(b))
	}

}
