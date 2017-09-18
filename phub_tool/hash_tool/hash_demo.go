package main

import (
	"fmt"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func randomPeerid() string {
	str := make([]byte, 16)
	for i := 0; i < 16; i++ {
		str[i] = strconv.FormatInt(int64(rand.Intn(16)), 16)[0]
	}
	return strings.ToUpper(string(str))
}

func peeridHashCode(peerid string) uint32 {
	var result int32 = 1
	for i := 0; i < 16; i++ {
		result = 31*result + int32(peerid[i])
	}

	return uint32(math.Abs(float64(result)))
}

func peeridHashCodeEx(peerid string) uint32 {
	var num uint32
	num += uint32(peerid[0]) << 24
	num += uint32(peerid[1]) << 16
	num += uint32(peerid[10]) << 8
	num += uint32(peerid[11])
	return num
}

func main() {
	ratio, _ := strconv.Atoi(os.Args[1])
	fmt.Printf("ratio:%d\n", ratio)
	quit := make(chan bool)
	go func() {
		for {
			peerid := randomPeerid()
			hash := peeridHashCodeEx(peerid)
			m := hash%100
			//if m < uint32(ratio) {
			if m == uint32(ratio) {
				fmt.Printf("%s\n", peerid)
			}
		}
	}()

	<-quit
}
