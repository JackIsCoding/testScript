package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	//"net"
        "net/http"
        //"time"
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

func Send_post(ch chan int) {
    var ch_total_num int = 0
    Guid_count := len(Guid_list)
    for i:=0;i<1000;i++{
        HERE:
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

	url := "http://tw06600.sandai.net:7000/api/shenzhen/shoulei/1"
	b, err := json.Marshal(my_data)
	if err != nil {
                Fail_num++
		goto HERE
	}
	body := bytes.NewBuffer([]byte(b))
        ch_total_num++
        //from here
        /*req, err := http.NewRequest("POST", url, body)
        if err != nil{
            Fail_num++
            goto HERE
        }
        req.Header.Set("Content-Type","application/json")
        req.Header.Set("Conection","Keep-alive")
        Client := http.Client{
        Transport: &http.Transport{
            Dial: func(netw, url string) (net.Conn, error){
                deadline := time.Now().Add(3 * time.Second)
                c,err := net.DialTimeout(netw, url, time.Second*3)
                if err != nil{
                   Fail_num++
                   return nil, err
                   //goto HERE
                   }
                c.SetDeadline(deadline)
                return c,nil
                },
            },
        }	
        resp, err := Client.Do(req)*/

        //from here
        resp, err := http.Post(url, "application/json;charset=utf-8", body)
        if err != nil{
                Fail_num++
                goto HERE
        }
	result, err := ioutil.ReadAll(resp.Body)
	if err != nil{
               Fail_num++
               goto HERE
        }
	resp.Body.Close()
        //fmt.Println(string(result))
        if string(result)[1:11] == "\"code\":\"0\""{
            Success_num++
        }else{
            Fail_num++
        }
    }
    ch <- ch_total_num
}

func main() {
        Get_guid("guid.data")
        chs := make([]chan int, 500)
        for i := 0;i<100;i++{
            chs[i] = make(chan int)
            go Send_post(chs[i])
         }
        for _,ch := range(chs){
            num := <-ch
            fmt.Println("ch_total_num:",num)
        }
        fmt.Println("Total_num:",Total_num,"Sucess_num:",Success_num,"Fail_num:",Fail_num)
}
