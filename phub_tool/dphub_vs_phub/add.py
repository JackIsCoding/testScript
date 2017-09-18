#! /bin/env python
fr = open('data1','r')
add_1 = 0
add_2 = 0
add_3 = 0

for item in fr.readlines():
    add_1 += int(item.split('    ')[0])
    add_2 += int(item.split('    ')[1])
    add_3 += int(item.split('    ')[2])
fr.close()
print add_1,add_2,add_3
