#!/bin/bash

def run():
    f=open('1.out','r')
    for line in f.readlines():
        val_list = line.split(':')
        print len(val_list)
        for i in range(0,len(val_list)):
            if val_list[i].find("sn_count")!=-1:
                print val_list[i+2]
               
if __name__ == "__main__":
   run() 
