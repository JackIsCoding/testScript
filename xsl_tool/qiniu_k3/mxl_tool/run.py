#! /usr/bin/env python
import test_download_qn_sk
import os

count = 0
while count<15:
    os.system('rm -f ./out/*')
    test_download_qn_sk.run()
    print "\nfinish dowmload 20 *",count + 1
    count = count + 1
