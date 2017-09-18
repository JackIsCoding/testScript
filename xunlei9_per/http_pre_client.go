package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	//"net"
        "net/http"
        "time"
        "os"
        "bufio"
        "strings"
        "math/rand"
	"strconv"
	"sync/atomic"
)

type Data struct{
	Group_id int64 `json:"group_id"`
	Uid int64 `json:"uid"`
	Rate int `json:"rate"`
	Ul_total int `json:"ul_total"`
	Ul_time int `json:"ul_time"`
	Dl_speed int `json:"dl_speed"`
}

type Report_param struct{
	My_data []Data `json:"data"`
}

var Send_req_num_total uint64 = 0
var Send_req_num_fail uint64 = 0
var Send_req_num_success uint64 = 0
var Response_time_total uint64 = 0
var Uid_list = make([]string,0)
var Group_list = make([]string,0)
var Task_list = make([]string,0)
var Task_count int = 0
var Uid_count int = 0
var Group_count int = 0 
func Get_task(file_path string){
        fi,err := os.Open(file_path)
        if err != nil{panic(err)}
        defer fi.Close() 
        buf := bufio.NewReader(fi)
        for{
             line,err := buf.ReadString('\n')
             line = strings.TrimSpace(line)
             Task_list = append(Task_list,string(line))
             if err != nil{
                 return
             }
        }
}

func Get_uid(file_path string){
        fi,err := os.Open(file_path)
        if err != nil{panic(err)}
        defer fi.Close() 
        buf := bufio.NewReader(fi)
        for{
             line,err := buf.ReadString('\n')
             line = strings.TrimSpace(line)
             Uid_list = append(Uid_list,string(line))
             if err != nil{
                 return
             }
        }
}

func Get_group_id(file_path string){
        fi,err := os.Open(file_path)
        if err != nil{panic(err)}
        defer fi.Close() 
        buf := bufio.NewReader(fi)
        for{
             line,err := buf.ReadString('\n')
             line = strings.TrimSpace(line)
             Group_list = append(Group_list,string(line))
             if err != nil{
                 return
             }
        }
}

func Send_get(ch chan uint64,get_type string){
    if get_type == "motorcade_list"{
        for i:=0;i<100000;i++{
	    HERE1:
            the_task_num := rand.Intn(Task_count-1)
	    atomic.AddUint64(&Send_req_num_total,1)
	    url := fmt.Sprintf("http://pre.api-shoulei-ssl.xunlei.com/group_accel/motorcade_list?task=%s",Task_list[the_task_num])
	    response_time_start := time.Now().Unix()
	    resp, err := http.Get(url)
	    response_time_end := time.Now().Unix()
	    response_time := uint64(response_time_end - response_time_start)
	    atomic.AddUint64(&Response_time_total,response_time)
	    if err != nil{
		atomic.AddUint64(&Send_req_num_fail,1)
		goto HERE1
	    }
	    result, err := ioutil.ReadAll(resp.Body)
	    if err != nil{
		atomic.AddUint64(&Send_req_num_fail,1)
		goto HERE1
	    }
            if strings.Contains(string(result),"\"result\":\"ok\""){
		atomic.AddUint64(&Send_req_num_success,1)
	    }else{
		//fmt.Println("motorcade_list error result:",string(result))
		atomic.AddUint64(&Send_req_num_fail,1)
	    }
	    defer resp.Body.Close()
	}
    ch <- Send_req_num_total
    }else if get_type == "motorcade_mem"{
	for i:=0;i<100000;i++{
	    HERE2:
	    the_uid_num := rand.Intn(Uid_count-1)
	    the_group_num := rand.Intn(Group_count-1)
	    atomic.AddUint64(&Send_req_num_total,1)
	    url := fmt.Sprintf("http://pre.api-shoulei-ssl.xunlei.com/group_accel/motorcade_mem?group_id=%s&uid=%s",Group_list[the_group_num],Uid_list[the_uid_num])
	    response_time_start := time.Now().Unix()
	    resp, err := http.Get(url)
	    response_time_end := time.Now().Unix()
	    response_time := uint64(response_time_end - response_time_start)
	    atomic.AddUint64(&Response_time_total,response_time)
	    if err != nil{
		atomic.AddUint64(&Send_req_num_fail,1)
                goto HERE2
	    }
	    result, err := ioutil.ReadAll(resp.Body)
	    if err != nil{
		atomic.AddUint64(&Send_req_num_fail,1)
		goto HERE2
	    }
	    resp.Body.Close()
            if strings.Contains(string(result),"\"result\":\"ok\"") || strings.Contains(string(result),"\"result\":\"not exist group\""){
		atomic.AddUint64(&Send_req_num_success,1)
	    }else{
		atomic.AddUint64(&Send_req_num_fail,1)
		//fmt.Println("motorcade_mem error result:",string(result))
		}
	}
    ch <- Send_req_num_total
    }else{
	fmt.Println("url error!")
        ch <- 0
    }

}

