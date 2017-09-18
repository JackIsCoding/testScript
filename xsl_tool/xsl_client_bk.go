package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

type Param struct {
	Page int  `json:"page"`
	Size int  `json:"size"`
}

type Data struct {
	Guid     string    `json:"guid"`
	Userid   string    `json:"userid"`
	Appid    string    `json:"appid"`
	Position string    `json:"position"`
	ClientV  string    `json:"clientV"`
	Trace    string    `json:"trace"`
	Params   Param     `json:"params"`
}

type Datalice struct {
	My_datas []Data
}

func Send_post() {

	my_param := Param{
		Page: 10,
		Size: 10,
	}

	my_data := Data{
		Guid:     "2c29f5b154909aef3ebe3b9210",
		Userid:   "111",
		Appid:    "46",
		Position: "index",
		ClientV:  "1.1",
		Trace:    "1000000",
		Params:   my_param,
	}

	url := "http://tw06600.sandai.net:7000/api/shenzhen/shoulei/1"
	fmt.Println("my_data:", my_data)
	b, err := json.Marshal(my_data)
	if err != nil {
		panic(err)
		return
	}
	fmt.Println("b:", len(b))
	body := bytes.NewBuffer([]byte(b))
	fmt.Println("body:", body)
	resp, _ := http.Post(url, "application/json;charset=utf-8", body)
	result, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
		return
	}
	resp.Body.Close()

	fmt.Println("result:\n", string(result))
}

func main() {
	Send_post()

}
