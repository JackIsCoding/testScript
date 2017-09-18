package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net"
        "net/http"
        "time"
        "os"
        "bufio"
        "strings"
        "math/rand"
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

var Total_num int = 0
var Fail_num int = 0
var Success_num int = 0
var Guid_list = make([]string,0) 
func Get_guid(file_path string){
        fi,err := os.Open(file_path)
        if err != nil{panic(err)}
        defer fi.Close() 
        buf := bufio.NewReader(fi)
        for{
             line,err := buf.ReadString('\n')
             line = strings.TrimSpace(line)
             Guid_list = append(Guid_list,string(line))
             if err != nil{
                 return
             }
        }
}

func Post_client(network, url string)(net.Conn, error){
        dial := net.Dialer{
        Timeout:    30 * time.Second,
        KeepAlive:  30 * time.Second,
    }
    
    conn,err := dial.Dial(network,url)
    if err != nil{
        return conn,err
    }
    fmt.Println("connect done, use", conn.LocalAddr().String())
    
    fmt.Println("HI22")
    return conn,err

}

func DoPost(client *http.Client, url string, param Data){
    b, err := json.Marshal(param)
    if err != nil {
            Fail_num++
	}
    body := bytes.NewBuffer([]byte(b))
    resp,err := client.Post(url,"application/json;charset=utf-8",body)
    result, err := ioutil.ReadAll(resp.Body)
    if err != nil{
           Fail_num++
    }
    fmt.Println("HI")
    resp.Body.Close()
    fmt.Println(string(result))

}

func Send_post(ch chan int) {
    client := &http.Client{
    Transport: &http.Transport{
        Dial: Post_client,
        },
    }

    req_num := 1000
    ch_total_num := 0
    Guid_count := len(Guid_list)
    url := "http://tw06600.sandai.net:7000/api/shenzhen/shoulei/1"
    for i:=0;i<req_num;i++{
        Total_num = Total_num + 1
        Num := rand.Intn(Guid_count)
	my_param := Param{
		Page: 10,
		Size: 10,
	}

	my_data := Data{
		Guid:     Guid_list[Num],
		Userid:   "111",
		Appid:    "46",
		Position: "index",
		ClientV:  "1.1",
		Trace:    "1000000",
		Params:   my_param,
	}

        go DoPost(client,url,my_data)
    }
    ch <- ch_total_num
}

func main() {
        Get_guid("guid.data")
        chs := make([]chan int, 500)
        for i := 0;i<2;i++{
            chs[i] = make(chan int)
            go Send_post(chs[i])
         }
        for _,ch := range(chs){
            num := <-ch
            fmt.Println("ch_total_num:",num)
        }
        fmt.Println("Total_num:",Total_num,"Sucess_num:",Success_num,"Fail_num:",Fail_num)
}