func Send_post(ch chan uint64) {
    for i:=0;i<100000;i++{
        HERE:
        atomic.AddUint64(&Send_req_num_total,1)
        //group_id := rand.Int63n(1000000)
        //user_id := rand.Int63n(1000000)
	the_uid_num := rand.Intn(Uid_count-1)
	the_group_num := rand.Intn(Group_count-1)
        group_id,_ := strconv.ParseInt(Group_list[the_group_num],10,0)
        uid,_ := strconv.ParseInt(Uid_list[the_uid_num],10,0)
	var my_data []Data

	my_data = append(my_data, Data{
		Group_id:    group_id,
		Uid:   uid,
		Rate: 80,
		Ul_total:  81920,
		Ul_time:    320,
		Dl_speed:   356,
	})

	post_data := Report_param{
		My_data:     my_data,
	}
	url := "http://pre.api-shoulei-ssl.xunlei.com/group_accel/report_batch?timestamp=1491459146&accesskey=ios.m.xunlei&sig=jKO_dw3zRCTSWFtDOitbbrQKIyM="
	b, err := json.Marshal(post_data)
	if err != nil {
                atomic.AddUint64(&Send_req_num_fail,1)
		goto HERE
	}
	body := bytes.NewBuffer([]byte(b))

        //from here
	response_time_start := time.Now().Unix()
        resp, err := http.Post(url, "application/json;charset=utf-8", body)
	response_time_end := time.Now().Unix()
	response_time := uint64(response_time_end - response_time_start)
	atomic.AddUint64(&Response_time_total,response_time)
        if err != nil{
                atomic.AddUint64(&Send_req_num_fail,1)
                goto HERE
        }
	result, err := ioutil.ReadAll(resp.Body)
	if err != nil{
               atomic.AddUint64(&Send_req_num_fail,1)
               goto HERE
        }
	resp.Body.Close()
        if strings.Contains(string(result),"\"result\":\"ok\""){
            atomic.AddUint64(&Send_req_num_success,1)
        }else{
            atomic.AddUint64(&Send_req_num_fail,1)
		fmt.Println("report_batch error result:",string(result))
        }
    }
    ch <- Send_req_num_total
}

func Stat(){
	for{
		// before 1s
		start_time := time.Now().Unix()
		total_count_start := atomic.LoadUint64(&Send_req_num_total)
		success_count_start := atomic.LoadUint64(&Send_req_num_success)
		resp_time_start := atomic.LoadUint64(&Response_time_total)
		time.Sleep(time.Second*1)

		//after 1s
		end_time := time.Now().Unix()
		total_count_end := Send_req_num_total
		success_count_end := Send_req_num_success
		resp_time_end := Response_time_total
		qps := float64(total_count_end-total_count_start)/1.0
		avg_resp_time := fmt.Sprintf("%.2f",(float64(resp_time_end-resp_time_start)*1000)/float64(total_count_end-total_count_start))
		success_rate := fmt.Sprintf("%f%%",float64(success_count_end-success_count_start)/float64(total_count_end-total_count_start)*100)
		fmt.Println("start_time:",start_time,"end_time:",end_time,"QPS:",qps,"success_rate:",success_rate,"avg_resp_time:",avg_resp_time)
	}

}

func main() {
	Get_task("task.data")
	Get_uid("uid.data")
	Get_group_id("group_id.data")
        Uid_count = len(Uid_list)
        Group_count = len(Group_list)
        Task_count = len(Task_list)
        chs := make([]chan uint64, 240)
        for i := 0;i<240;i++{
            chs[i] = make(chan uint64)
	    if i%6 == 0 || i%6 == 1 || i%6 == 2{
                go Send_post(chs[i])
		fmt.Println("Send_Post,id:",i)
            }
	    if i%6 == 3 || i%6 == 4{
                go Send_get(chs[i],"motorcade_mem")
		fmt.Println("Send_get_mem,id:",i)
            }
            if i%6 == 5{
		go Send_get(chs[i],"motorcade_list")
		fmt.Println("Send_get_list,id:",i)
	    }
		//go Send_get(chs[i],"motorcade_list")
                //go Send_post(chs[i])
                //go Send_get(chs[i],"motorcade_mem")
         }
	go Stat()
        for _,ch := range(chs){
            _ = <-ch
	    return
        }
}
