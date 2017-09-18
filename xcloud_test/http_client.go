package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"sync"
        "os"
        "strconv"
	"encoding/json"
	"encoding/base64"
)

var succCount int
var failedCount int
var mu sync.Mutex

// host query response struct
type HostQueryRespHeader struct {
	Client_version string `json:"client_version"`
	Channel        string `json:"channel"`
	Sequence       int    `json:"sequence"`
	Result         int32  `json:"result"`
}

type HostQueryRespBody struct {
	Host       string   `json:"host"`
IpList []Ips  `json:"ips"`
}

type Ips struct {  
	Protocol string `json:"protocol"`
	Port     uint32 `json:"port"`
	Ip       string `json:"ip"` 

}

type HostQueryRespStruct struct {
	Header *HostQueryRespHeader `json:"header"`
	Data   string               `json:"data"` //base64(HostQueryRespBody)
}

func httpGet(reqPara string, maxReq int) bool {
	//resp, err := http.Get("http://10.10.67.110:801/xcloud/hostquery?version=1.0&channel=test1&seq=1001&host=auto.test.load.limit.com")
	//resp, err := http.Get("http://10.10.67.110:801/xcloud/hostquery?version=1&client_version=1.1.0&seq=1001&channel=ios_xunlei&host=auto.dynamic.test1.com")
	for i := 0; i < maxReq; i++ {
                //http://127.0.0.1:801/xcloud/hostquery?version=1&client_version=1.1.0&channel=test&seq=1001&host=aaa.com
                resp, err := http.Get(reqPara)
                if err != nil {
	                fmt.Printf("http get failed, err:%s", err)
		        continue
	                }
	        defer resp.Body.Close()
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			fmt.Printf("ReadAll failed, err:%s",err)
                	continue
			}	
		//fmt.Println(string(body))
		var responseData HostQueryRespStruct
		if json.Unmarshal(body, &responseData) != nil {
			fmt.Printf("json paser response data failed...")
			continue
		}
		fmt.Printf("responseData:%v", responseData)
		header := *(responseData.Header)
		if header.Result != 0 {
			fmt.Printf("Host query failed, result:%d\n\n", header.Result)
		}	
		var responseBody HostQueryRespBody
		bodyStr, _ := base64.StdEncoding.DecodeString(responseData.Data)
		if json.Unmarshal([]byte(bodyStr), &responseBody) != nil {
			fmt.Printf("json paser response body failed...")
		}
		fmt.Printf("header:%v\n", header)
		fmt.Printf("body:%v\n", responseBody)
        	}
		return true
	}

func main() {
    maxReq := 0
    maxReq, _ = strconv.Atoi(os.Args[2])    
    httpGet(os.Args[1],maxReq)
}
