package main

import (
	"fmt"
	"math"
	"os"
)

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
	hash := peeridHashCodeEx(os.Args[1])
	fmt.Printf("hash:%d\n", hash)
	fmt.Printf("m:%d\n", hash%100)
}
