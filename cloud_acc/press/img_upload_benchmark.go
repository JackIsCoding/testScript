package main

import (
	"bytes"
	"crypto/md5"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"math/rand"
	"mime/multipart"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

var lock *sync.RWMutex

var success int64

func GetMD5ToLower(aimStr string) string {
	return strings.ToLower(fmt.Sprintf("%x", md5.Sum([]byte(aimStr))))
}

func GenGcid() string {
	str := "0123456789abcdef"
	bytes := []byte(str)
	result := []byte{}
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	for i := 0; i < 40; i++ {
		result = append(result, bytes[r.Intn(len(bytes))])
	}
	return strings.ToUpper(string(result))
}

func UploadData(path, url string) int {
	lock.RLock()
	defer lock.RUnlock()
	resGcid := GenGcid()
	str := resGcid + "1ABC123"
	sign := GetMD5ToLower(str)
	url = url + "upload?res_gcid=" + resGcid + "&img_type=1&sign=" + sign
	//fmt.Println(url)
	f, err := os.Open(path)
	defer f.Close()
	if err != nil {
		fmt.Printf("Open file %s failed %v\n", path, err)
		return 0
	}
	body := &bytes.Buffer{}
	bodyWriter := multipart.NewWriter(body)
	fileWriter, err := bodyWriter.CreateFormFile("img", path)
	if err != nil {
		fmt.Println("Create Form file failed", err)
		return 0
	}
	_, err = io.Copy(fileWriter, f)
	contentType := bodyWriter.FormDataContentType()
	bodyWriter.Close()
	resp, err := http.Post(url, contentType, body)
	if err != nil {
		return 0
	}
	//fmt.Println(resp.Status)
	if resp.Status == "200 OK" {
		return 1
	}
	return 0
}

func Task(path, url string, wg *sync.WaitGroup) {
	defer wg.Done()
	ff := UploadData(path, url)
	if ff != 1 {
		fmt.Printf("upload_data failed\n")
		return
	}
	success++
}

/*func main() {
	url := "http://10.10.191.2:8801/upload?"
	path := "./data/test.flv"
	UploadData(path, url)
}*/

func main() {
	url := flag.String("url", "http://10.10.191.2:8801/", "Uploader server host")
	count := flag.Int("count", 10, "Concurrency counts")
	dir := flag.String("dir", "./data", "Waiting for the uploaded file directory")
	flag.Parse()

	lock = new(sync.RWMutex)
	wg := &sync.WaitGroup{}

	files, err := ioutil.ReadDir(*dir)
	if err != nil {
		panic(err)
	}

	fileNum := len(files)
	if fileNum == 0 {
		fmt.Println("There is no file in ", dir)
		return
	}
	var totalSize int64
	totalSize = 0
	startTime := uint64(time.Now().UnixNano() / 1000000)

	for i := 0; i < *count; i++ {
		wg.Add(1)
		n := i % fileNum
		totalSize += files[n].Size()
		go Task(*dir+"/"+files[n].Name(), *url, wg)
	}

	wg.Wait()

	endTime := uint64(time.Now().UnixNano() / 1000000)
	size := totalSize / 1024
	sec := (endTime - startTime) / uint64(1000)
	fmt.Println("Used time:", endTime-startTime, "Millseconds, speed:", uint64(size)/sec, "kb/s")

}
