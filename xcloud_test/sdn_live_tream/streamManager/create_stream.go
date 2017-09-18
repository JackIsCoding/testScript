package main

import (
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	pb "../../../../protocol/stream_manager"
	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

func registerSignal() {
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM, syscall.SIGPIPE)
	go func() {
		for {
			sig := <-sigs
			if sig != syscall.SIGPIPE {
				log.Print(sig, "=================EXIT============")
				os.Exit(1)
			}
		}
	}()
}

func GenerateRangeNum(min, max int64) int64 {
	rand.Seed(time.Now().Unix())
	randNum := rand.Int63n(max-min) + min
	return randNum
}

func doRequest(client pb.StreamManagerClient, args []string) {
	switch args[0] {
	case "CreateStream":
		streamKey := "xunlei"
		streamName := "test"
		streamType := "flv"
		businessID := GenerateRangeNum(10000, 20000)
		urlSuffixS := strings.Split(args[1], ",")
		length := (len(urlSuffixS))
		log.Printf("urlSuffixS:%v", urlSuffixS)
		log.Printf("length:%d", length)
		i := int(1)
		for _, urlSuffix := range urlSuffixS {
			if i <= length {
				log.Printf("urlSuffix:%s", urlSuffix)
				pullUrl := "rtmp://rtmp.stream2.show.xunlei.com/live/" + urlSuffix
				log.Printf("pullUrl:%v", pullUrl)
				req := &pb.CreateStreamInternalReq{
					Sequence:   rand.Int63(),
					BusinessID: businessID,
					StreamKey:  streamKey,
					StreamName: streamName,
					StreamType: streamType,
					PullUrl:    pullUrl,
				}
				fmt.Printf("req:%#v\n", req)
				resp, err := client.CreateStreamInternal(context.Background(), req)
				fmt.Printf("err:%v resp:%v\n", err, resp)
			}
			businessID = businessID + 1
			i = i + 1
		}
	case "CreateStreamInternal":
		streamKey := "xunlei"
		streamName := "testInter"
		streamType := "flv"
		businessID := GenerateRangeNum(10, 100)
		urlSuffixS := strings.Split(args[1], ",")
		length := (len(urlSuffixS))
		log.Printf("urlSuffixS:%v", urlSuffixS)
		log.Printf("length:%d", length)
		i := int(1)
		for _, urlSuffix := range urlSuffixS {
			if i <= length {
				log.Printf("urlSuffix:%s", urlSuffix)
				pullUrl := "rtmp://rtmp.stream2.show.xunlei.com/live/" + urlSuffix
				log.Printf("pullUrl:%v", pullUrl)
				req := &pb.CreateStreamInternalReq{
					Sequence:   rand.Int63(),
					BusinessID: businessID,
					StreamKey:  streamKey,
					StreamName: streamName,
					StreamType: streamType,
					PullUrl:    pullUrl,
				}
				fmt.Printf("req:%#v\n", req)
				resp, err := client.CreateStreamInternal(context.Background(), req)
				fmt.Printf("err:%v resp:%v\n", err, resp)
			}
			businessID = businessID + 1
			i = i + 1
		}
	default:
		log.Print("unkonwn request:", args[0:])
		return
	}
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

func usage() {
	if len(os.Args) == 3 && os.Args[2] == "CreateStream" {
		return
	} else if len(os.Args) == 3 && os.Args[2] == "CreateStreamInternal" {
		return
	} else if len(os.Args) < 4 {
		log.Printf(`usage:%s host:port ...
			---------------------------------------------------------------------------------------------------------------------------------------------------
			| CreateStream      | pullUrl_Suffix(example:7125_561667036,4117_655380780)
			| CreateStreamInternal    | pullUrl_Suffix(example:7125_561667036,4117_655380780)
			---------------------------------------------------------------------------------------------------------------------------------------------------
		`, os.Args[0])
		os.Exit(0)
	}
}

func main() {
	usage()
	rand.Seed(time.Now().Unix())
	client := connect(os.Args[1])
	doRequest(client, os.Args[2:])
}
