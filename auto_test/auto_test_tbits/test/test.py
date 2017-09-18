#!/bin/env python
import re

p=re.compile('\d+\.\d+\.\d+\.\d+')
d='bc123abcdai.10.10.159.11adccc4567bc81.1.1b90bbb10.10.7.105hehe'
print p.findall(d)
print p.search(d).group()

p=re.compile('\d+')
d='we are123a 45good 678science9 0man!'
print p.findall(d)
print p.search(d).group()

m = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
print "m.string:", m.string
print "m.re:", m.re
print "m.pos:", m.pos
print "m.endpos:", m.endpos
print "m.lastindex:", m.lastindex
print "m.lastgroup:", m.lastgroup

p=re.compile('\D+')
d='we are123a 45good 678science9 0man!'
print p.findall(d)

p=re.compile('\w+')
d='we are123a 45good 678science9 0man!'
print p.findall(d)

p=re.compile('\s+')
d='we are123a 45good 678science9 0man!'
a=re.sub('\d+',' ',d)
print a
print p.split(a)

