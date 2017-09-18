package main

import (
	"fmt"
	"log"
	"math/rand"
	"sync/atomic"
	"time"

	pb "../../../protocol/stream_manager"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

var Stat Count

type Count struct {
	recvCount uint64
	sendCount uint64
}

func (c *Count) addRecv() {
	atomic.AddUint64(&c.recvCount, 1)
}

func (c *Count) addSend() {
	atomic.AddUint64(&c.sendCount, 1)
}

func (c *Count) stat() {

	for {
		rate := 1.0
		if c.sendCount > 0 {
			if c.sendCount < c.recvCount {
				rate = 0.0
			} else {
				rate = float64(c.sendCount-c.recvCount) / float64(c.sendCount)
			}
		}

		startTime := time.Now().Unix()
		total_count_start := atomic.LoadUint64(&c.sendCount)

		time.Sleep(time.Second * 1)

		endTime := time.Now().Unix()
		total_count_end := atomic.LoadUint64(&c.sendCount)

		qps := float64(total_count_end - total_count_start)
		fmt.Println("start_time:", startTime, "end_time:", endTime, "send_count:", total_count_end, "qps:", qps, "avg_rate_loss:", 100.0*rate)
	}
}

func startClient(client pb.StreamManagerClient) {
	for i := 0; i < 100; i++ {
		go autoTestQueryInfo(client)
	}
}

func autoTestQueryInfo(client pb.StreamManagerClient) {
	for i := 0; i < 10000; i++ {
		req := &pb.QueryStreamInfoReq{
			Sequence:     rand.Int63(),
			StreamIDList: []string{"FWNligm13pJG5hayWYTXz7-SPxc="},
			//StreamIDList: []string{streamID},
		}
		//fmt.Printf("%#v\n", req)
		Stat.addSend()

		_, err := client.QueryStreamInfo(context.Background(), req)
		if err != nil {
			continue
		}

		Stat.addRecv()
	}

	//fmt.Printf("test succ!!\n")
}

func connect(addr string) pb.StreamManagerClient {
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		log.Fatal("did not connect: %v", err)
		return nil
	}
	client := pb.NewStreamManagerClient(conn)
	return client
}

func main() {
	go Stat.stat()

	client := connect("10.10.32.145:8087")
	go startClient(client)

	quit := make(chan bool)
	<-quit
}
