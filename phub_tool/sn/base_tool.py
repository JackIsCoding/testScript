#!/bin/env python

import os
import sys
from configobj import ConfigObj

def numToip(num):
    conf = "./conf.conf"
    config =ConfigObj(conf)
    return config['iplist']['%s'%num]




if __name__ == "__main__":
    num = "1443683386"
    print numToip(num)
    


