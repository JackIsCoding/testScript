#!/bin/env python
import sys
line_map = {}

fr=open('mshub_bt_emule.txt', 'r')
line = fr.readline()

fw=open('mshub_bt_emule.uniq.txt', 'wb')

count = 1

while line:
	sys.stdout.write(str(count)+'\r')
	sys.stdout.flush()
	if not line_map.has_key(line):
		fw.write(line)

	line_map[line] = 0
	line=fr.readline()#.replace('\n', '')
	count = count + 1
