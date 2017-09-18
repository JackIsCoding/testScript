package main

import (
	"../../../protocol/p2s_protocol/p2s"
	"errors"
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

func recv(socket *net.UDPConn) {
	data := make([]byte, 1024)
	for {
	START:
		n, _, err := socket.ReadFromUDP(data)
		if err != nil {
			log.Println("error recv data", err)
			time.Sleep(time.Second)
			continue
		}
		head, body, err := p2sFactory.DecodeHeader(data[:n])
		if err != nil {
			log.Println("p2sFactory.DecodeHeader", err)
			continue
		}
		var p2sResp p2s.Command
		switch head.CmdId {
		case p2s.GetMySnRespType:
			resp := &p2s.GetMySnResp{}
			resp.Head = *head
			p2sResp = resp
		case p2s.GetPeerSnRespType:
			resp := &p2s.GetPeerSnResp{}
			resp.Head = *head
			p2sResp = resp
		case p2s.PingSnRespType:
			resp := &p2s.PingSnResp{}
			resp.Head = *head
			p2sResp = resp
		case p2s.ICallSomeOneRespType:
			resp := &p2s.ICallSomeOneResp{}
			resp.Head = *head
			p2sResp = resp
		case p2s.UdpBrokeRespType:
			resp := &p2s.UDPBrokeResp{}
			resp.Head = *head
			p2sResp = resp
		case p2s.TcpBrokeRespType:
			resp := &p2s.TCPBrokeResp{}
			resp.Head = *head
			p2sResp = resp
		default:
			log.Println("unknown cmd", head.CmdId)
			goto START
		}
		err = p2sFactory.Decode(body, p2sResp)
		if err != nil {
			log.Println("p2sFactory.Decode %#v err:%#V", p2sResp, err)
		} else {
			//log.Printf("%#v", p2sResp)
		}

		log.Printf("recv from %#v\n", p2sResp)
		Stat.addRecv()
	}
}

var p2sFactory p2s.Factory

type ReqFunc func() ([]byte, error)

func getRandomPeerid() string {
	str := make([]byte, 16)
	for i := 0; i < 16; i++ {
		str[i] = strconv.FormatInt(int64(rand.Intn(16)), 16)[0]
	}
	return strings.ToUpper(string(str))
}

func getMySnReq() ([]byte, error) {
	req := p2s.NewGetMySnReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.GetMySnReqType
	req.PeerId = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func getPeerSnReq() ([]byte, error) {
	req := p2s.NewGetPeerSnReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.GetPeerSnReqType
	req.PeerId = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func pingSNReq() ([]byte, error) {
	req := p2s.NewPingSnReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.PingSnReqType
	req.Head.EncryType = 1
	req.PeerID = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func logoutReq() ([]byte, error) {
	req := p2s.NewNN2SNLogout()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.NN2SNLogoutType
	req.PeerID = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func ICallSomeOneReq() ([]byte, error) {
	req := p2s.NewICallSomeOneReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.ICallSomeOneReqType
	req.LocalPeerID = getRandomPeerid()
	req.RemotePeerID = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func UDPBrokeReq() ([]byte, error) {
	req := p2s.NewUDPBrokeReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.UdpBrokeReqType
	req.RequestorPeerID = getRandomPeerid()
	req.RemotePeerID = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func TCPBrokeReq() ([]byte, error) {
	req := p2s.NewTCPBrokeReq()
	req.Head.Ver = 66
	req.Head.CmdId = p2s.TcpBrokeReqType
	req.RemotePeerID = getRandomPeerid()
	buf, err := p2sFactory.Encode(req)
	if err != nil {
		return nil, errors.New("p2sFactory.Encode fail")
	}
	return buf, nil
}

func send(socket *net.UDPConn, maxReq int, funcname string) {
	var i int
	var buf []byte
	var err error
	reqFuncList := []ReqFunc{}
	switch funcname {
        case "getMySnReq":
            reqFuncList = append(reqFuncList, getMySnReq)
        case "getPeerSnReq":
            reqFuncList = append(reqFuncList, getPeerSnReq)
        case "pingSNReq":
            reqFuncList = append(reqFuncList, pingSNReq)
        case "logoutReq":
            reqFuncList = append(reqFuncList, logoutReq)  
        case "ICallSomeOneReq":
            reqFuncList = append(reqFuncList, ICallSomeOneReq)
        case "UDPBrokeReq":
            reqFuncList = append(reqFuncList, UDPBrokeReq)
        case "TCPBrokeReq":
            reqFuncList = append(reqFuncList, TCPBrokeReq)
        default:
            reqFuncList = append(reqFuncList, getMySnReq)
            reqFuncList = append(reqFuncList, getPeerSnReq)
            reqFuncList = append(reqFuncList, pingSNReq)
            reqFuncList = append(reqFuncList, logoutReq)
            reqFuncList = append(reqFuncList, ICallSomeOneReq)
            reqFuncList = append(reqFuncList, UDPBrokeReq)
            reqFuncList = append(reqFuncList, TCPBrokeReq)
       
        }
        //reqFuncList = append(reqFuncList, getMySnReq)
	//reqFuncList = append(reqFuncList, getPeerSnReq)
	//reqFuncList = append(reqFuncList, pingSNReq)
	//reqFuncList = append(reqFuncList, logoutReq)
	//reqFuncList = append(reqFuncList, ICallSomeOneReq)
	//reqFuncList = append(reqFuncList, UDPBrokeReq)
	//reqFuncList = append(reqFuncList, TCPBrokeReq)
	for num := maxReq; maxReq == 0 || num > 0; num-- {
		i = 1
		buf, err = reqFuncList[i%len(reqFuncList)]()
		if err == nil {
			n, err := socket.Write(buf)
			if err != nil || n != len(buf) {
				log.Println("send udp packet fail,err:", err)
				time.Sleep(time.Second)
				continue
			}
			if i != 3 {
				Stat.addSend()
			}
		}
		time.Sleep(time.Duration(rand.Intn(64)) * time.Millisecond)
	}
}

func startClient(server string, maxReq int,funcname string) {
	addr, err := net.ResolveUDPAddr("udp", server)
	if err != nil {
		log.Println("net.ResolveUDPAddr fail.", err)
		os.Exit(1)
	}

	socket, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		log.Println("net.DialUDP fail.", err)
		os.Exit(1)
	}
	socket.SetReadBuffer(24 * 1024)
	socket.SetWriteBuffer(24 * 1024)
	go recv(socket)
	go send(socket, maxReq,funcname)
}

var Stat Count

func main() {
	rand.Seed(time.Now().UnixNano())
	threadNum := 1
	maxReq := 0
        funcname := "default"
	if len(os.Args) < 2 {
		log.Printf("usage:%s host:port,[host,port] thread_num max_request\n", os.Args[0])
		return
	}
	if len(os.Args) >= 3 {
		var err error
		threadNum, err = strconv.Atoi(os.Args[2])
		if err != nil || threadNum < 1 || threadNum > 100000 {
			threadNum = 1
		}
	}
        if len(os.Args) >= 4 {
               var err error
               maxReq, err = strconv.Atoi(os.Args[3]) 

               if err != nil {
               maxReq = 1
               }       
        }

	if len(os.Args) >= 5 {
		//var err error
		//maxReq, err = strconv.Atoi(os.Args[3])
		//if err != nil || maxReq <= 0 {
		//	maxReq = 0
		//}
                funcname = os.Args[4]
                log.Printf("use press for %s\n",funcname)

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
			go startClient(v, maxReq,funcname)
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
