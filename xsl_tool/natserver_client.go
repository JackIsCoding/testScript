package main

import (
	"../../../protocol/s2s_protocol/natserver/"
	"../../src/xlvip"
	"errors"
	"github.com/golang/protobuf/proto"
	"log"
	"math/rand"
	"net"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"
)

type Count struct {
	recvCount uint64
	sendCount uint64
	recvTotal uint64
	sendTotal uint64
	statCount uint64
	mutex     sync.Mutex
}

func (c *Count) addRecv() {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.recvCount++
}

func (c *Count) addSend() {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.sendCount++
}

func (c *Count) reset() {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.recvCount = 0
	c.sendCount = 0
}

func (c *Count) stat() {
	c.mutex.Lock()
	defer c.mutex.Unlock()
	c.recvTotal += c.recvCount
	c.sendTotal += c.sendCount
	c.statCount++
	rate := 1.0
	if c.sendTotal != 0 {
		if c.sendTotal < c.recvTotal {
			rate = 0.0
		} else {
			rate = float64(c.sendTotal-c.recvTotal) / float64(c.sendTotal)
		}
	}
	log.Printf("send count:%d, recv count:%d, send total:%d, recv total:%d, avg_qps:%d, avg_loss_rate:%f%%\n", c.sendCount, c.recvCount, c.sendTotal, c.recvTotal, c.sendTotal/c.statCount, 100.0*rate)
}

func recv(socket *net.TCPConn) {
	factory := xlvip.NewFactory()
	for {
		header, body, err := factory.DecodeHeader(socket)
		if err != nil {
			log.Println("decode head", err)
			continue
		}

		switch header.Cmdid {
		case int(dp2pcomm_natserver.GetMySNResp_MESSAGE_TYPE):
			resp := &dp2pcomm_natserver.GetMySNResp{}
			if err = factory.Decode(body, resp); err != nil {
				log.Println("factory.Decode %#v err:%#V", resp, err)
			}

		case int(dp2pcomm_natserver.GetPeerSNResp_MESSAGE_TYPE):
			resp := &dp2pcomm_natserver.GetPeerSNResp{}
			if err = factory.Decode(body, resp); err != nil {
				log.Println("factory.Decode %#v err:%#V", resp, err)
			}

		default:
			continue

		}
		//if len(body) > 0 {
		//}

		Stat.addRecv()
	}
}

type ReqFunc func() ([]byte, error)

func getRandomPeerid() string {
	str := make([]byte, 16)
	for i := 0; i < 16; i++ {
		str[i] = strconv.FormatInt(int64(rand.Intn(16)), 16)[0]
	}
	return strings.ToUpper(string(str))
}

var seq int64

func inetAton(ipnr net.IP) uint32 {
	bits := strings.Split(ipnr.String(), ".")

	b0, _ := strconv.Atoi(bits[0])
	b1, _ := strconv.Atoi(bits[1])
	b2, _ := strconv.Atoi(bits[2])
	b3, _ := strconv.Atoi(bits[3])

	var sum uint32

	sum += uint32(b0) << 24
	sum += uint32(b1) << 16
	sum += uint32(b2) << 8
	sum += uint32(b3)

	return sum
}

func getMySnReq() ([]byte, error) {
	factory := xlvip.NewFactory()
	//req := new(dp2pcomm_natserver.GetMySNReq)
	req := &dp2pcomm_natserver.GetMySNReq{}
	req.Sequence = proto.Int64(seq)
	seq = seq + 1
	req.ProtocolVer = proto.Uint32(65)
	req.ClientIp = proto.Uint32(123456)
	req.Peerid = proto.String(getRandomPeerid())
	req.DisableSNs = append(req.DisableSNs, getRandomPeerid())
	req.Isp = dp2pcomm_natserver.ISP_TEL.Enum()
	buffer, err := factory.Encode(req, int(dp2pcomm_natserver.GetMySNReq_MESSAGE_TYPE))
	if err != nil {
		return nil, errors.New("get my sn encode fail")
	}

	return buffer, nil
}

func getPeerSnReq() ([]byte, error) {
	factory := xlvip.NewFactory()
	req := &dp2pcomm_natserver.GetPeerSNReq{}
	req.Sequence = proto.Int64(seq)
	seq = seq + 1
	req.ProtocolVer = proto.Uint32(65)
	req.ClientIp = proto.Uint32(123456)
	req.Peerid = proto.String(getRandomPeerid())
	req.Isp = dp2pcomm_natserver.ISP_TEL.Enum()

	buf, err := factory.Encode(req, int(dp2pcomm_natserver.GetPeerSNReq_MESSAGE_TYPE))
	if err != nil {
		return nil, errors.New("get peer sn pb encode fail")
	}
	return buf, nil
}

func send(socket *net.TCPConn, maxReq int) {
	var i int
	var buf []byte
	var err error
	reqFuncList := []ReqFunc{}
	reqFuncList = append(reqFuncList, getMySnReq)
	reqFuncList = append(reqFuncList, getPeerSnReq)
	//reqFuncList = append(reqFuncList, pingSNReq)
	//reqFuncList = append(reqFuncList, logoutReq)
	for num := maxReq; maxReq == 0 || num > 0; num-- {
		i = 0
		buf, err = reqFuncList[i%len(reqFuncList)]()
		if err == nil {
			n, err := socket.Write(buf)
			if err != nil || n != len(buf) {
				log.Println("send tcp packet fail,err:", err)
				time.Sleep(time.Second)
				continue
			}
			if i != 3 {
				Stat.addSend()
			}
		}
		//time.Sleep(1 * 1000 * 1000 * time.Nanosecond)
	}
}

func startClient(server string, maxReq int) {
	tcpAddr, err := net.ResolveTCPAddr("tcp4", server)
	if err != nil {
		log.Println("net.ResolveTCPAddr fail,", server)
		os.Exit(1)
	}
	conn, err := net.DialTCP("tcp", nil, tcpAddr)
	if err != nil {
		log.Println("connect tcp server fail,", server)
		os.Exit(1)
	}
	conn.SetKeepAlive(true)
	conn.SetKeepAlivePeriod(5 * time.Second)

	go recv(conn)
	go send(conn, maxReq)
}

var Stat Count

func main() {
	rand.Seed(time.Now().UnixNano())
	threadNum := 1
	maxReq := 0
	if len(os.Args) < 2 {
		log.Printf("usage:%s host:port,[host,port] thread_num max_request\n", os.Args[0])
		return
	}
	if len(os.Args) >= 3 {
		var err error
		threadNum, err = strconv.Atoi(os.Args[2])
		if err != nil || threadNum < 1 || threadNum > 100 {
			threadNum = 1
		}
	}
	if len(os.Args) >= 4 {
		var err error
		maxReq, err = strconv.Atoi(os.Args[3])
		if err != nil || maxReq <= 0 {
			maxReq = 0
		}

	}
	log.Println("thread num:", threadNum)
	Stat = *new(Count)

	startTime := time.Now().Unix()
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	go func() {
		sig := <-sigs
		log.Println(sig)
		endTime := time.Now().Unix()
		log.Println("============exit================time:", endTime-startTime)
		Stat.stat()
		os.Exit(0)
	}()
	defer func() {
		endTime := time.Now().Unix()
		log.Println("============exit================time:", endTime-startTime)
		Stat.stat()
	}()

	for _, v := range strings.Split(os.Args[1], ",") {
		for i := 0; i < threadNum; i++ {
			go startClient(v, maxReq)
		}
	}
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
