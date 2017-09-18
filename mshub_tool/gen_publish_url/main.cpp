#include <iostream>
#include <string>
#include <stdio.h>
#include <openssl/md5.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

using namespace std;

static const char base64digits[] =
"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*-";

void base64_encode(unsigned char *out, const unsigned char *in, int inlen)
{
	for (; inlen >= 3; inlen -= 3) {
		*out++ = base64digits[in[0] >> 2];
		*out++ = base64digits[((in[0] << 4) & 0x30) | (in[1] >> 4)];
		*out++ = base64digits[((in[1] << 2) & 0x3c) | (in[2] >> 6)];
		*out++ = base64digits[in[2] & 0x3f];
		in += 3;
	}

	if (inlen > 0) {
		unsigned char fragment;

		*out++ = base64digits[in[0] >> 2];
		fragment = (in[0] << 4) & 0x30;

		if (inlen > 1)
			fragment |= in[1] >> 4;

		*out++ = base64digits[fragment];
		*out++ = (inlen < 2) ? '=' : base64digits[(in[1] << 2) & 0x3c];
		*out++ = '=';
	}

	*out = '\0';
}

int hex2int(const char c)
{
    int ret = 0; 
    
    if ('0' <= c && c <= '9') {
        ret = (c - '0');
    } else if ('a' <= c && c <= 'f') {
        ret = c - 'a' + 10;
    } else if ('A' <= c && c <= 'F') {
        ret = c - 'A' + 10;
    } else {
        ret = 0; 
    }    

    return ret; 
}

string hex2str(const string& str) 
{
    string ret; 

    if (!str.empty() && str.length() % 2 == 0) { 
        for (unsigned i = 0; i < str.length(); i += 2) { 
            char c = 16 * hex2int(str[i]) + hex2int(str[i+1]);
            ret.append(&c, 1);
        }    
    }    

    return ret; 
}

string str2hex(const string& str) 
{
    string ret; 

    char buffer[4];
    for (unsigned i = 0; i  < str.length(); ++i) {
        sprintf(buffer,"%02X",(unsigned char)str[i]); 
        ret += buffer;
    }    

    return ret; 
}

string puburl_encode(const string& host, const string& filename, const string& hexcid, uint64_t filesize, const string& hexgcid)
{
	if (host.empty() || filename.empty() || hexcid.length()!=40 || filesize==0 || hexgcid.length()!=40) {
		return "";
	}
	
	unsigned char inbuf[48];
	unsigned char fidbuf[64];
	
	string cid = hex2str(hexcid);
	string gcid = hex2str(hexgcid);
	
	memcpy(inbuf, cid.c_str(), 20);
	memcpy(inbuf+20, &filesize, 8);
	memcpy(inbuf+28, gcid.c_str(), 20);
	
	base64_encode(fidbuf, inbuf, 48);
	
	unsigned char md[16];
	unsigned char tidbuf[16];
	uint32_t tid_uint32 = 150;		
	tid_uint32 = ~tid_uint32;
	memcpy(tidbuf, &tid_uint32, sizeof(tid_uint32));
	uint32_t lower_size = (uint32_t)filesize; 
	memcpy(tidbuf+sizeof(int), &lower_size, sizeof(lower_size));
	tidbuf[8] = 47;
	tidbuf[9] = 13;
	tidbuf[10] = 94;
	tidbuf[11] = 118;
	tidbuf[12] = 39;
	tidbuf[13] = 71;
	tidbuf[14] = 156;
	tidbuf[15] = 59;
	MD5((const unsigned char*)tidbuf, sizeof(tidbuf), md);
	string tid = str2hex(string((const char*)md, sizeof(md)));
	
	return "http://" + host + "/" + filename + "?fid=" + string((const char*)fidbuf, sizeof(fidbuf)) + "&mid=666&threshold=150&tid=" + tid + "&srcid=9&verno=1";
}

int main(int argc, char* argv[])
{
	string host = "xlissue110.sandai.net";
	string filename = "µÁÃÎ¿Õ¼ä.rmvb";
	string hexcid = "450FC1F75F41F3C818528D6DF14D6BAA829E9B3D";
	uint64_t filesize = 60000000;
	string hexgcid = "3BBE1F88504EAAE5B94C9BF2EAD8FF182C586A9C";
	
	cout << puburl_encode(host, filename, hexcid, filesize, hexgcid) << endl;
	
	return 0;
}
