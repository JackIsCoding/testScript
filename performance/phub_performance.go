package main
import (
    "net"
    "os"
    "fmt"
    "io/ioutil"
    "strconv"
    "crypto/aes"
    "crypto/cipher"
    "crypto/rand"
    "encoding/hex"
    "error"
)

type Peer_query struct{
    Version        uint32
    Seq            uint32
    Length         uint32
    Query_plus     uint8
    Peerid         string
    Cid            string_hex
    Filesize       uint64
    Gcid           string_hex
    Peer_capacity  uint32
    Internal_ip    uint32
    Nat_type       uint32
    Level_resource uint8
    Query_type     uint8
    Server_res_num uint32
    Query_times    uint32
    P2p_capacity   uint32
    Upnp_ip        uint32
    Upnp_port      uint16
}

func getRandomPeerid() string {
    str := make([]byte, 16)
    for i := 0; i < 16; i++ {
        str[i] = strconv.FormatInt(int64(rand.Intn(16)), 16)[0]
    }
        return strings.ToUpper(string(str))
}

func AESencode (data Peer_query){
    
}
