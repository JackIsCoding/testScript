package main

import (
	//"encoding/base64"
	//"fmt"
	//"io/ioutil"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"sync/atomic"
	"syscall"
	"time"
)

var Stat Count

type Count struct {
	recvCount uint64
	sendCount uint64
	recvTotal uint64
	sendTotal uint64
	statCount uint64
}

func (c *Count) addRecv() {
	atomic.AddUint64(&c.recvCount, 1)
}

func (c *Count) addSend() {
	atomic.AddUint64(&c.sendCount, 1)
}

func (c *Count) reset() {
	atomic.StoreUint64(&c.recvCount, 0)
	atomic.StoreUint64(&c.sendCount, 0)
}

func (c *Count) stat() {
	recvCount := atomic.LoadUint64(&c.recvCount)
	sendCount := atomic.LoadUint64(&c.sendCount)
	recvTotal := atomic.AddUint64(&c.recvTotal, recvCount)
	sendTotal := atomic.AddUint64(&c.sendTotal, sendCount)
	statCount := atomic.AddUint64(&c.statCount, 1)
	rate := 1.0
	if sendTotal != 0 {
		if sendTotal < recvTotal {
			rate = 0.0
		} else {
			rate = float64(sendTotal-recvTotal) / float64(sendTotal)
		}
	}
	log.Printf("send count:%d, recv count:%d, send total:%d, recv total:%d, avg_qps:%d, avg_loss_rate:%f%%\n", sendCount, recvCount, sendTotal, recvTotal, sendTotal/statCount, 100.0*rate)
}

func httpGet(reqPara string, maxReq int) {
	for i := 0; i < maxReq; i++ {
		//http://127.0.0.1:801/xcloud/hostquery?version=1&client_version=1.1.0&channel=test&seq=1001&host=aaa.com
		_, err := http.Get(reqPara)
		Stat.addSend()
		if err != nil {
			continue

		}
		Stat.addRecv()
		/*	if err != nil {
				fmt.Printf("Http-get request failed, err:%s\n\n", err)
				continue
			}
			defer resp.Body.Close()
			Stat.addSend()
			body, err := ioutil.ReadAll(resp.Body)
			if err != nil {
				fmt.Printf("ReadAll failed, err:%s\n\n", err)
				continue
			}
			Stat.addRecv()
			//fmt.Println(string(body))
			var responseData HostQueryRespStruct
			if json.Unmarshal(body, &responseData) != nil {
				fmt.Printf("Json paser response data failed...\n\n")
				continue
			}
			//fmt.Printf("responseData:%v", responseData)
			header := *(responseData.Header)
			if header.Result != 0 {
				fmt.Printf("Host query failed, result:%d\n\n", header.Result)
			}
			/*continue

			var responseBody HostQueryRespBody
			bodyStr, _ := base64.StdEncoding.DecodeString(responseData.Data)
			if json.Unmarshal([]byte(bodyStr), &responseBody) != nil {
				fmt.Printf("json paser response body failed...")
				continue
			}
			fmt.Printf("header:%v\n", header)
			fmt.Printf("body:%v\n", responseBody)
		*/
	}
}

func startClient(reqPara string, goNum int, maxReq int) {
	for i := 0; i < goNum; i++ {
		go httpGet(reqPara, maxReq)
	}
}

func main() {
	var err error
	threadNum := 1
	maxReq := 0
	reqPara := "http://10.10.32.143:8101/httpdown?id=1234&g=1111111111111111111111111111111111111111"
	if len(os.Args) >= 3 {
		if threadNum, err = strconv.Atoi(os.Args[1]); err != nil || threadNum < 1 || threadNum > 10000 {
			threadNum = 1
		}
		if maxReq, err = strconv.Atoi(os.Args[2]); err != nil || maxReq <= 0 {
			maxReq = 0
		}

	}
	log.Printf("thread num:%d max req:%d\n", threadNum, maxReq)
	Stat = *new(Count)

	startTime := time.Now().Unix()
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM, syscall.SIGPIPE)
	go func() {
		sig := <-sigs
		if sig != syscall.SIGPIPE {
			log.Println(sig)
			endTime := time.Now().Unix()
			log.Println("============exit================time:", endTime-startTime)
			Stat.stat()
			os.Exit(0)
		}
	}()
	defer func() {
		endTime := time.Now().Unix()
		log.Println("============exit================time:", endTime-startTime)
		Stat.stat()
	}()

	go startClient(reqPara, threadNum, maxReq)
	t := time.NewTimer(time.Second)
	for {
		select {
		case <-t.C:
			Stat.stat()
			if Stat.sendCount <= 0 && Stat.recvCount <= 0 {
				time.Sleep(time.Second)
				return
			}
			Stat.reset()
			t.Reset(time.Second)
		}
	}
}
