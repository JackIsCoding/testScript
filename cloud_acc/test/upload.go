package main

import (
	"bytes"
	"crypto/sha1"
	"encoding/json"
	"fmt"
	"io"
	//	"math/rand"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	//	"time"
)

type BlockInfosReq struct {
	Sha1 string `json:"sha1"`
}

type RequestUploadReq struct {
	FileName   string          `json:"filename"`
	Filesize   int64           `json:"filesize"`
	BlockSize  int64           `json:"block_size"`
	BlockInfos []BlockInfosReq `json:"block_infos"`
}

type BlockInfosResp struct {
	Offset int64 `json:"offset"`
	Len    int64 `json:"len"`
}

type UploadDataInfo struct {
	UploadInfo BlockInfosResp `json:"upload_info"`
}

func requsetUpload(filePath string, blockSize int, offset int64, addrs string) {
	var uploadReq RequestUploadReq
	f, err := os.Open(filePath)
	defer f.Close()
	if err != nil {
		fmt.Println("Opem file failed", err)
		return
	}

	stat, err := f.Stat()
	if err != nil {
		fmt.Println("Get file stat failed", err)
		return
	}
	uploadReq.Filesize = stat.Size()
	uploadReq.BlockSize = int64(blockSize)

	blockInfos := []BlockInfosReq{}
	for {
		blocks := make([]byte, blockSize)
		ret, err := f.Seek(offset, 0)
		if ret <= 0 || err != nil {
			fmt.Println("Seek file failed", err, "offset ", offset)
		}
		n, err := f.Read(blocks)
		if err != nil {
			fmt.Println("Read file failed", err)
			break
		}
		offset += int64(n)
		if n < blockSize {
			blocks = blocks[0:n]
		}
		sha := sha1.New()
		sha.Write(blocks)
		bs := sha.Sum(nil)
		var blockInfo BlockInfosReq
		blockInfo.Sha1 = fmt.Sprintf("%x", bs)
		blockInfos = append(blockInfos, blockInfo)
		if n < blockSize || offset >= uploadReq.Filesize {
			break
		}
	}
	uploadReq.BlockInfos = blockInfos

	b, err := json.Marshal(uploadReq)
	if err != nil {
		fmt.Println("Json Marshal failed", err)
	}

	fmt.Println(string(b))
	fmt.Println("addrs" + addrs)
	resp, err := http.Post(addrs, "application/json", bytes.NewReader(b))
	if err != nil {
		fmt.Println("Http post failed", err)
		return
	}

	body := make([]byte, 10000)
	_, _ = resp.Body.Read(body)
	str := string(body)
	fmt.Println("Http post reaponse ", str)
}

func uploadData(filePath string, blockSize int, offset int64, addrs string) {
	f, err := os.Open(filePath)
	defer f.Close()
	if err != nil {
		fmt.Println("Opem file failed", err)
		return
	}

	stat, err := f.Stat()
	if err != nil {
		fmt.Println("Get file stat failed", err)
		return
	}
	fileSize := stat.Size()

	for {
		blocks := make([]byte, blockSize)
		ret, err := f.Seek(offset, 0)
		if ret <= 0 || err != nil {
			fmt.Println("Seek file failed", err)
		}
		n, err := f.Read(blocks)
		if err != nil {
			fmt.Println("Read file failed", err)
			break
		}

		if n < blockSize {
			blocks = blocks[0:n]
		}

		var dataInfo UploadDataInfo
		dataInfo.UploadInfo.Len = int64(n)
		dataInfo.UploadInfo.Offset = offset
		offset += int64(n)

		body := &bytes.Buffer{}
		writer := multipart.NewWriter(body)
		part, err := writer.CreateFormFile("file", filepath.Base(filePath))
		if err != nil {
			fmt.Println("Create Form file failed", err)
			return
		}
		_, err = io.Copy(part, bytes.NewReader(blocks))

		b, err := json.Marshal(dataInfo)
		if err != nil {
			fmt.Println("Json marshal failed", err)
			return
		}

		fmt.Println("json: ", string(b))

		err = writer.WriteField("json", string(b))
		if err != nil {
			fmt.Println("Writer json field failed")
			return
		}

		err = writer.Close()
		if err != nil {
			fmt.Println("Writer close failed", err)
			return
		}

		req, err := http.NewRequest("POST", addrs, body)
		if err != nil {
			fmt.Println("New request failed", err)
			return
		}
		req.Header.Set("Content-Type", writer.FormDataContentType())

		client := &http.Client{}
		resp, err := client.Do(req)

		if err != nil {
			fmt.Println("Request failed", resp.Body)
			return
		}

		rbody := make([]byte, 10000)
		_, _ = resp.Body.Read(rbody)
		str := string(rbody)
		fmt.Println("Http post reaponse ", str)

		if n < blockSize || offset >= fileSize {
			break
		}
	}
}

func usage() {
	fmt.Println("usage:uploader_client filePath blockSize offset {1(request_upload)|2(upload_data)} userid")
}

func main() {
	args := os.Args
	arg := len(os.Args)
	if arg < 6 {
		usage()
		return
	}
	filePath := args[1]
	blockSize, err := strconv.Atoi(args[2])
	if err != nil {
		usage()
		return
	}
	offset, err := strconv.Atoi(args[3])
	if err != nil {
		usage()
		return
	}
	oper, err := strconv.Atoi(args[4])
	if err != nil {
		usage()
		return
	}
	userid, err := strconv.Atoi(args[5])
	addrs1 := "http://10.10.191.2:80/request_upload?g=40303F67B89C5F132AE727CB67C8B7062A2610F4&ui=" + strconv.Itoa(userid) + "&ak=123&pk=344&s=123&e=1599669994&ms=100"
	addrs2 := "http://10.10.191.2:80/upload_data?g=40303F67B89C5F132AE727CB67C8B7062A2610F4&ui=" + strconv.Itoa(userid) + "&ak=123&pk=344&s=123&e=1599669994&ms=100"
	fmt.Println(filePath, blockSize, addrs1)

	if oper == 1 {
		requsetUpload(filePath, blockSize, int64(offset), addrs1)
	} else {
		uploadData(filePath, blockSize, int64(offset), addrs2)
	}
}
