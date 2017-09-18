#include <string>
#include <stdint.h>
#include <iostream>
#include <stdlib.h>
using namespace std;

uint32_t murmur_hash(const char *data, size_t len)
{
    uint32_t  h, k;

    h = 0 ^ len;

    while (len >= 4) {
        k  = data[0];
        k |= data[1] << 8;
        k |= data[2] << 16;
        k |= data[3] << 24;

        k *= 0x5bd1e995;
        k ^= k >> 24;
        k *= 0x5bd1e995;

        h *= 0x5bd1e995;
        h ^= k;

        data += 4;
        len -= 4;
    }

    switch (len) {
    case 3:
        h ^= data[2] << 16;
    case 2:
        h ^= data[1] << 8;
    case 1:
        h ^= data[0];
        h *= 0x5bd1e995;
    }

    h ^= h >> 13;
    h *= 0x5bd1e995;
    h ^= h >> 15;

    return h;;
}

uint32_t murmur_hash(const std::string &data)
{
    return murmur_hash(data.c_str(), data.length());
}

int hex2int(char c)
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

std::string hex2str(const std::string& str)
{
    std::string ret;
    if (!str.empty() && str.length() % 2 == 0) {
        for (unsigned i = 0; i < str.length(); i += 2) {
            char c = 16 * hex2int(str[i]) + hex2int(str[i+1]);
            ret.append(&c, 1);
        }
    } else {
        cout << "bad argument, str.length() must be even" << endl;
        exit(1);
    }
    return ret;
}

int main(int argc, const char *argv[])
{
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " key" << endl;
        return 0;
    }
    std::string key = argv[1];
    cout << murmur_hash(hex2str(key)) << endl;
    return 0;
}
